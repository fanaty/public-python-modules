import requests
from threading import Thread
import os

from ppm.log import setup_logging

# Config
ADMIN_CHAT_IDS = [
#    1809111170, # Fede
#    43759228,   # Agusavior
    680640473,  # Agna
#    80627582,   # Pablo Vannini
]

class Telegram:
    # Class variable
    _warning_has_been_printed = False
    logger = setup_logging('Telegram')

    @classmethod
    def send_message(cls, text: str) -> None:
        # Pick only last 4000 chars
        text = text[-4000:]

        # Get and assert token
        token = os.getenv('TELEGRAM_BOT_TOKEN')

        if not token:
            # Log
            if not cls._warning_has_been_printed:
                cls.logger.warn('Environment TELEGRAM_BOT_TOKEN is not defined. Will not use Telegram.')
            
                # Flag
                cls._warning_has_been_printed = True

            return

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
                    cls.logger.error(e, exc_info=True)
            
            # Run it in a seperate thread
            Thread(target=send_telegram_message_of_particular_user, daemon=True).start()
