import logging
from functools import lru_cache


@lru_cache(maxsize=1)
def get_logger():
    _logger = logging.getLogger("uvicorn")
    _logger.info('Starting the app logging...')

    return _logger


logger: logging.Logger = get_logger()
