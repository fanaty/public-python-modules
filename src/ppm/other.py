from threading import Thread
from typing import Any, Callable
from ppm.report import Report


def launch_in_other_thread(target: Callable[[], Any]):
    def _target_with_report():
        try:
            target()
        except Exception as e:
            Report.exception(e, place=target.__name__)
    
    # Launch
    Thread(target=_target_with_report, daemon=True).start()
    
    return None
