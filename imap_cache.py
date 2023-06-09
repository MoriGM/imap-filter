import logging
import re
from imaplib import IMAP4_SSL


class ImapCache:
    def __init__(self, connection: IMAP4_SSL) -> None:
        self.connection = connection

    def sender(self, mailbox: str, uid: str) -> str:
        header = self.header(mailbox, uid)
        sender = header['From']
        if sender.__contains__('<'):
            matches = re.search(r'(?P<email>[\w]+@[\w.]+)', sender)
            if matches is None:
                return ''
            sender = matches.group('email')

        return sender

    def header(self, mailbox: str, uid: str) -> dict[str, str]:
        self.connection.select(mailbox)
        status, header = self.connection.uid('fetch', uid, 'BODY[HEADER]')

        if status != 'OK':
            self.connection.unselect()
            logging.warning(f'Header for {uid} couldn\'t be recevied')
            return {}

        header = header[0][1].decode('utf-8')
        header = re.split(r'\r\n(?!\\s)', header)
        self.connection.unselect()

        header = [head.split(':', 1) for head in header if head.__contains__(':')]
        header = {key: value for (key, value) in header}
        return header
