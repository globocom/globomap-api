import redis
from redis.sentinel import Sentinel

from globomap_api import config


class RedisClient(object):

    def get_redis_conn(self):
        if config.REDIS_SENTINEL_ENDPOINT_SIMPLE:
            try:
                sentinel = Sentinel(
                    config.REDIS_SENTINELS, socket_timeout=0.1)
                master = sentinel.discover_master(
                    config.REDIS_SENTINEL_SERVICE_NAME)
                connection = redis.StrictRedis(
                    host=master[0],
                    port=master[1],
                    password=config.REDIS_SENTINEL_PASSWORD)
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
