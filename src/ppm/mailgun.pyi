from typing import Sequence

MAIL_HOST: str
MAIL_PORT: int
MAIL_SENDER: str
MAIL_SENDERNAME: str
HOST = MAIL_HOST
PORT = MAIL_PORT
SENDER = MAIL_SENDER
SENDERNAME = MAIL_SENDERNAME

class Mailgun:
    @classmethod
    def setup_credentials(cls, username_smtp: str, password_smtp: str): ...
    @classmethod
    def send_email(cls, to_addrs: Sequence[str], subject: str, body: str): ...
