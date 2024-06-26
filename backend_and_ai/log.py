"""Module for generating application logs."""
import logging
import time

from pathlib import Path

try:
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
except Exception as e:
    logging.error(str(e))

timestr = time.strftime("%Y%m%d-%H%M%S")
log_filename = "log_" + timestr + ".log"
log_filepath = log_dir.joinpath(log_filename)

LOG_FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(levelname)s %(message)s"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(log_filepath)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# stream_handler = logging.StreamHandler()
# stream_handler.setLevel(logging.DEBUG)
# stream_handler.setFormatter(logging.Formatter(log_format))

logger.addHandler(file_handler)
logger.addHandler(logging.StreamHandler())