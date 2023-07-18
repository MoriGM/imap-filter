import logging
import os
from imaplib import IMAP4_SSL
from imap_cache import ImapCache

import config_loader
import imap_filter
import imap_outcome


def main():
    LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
    logging.basicConfig(level=LOGLEVEL)
    logging.info('Start Filter')
    filters = config_loader.get_filter_tomls()

    config_accounts = config_loader.get_accounts()
    imap_connections = {}
    imap_cache = {}

    for email in config_accounts:
        config = config_accounts[email]

        if 'port' not in config:
            config['port'] = 993

        connection = IMAP4_SSL(config['server'], config['port'])
        connection.login(email, config['password'])
        imap_connections[email] = connection
        imap_cache[email] = ImapCache(connection)

    for f in filters:
        content = filters[f]
        if 'setup' not in content:
            logging.warning(f'Missing setup table in {f}')
            continue
        if 'email' not in content['setup']:
            logging.warning(f'Missing email in setup table in {f}')
            continue
        if 'src' not in content['setup']:
            logging.warning(f'Missing source mailbox in setup table in {f}')
            continue

        email = content['setup']['email']
        connection = imap_connections[email]
        cache = imap_cache[email]
        src = content['setup']['src']

        uids = imap_filter.run_seach_filters(connection, content, f)
        if len(uids) == 0:
            logging.info(f"Nothing found for {f}")
            continue

        uids = imap_filter.run_fetch_filter(cache, content, f, uids)

        if len(uids) == 0:
            logging.info(f"Nothing found for {f}")
            continue

        if 'dst' in content['setup']:
            dst = content['setup']['dst']
            imap_outcome.move_uids(connection, uids, src, dst)
        imap_outcome.delete_uids(connection, uids, src)


if __name__ == '__main__':
    main()
