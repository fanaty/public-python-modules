import logging
import colorlog

BACKUP_COUNT = 150
MAX_SIZE_B = 50 * (1024 ** 2)  # Logfile size before rollover
COLORED_LOGFILE = True
COLORS = ['black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white', 'orange']
OUTPUT_TO_STDOUT = True

def setup_logging(module_name: str, color: str = 'white'):
    assert color in COLORS
    
    log = logging.getLogger(module_name)
    
    if not log.hasHandlers():
        cf = colorlog.ColoredFormatter(
            "%(thin)s%(asctime)s%(reset)s - "
            f"%(bold{f'_{color}' if color else ''})s%(name)s%(reset)s"
            " - %(log_color)s%(levelname)s - %(message)s"
        )
        log.setLevel(logging.DEBUG)

        if OUTPUT_TO_STDOUT:
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)  # ToDo: change to WARN? Read from env?
            ch.setFormatter(cf)
            log.addHandler(ch)
    return log
