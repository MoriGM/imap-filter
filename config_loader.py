import os
import tomllib
import logging


def get_accounts():
    accounts = {}

    file = './accounts.toml'
    if not os.path.exists(file) or not os.path.isfile(file):
        return accounts

    with open('./accounts.toml', 'rb') as file:
        toml = tomllib.load(file)

        for account in toml['account']:
            if not all(x in account for x in ['email', 'password', 'server']):
                print(account)
                logging.warn('Missing email, password or server!')
                continue

            email = account['email']
            accounts[email] = account

    return accounts


def get_filter_tomls():
    path = './filters/'
    if not os.path.exists(path):
        logging.error('Folder for filters is missing.')
        return []
    if not os.path.isdir(path):
        logging.error('Folder for filters is not a folder.')
        return []

    filters = {}

    for file in os.listdir(path):
        if not file.endswith('.toml'):
            continue

        absolute_file = path + file
        if not os.path.isfile(absolute_file):
            logging.warn(f'{file} is not a file in folder {path}')
            continue

        with open(absolute_file, 'rb') as fp:
            filters[os.path.basename(file)] = tomllib.load(fp)

    return filters
