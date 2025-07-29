import logging
import sys


logger = logging.getLogger(__name__)

# Formatters
formater = logging.Formatter(
    fmt="%(levelname)-7s %(asctime)s.%(msecs)03d %(module)10s:%(lineno)-3d  - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Handlers
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("logs/root_logger.log", encoding="utf-8", mode="w")

stream_handler.setFormatter(formater)
file_handler.setFormatter(formater)

logger.handlers = [stream_handler, file_handler]

logger.setLevel(logging.DEBUG)
