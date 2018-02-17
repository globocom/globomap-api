import json
import logging
from datetime import datetime

from flask import abort
from werkzeug.exceptions import Forbidden

from globomap_api import config
from globomap_api.api.v2.keystone.auth import Auth
from globomap_api.exceptions import AuthException
from globomap_api.exceptions import InvalidToken
from globomap_api.models.redis import RedisClient


class KeystoneAuth(object):

    logger = logging.getLogger(__name__)

    def __init__(self, value):
        self.value = value

    def check_auth_token(self):
        auth = self.value
        if auth.find('Token token=') == 0:
            token = auth[12:]
            token_data = self.get_cache_info_token(token)
            if not token_data:
                auth = Auth()
                token_data = auth.validate_token(token)
                if token_data:
                    token_data = token_data.to_dict()
                    self.set_cache_info_token(token_data)
                else:
                    self.logger.error('Invalid Token %s' % token)
                    raise InvalidToken('Invalid Token')
        else:
            self.logger.error('Invalid Token %s' % token)
            raise InvalidToken('Invalid Token')

        return token_data

    def get_cache_info_token(self, token):
        conn = RedisClient().get_redis_conn()
        token_data = conn.get(token)
        if token_data:
            token_data = json.loads(token_data)

        return token_data

    def set_cache_info_token(self, token_data):
        conn = RedisClient().get_redis_conn()

        token = token_data['token']['id']

        token_expires = token_data['token']['expires']
        datetime_object = datetime.strptime(
            token_expires, '%Y-%m-%dT%H:%M:%SZ')
        ttl = (datetime.utcnow().now() - datetime_object)
        token_data = json.dumps(token_data)
        conn.setex(token, token_data, ttl.seconds)
