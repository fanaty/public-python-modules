from typing import Optional
import requests
import logging
from threading import Thread

# Config
ADMIN_CHAT_IDS = [
    1809111170, # Fede
    43759228,   # Agusavior
    680640473,  # Agna
    80627582,   # Pablo Vannini
]

class Telegram:
    # Secret bot token
    _token: Optional[str] = None

    @classmethod
    def set_token(cls, token: str) -> None:
        cls._token = token
    
    @classmethod
    def send_message(cls, text: str) -> None:
        # Pick only last 4000 chars
        text = text[-4000:]

        # Get and assert token
        token = cls._token
        assert token, 'Call Telegram.set_token first.'

        # For each chat, run a Thread with the request to telegram-bot API
        for chat_id in ADMIN_CHAT_IDS:
            def send_telegram_message_of_particular_user() -> None:
                try:
                    url = f'https://api.telegram.org/bot{token}/sendmessage'
                    payload = (
                        ('chat_id', chat_id),
                        ('text', f'```\n{text}\n```'),
                        ('parse_mode', 'Markdown'),
                    )

                    # Request
                    response = requests.get(url, params=payload, timeout=10)

                    # Raise exception if something went wrong
                    response.raise_for_status()
                except Exception as e:
                    logging.error(e, exc_info=True)
            
            # Run it in a seperate thread
            Thread(target=send_telegram_message_of_particular_user, daemon=True).start()
