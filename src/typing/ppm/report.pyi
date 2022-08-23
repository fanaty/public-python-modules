from _typeshed import Incomplete
from ppm.mailgun import Mailgun as Mailgun
from ppm.telegram import Telegram as Telegram
from typing import Any

USE_TELEGRAM: bool
SEND_MAILS: bool
REPORT_MAX_TELEGRAM_MESSAGES_BY_EXCEPTION: int
REPORT_MAX_TELEGRAM_MESSAGES_BY_EVENT: int
REPORT_ADMIN_MAILS: Incomplete
Stringable = Any

class Report:
    @classmethod
    def setup(cls, telegram_token: str, username_smtp: str, password_smtp: str, footer: str): ...
    @classmethod
    def exception(cls, exception: Exception, **kwargs: Stringable): ...
    @classmethod
    def event_once(cls, event: str, **kwargs: Stringable): ...
    @classmethod
    def event_always(cls, event: str, **kwargs: Stringable): ...
    @classmethod
    def event(cls, event: str, max_times_to_report: int = ..., send_email: bool = ..., **kwargs: Stringable) -> None: ...
    @classmethod
    def clear_cache(cls) -> None: ...
