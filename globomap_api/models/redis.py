import redis
from flask import current_app as app
from redis.sentinel import Sentinel

from globomap_api import config


class RedisClient(object):

    def get_redis_conn(self):
        if config.REDIS_SENTINEL_ENDPOINT_SIMPLE:
            redis_sentinels = [(rs, config.REDIS_SENTINELS_PORT)
                               for rs in config.REDIS_SENTINELS.split(',')]
            redis_service = config.REDIS_SENTINEL_SERVICE_NAME
            redis_password = config.REDIS_SENTINEL_PASSWORD
            try:
                sentinel = Sentinel(redis_sentinels, socket_timeout=0.1)
                master = sentinel.discover_master(redis_service)
                connection = redis.StrictRedis(
                    host=master[0], port=master[1], password=redis_password)
            except Exception as e:
                app.logger.error(
                    'Failed to connect to redis Sentinel: {}'.format(e))
        else:
            try:
                connection = redis.Redis(
                    host=config.REDIS_HOST,
                    port=config.REDIS_PORT,
                    password=config.REDIS_PASSWORD
                )
            except Exception as e:
                app.logger.error(
                    'Failed to connect to redis: {}'.format(model, e))
        return connection
