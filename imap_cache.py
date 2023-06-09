import logging
import re
from imaplib import IMAP4_SSL


class ImapCache:
    def sender(self, connection: IMAP4_SSL, mailbox: str, uid: str) -> str:
        connection.select(mailbox)
        status, header = connection.uid('fetch', uid, 'BODY[HEADER]')

        if status != 'OK':
            logging.warning('')
            return ''

        header = header[0][1].decode('utf-8')
        header = re.split('\r\n(?!\\s)', header)
        print(header)
        connection.unselect()
        return ''
