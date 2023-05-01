import logging
from logging.handlers import RotatingFileHandler


def get_logger():
    error_logger = logging.getLogger('error')
    # Add handlers
    err_handler = RotatingFileHandler('error.log', maxBytes=100000, backupCount=1)
    # Add formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # Set level
    err_handler.setFormatter(formatter)
    error_logger.addHandler(err_handler)
    error_logger.setLevel(logging.ERROR)
    return error_logger
