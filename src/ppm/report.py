import traceback
from typing import Any, Optional, Sequence
from ppm.mailgun import Mailgun
from ppm.telegram import Telegram
from threading import Lock
from ppm.log import setup_logging

# Config
REPORT_MAX_TELEGRAM_MESSAGES_BY_EXCEPTION = 10
REPORT_MAX_TELEGRAM_MESSAGES_BY_EVENT = 5

# Type alias
# All objects are stringables so...
Stringable = Any

# Abstraction to report bugs or uncommon behavior to the developer
class Report:
    # Lock for count
    _COUNTER_LOCK = Lock()

    # Logging logger
    _log = setup_logging('Report')

    # Register the amount of times that every trace did ocurred
    _reports: Stringable = dict()

    # String limit per info kwarg
    _STRING_LEN_LIMIT_PER_INFO_KWARG = 1600

    # Class attributes
    _footer: str = ''
    _sender_email_address: str = ''
    _sender_name: str = ''
    _receiver_email_addresses: Sequence[str]

    @classmethod
    def setup(cls,
        telegram_token: str,
        username_smtp: str,
        password_smtp: str,
        footer: str,
        sender_email_address: str,
        receiver_email_addresses: Sequence[str],
        sender_name: str,
        ) -> None:
        # Setup telegram bot
        Telegram.set_token(token=telegram_token)

        # Setup mailgun
        Mailgun.setup_credentials(username_smtp=username_smtp, password_smtp=password_smtp)
        
        # Store class variables
        cls._footer = footer
        cls._sender_email_address = sender_email_address
        cls._sender_name = sender_name
        cls._receiver_email_addresses = receiver_email_addresses

    @classmethod
    def _increment_and_get_times(cls, hashable_string: str) -> Stringable:
        with Report._COUNTER_LOCK:
            # If the trace is new, register it in _reports
            if hashable_string not in Report._reports:
                Report._reports[hashable_string] = 0

            # Increment
            Report._reports[hashable_string] += 1

            # Times that the exception ocurred
            return Report._reports[hashable_string]


    @classmethod
    def exception(cls, exception: Exception, **kwargs: Stringable) -> None:
        trace = traceback.format_exc()

        Report.event(trace, max_times_to_report = REPORT_MAX_TELEGRAM_MESSAGES_BY_EXCEPTION, **kwargs)


    @classmethod
    def event_once(cls, event: str, send_email: bool = False, **kwargs: Stringable) -> None:
        return cls.event(event, send_email=send_email, max_times_to_report = 1, **kwargs)


    @classmethod
    def event_always(cls, event: str, send_email: bool = False, **kwargs: Stringable) -> None:
        return cls.event(event, send_email=send_email, max_times_to_report=500, **kwargs)

    
    @classmethod
    def event(cls,
        event: str,
        max_times_to_report: int = REPORT_MAX_TELEGRAM_MESSAGES_BY_EVENT,
        send_email: bool = False,
        **kwargs: Stringable,
        ) -> None:
        # Increment times counter
        times = cls._increment_and_get_times(event)

        # Header information about the exception
        header = f'{times}/{max_times_to_report}) {event}'
        footer = cls._footer

        # Extra information given in kwargs
        info = ''
        for k, v in kwargs.items():
            # If v is bytes, decode
            if type(v) is bytes:
                v = v.decode('utf-8')

            # Value to string
            v = str(v)
            
            # Crop large strings
            if len(v) > Report._STRING_LEN_LIMIT_PER_INFO_KWARG:
                v = '...' + v[-Report._STRING_LEN_LIMIT_PER_INFO_KWARG:]

            # Added wkarg to info
            info += f'{k}={v}\n'

        # Join header with trace
        message = f'{header}\n{info}\n{footer}'

        # Send it to the developer
        if times <= max_times_to_report:
            # Send using telegram
            Telegram.send_message(message)

            # May send email
            if send_email:
                Mailgun.send_email(
                    to_addrs=cls._receiver_email_addresses,
                    subject=event,
                    body=message,
                    sender_email_address=cls._sender_email_address,
                    sender_name=cls._sender_name,
                )

            # Print it
            cls._log.debug(event)

    @classmethod
    def clear_cache(cls) -> None:
        cls._reports = dict()
