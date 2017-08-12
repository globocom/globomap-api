import logging
from logging.handlers import RotatingFileHandler
from os import environ

from app import create_app

if __name__ == '__main__':
    application = create_app('config')
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s %(threadName)s %(levelname)s %(message)s')
    application.logger.addHandler(handler)
    application.run('0.0.0.0', int(environ.get('PORT', '5000')))
