from threading import Thread
from typing import Any, Callable, TypeVar, Tuple, List, Union
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

# TypeVars
T = TypeVar('T')
U = TypeVar('U')

def launch_in_parallel_and_join(f0: Callable[..., T], f1: Callable[..., U]) -> Tuple[T, U]:
    '''This function launch two functions in parallel and then wait until both finish'''

    # Lists with one element, in order to pass variable as reference.
    # If something went wrong with the thread, the exception will be stored in there.
    first_value_ref: List[Union[T, Exception]] = []   
    second_value_ref: List[Union[U, Exception]] = []
    def decorator(f: Callable[..., Any], is_first: bool):
        try:
            if is_first:
                first_value_ref[0] = f()
            else:
                second_value_ref[0] = f()
        except Exception as e:
            Report.exception(e, place=f.__name__)

            if is_first:
                first_value_ref[0] = e
            else:
                second_value_ref[0] = e
    thread0 = Thread(target=decorator(f0, True))
    thread1 = Thread(target=decorator(f1, False))
    thread0.start()
    thread1.start()
    thread0.join()
    thread1.join()
    assert len(first_value_ref) == 1 and len(second_value_ref) == 1
    first_value = first_value_ref[0]
    second_value = second_value_ref[0]
    if isinstance(first_value, Exception):
        raise first_value
    if isinstance(second_value, Exception):
        raise second_value
    return first_value, second_value