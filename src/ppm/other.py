from threading import Thread
from typing import Any, Callable
from ppm.report import Report
import os

def launch_in_other_thread(target: Callable[[], Any]):
    def _target_with_report():
        try:
            target()
        except Exception as e:
            Report.exception(e, place=target.__name__)
    
    # Launch
    Thread(target=_target_with_report, daemon=True).start()
    
    return None


def get_env_or_raise(environment_variable_name: str) -> str:
    env_value = os.getenv(environment_variable_name)
    if not env_value:
        raise Exception(f'You have to define an environment variable called {environment_variable_name}.')
    return env_value
