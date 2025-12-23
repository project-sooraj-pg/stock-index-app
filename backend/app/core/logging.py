import logging
import os
from logging.handlers import TimedRotatingFileHandler


def setup_logging():
    logger = logging.getLogger('stock-index-app')
    if not logger.handlers:
        formatter = logging.Formatter('[%(asctime)s] [%(process)-5s] [%(threadName)-10s] [%(levelname)-5s] %(message)s')
        os.makedirs('logs', exist_ok=True)
        handler = TimedRotatingFileHandler(filename='logs/app.log', when='midnight', interval=1, backupCount=30)
        handler.setFormatter(formatter)
        logger.addHandler(handler)