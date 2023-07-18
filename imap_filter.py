from imaplib import IMAP4_SSL
import logging
from imap_cache import ImapCache

import search_filter
import fetch_filter


def run_seach_filters(connection: IMAP4_SSL, content: dict, filter_name: str) -> list[str]:
    if 'filter' not in content:
        logging.warning(f'Missing filter table in filter {filter_name}')
        return []
    if 'src' not in content['setup']:
        logging.warning(f'Missing source folder in filter {filter_name}')
        return []

    search_filter_functions = {
        'senderEndsWith': search_filter.sender_filter,
        'senderStartsWith': search_filter.sender_filter,
        'senderContains': search_filter.sender_filter,
    }
    search_filter_content = []
    for filter in content['filter']:
        if 'name' not in filter:
            continue

        filter_name = filter['name']
        if filter_name not in search_filter_functions:
            logging.warning(f'There is no filter with the name {filter_name}')
            continue

        filter_function = search_filter_functions[filter['name']]
        filter_result = filter_function(filter)

        if filter_result == '':
            continue

        search_filter_content.append(filter_result)

    if len(search_filter_content) == 0:
        return []

    connection.select(content['setup']['src'])
    status, uids = connection.uid(
        'search', ' AND '.join(search_filter_content))

    if status != 'OK' or len(uids[0]) == 0:
        return []

    connection.unselect()

    return uids[0].decode('utf-8').split(' ')


def run_fetch_filter(cache: ImapCache, content: dict, filter_name: str, uids: list[str]) -> list[str]:
    if 'filter' not in content:
        logging.warning(f'Missing filter table in filter {filter_name}')
        return []
    if 'src' not in content['setup']:
        logging.warning(f'Missing source folder in filter {filter_name}')
        return []

    search_filter_functions = {
        'senderEndsWith': fetch_filter.sender_ends_with,
    }
    filtered_uids = []
    for uid in uids:
        filter_result = True
        for filter in content['filter']:
            if 'name' not in filter:
                continue

            filter_name = filter['name']
            if filter_name not in search_filter_functions:
                logging.warning(f'There is no filter with named {filter_name}')
                continue

            filter_function = search_filter_functions[filter['name']]
            filter_result = filter_function(
                cache, content['setup']['src'], uid, filter) and filter_result

        if filter_result:
            filtered_uids.append(uid)

    return filtered_uids
