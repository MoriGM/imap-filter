import logging


def sender_filter(config):
    if not isinstance(config, dict):
        logging.warn(f'{config} is not a dict')
        return ''

    filter = ''

    if 'from' in config:
        from_sender = config['from']
        filter = f'FROM "{from_sender}"'

    return filter
