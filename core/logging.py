import logging
import sys
from functools import lru_cache


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


@lru_cache(maxsize=1)
def get_logger():
    _logger = logging.getLogger("uvicorn")
    _logger.info('Starting the app logging...')

    return _logger


logger: logging.Logger = get_logger()
