from imaplib import IMAP4_SSL
import logging
import search_filter


def run_seach_filters(connection: IMAP4_SSL, content: dict, filter_name: str) -> list[str]:
    if 'filter' not in content:
        logging.warning(f'Missing filter table in filter {filter_name}')
        return []
    if 'src' not in content['setup']:
        logging.warning(f'Missing source folder in filter {filter_name}')
        return []

    search_filter_functions = {
            'senderEndsWith': search_filter.sender_filter
    }
    search_filter_content = ''
    for filter in content['filter']:
        if 'name' not in filter:
            continue

        filter_name = filter['name']
        if filter_name not in search_filter_functions:
            logging.warning(f'There is no filter with the name {filter_name}')
            continue

        filter_function = search_filter_functions[filter['name']]
        search_filter_content += filter_function(filter)

    if search_filter_content == '':
        return []

    connection.select(content['setup']['src'])
    status, uids = connection.search(None, search_filter_content)

    if status != 'OK' or not uids:
        return []

    connection.unselect()

    return uids[0].decode('utf-8').split(' ')
