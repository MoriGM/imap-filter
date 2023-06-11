import logging
from imap_cache import ImapCache


def sender_ends_with(cache: ImapCache, mailbox: str, uid: str, content: dict) -> bool:
    sender = cache.sender(mailbox, uid)

    if 'name' not in content:
        logging.warning('Key name is missing')
        return False

    return sender.endswith('')
