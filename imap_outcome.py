from imaplib import IMAP4_SSL


def move_uids(connection: IMAP4_SSL, uids: list[str], src: str, dst: str):
    uids_set = ','.join(uids)
    connection.select(src)
    connection.uid('copy', uids_set, dst)
    connection.unselect()


def delete_uids(connection: IMAP4_SSL, uids: list[str], src: str):
    uids_set = ','.join(uids)
    connection.select(src)
    connection.uid('store', uids_set, '+FLAGS', '\\Deleted')
    connection.expunge()
    connection.unselect()
