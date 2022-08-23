from _typeshed import Incomplete

ADMIN_CHAT_IDS: Incomplete

class Telegram:
    @classmethod
    def set_token(cls, token: str): ...
    @classmethod
    def send_message(cls, text: str): ...
