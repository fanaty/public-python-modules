import requests
from threading import Thread
import os

from ppm.log import setup_logging

# Config
AGNA_CHAT_ID = '680640473'

# We get ADMIN_CHAT_IDS env, or we set AGNA_CHAT_ID if the env is not defined
ADMIN_CHAT_IDS = os.getenv('ADMIN_CHAT_IDS', AGNA_CHAT_ID)

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

        # Create admin chat id list
        admin_chat_ids_list_of_int = list(map(int, ADMIN_CHAT_IDS.split(',')))

        if not token:
            # Log
            if not cls._warning_has_been_printed:
                cls.logger.warn('Environment TELEGRAM_BOT_TOKEN is not defined. Will not use Telegram.')
            
                # Flag
                cls._warning_has_been_printed = True

            return

        # For each chat, run a Thread with the request to telegram-bot API
        for chat_id in admin_chat_ids_list_of_int:
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
