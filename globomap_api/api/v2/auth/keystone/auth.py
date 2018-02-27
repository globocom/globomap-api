import json
import logging
from datetime import datetime

from flask import abort
from flask import current_app as app
from werkzeug.exceptions import Forbidden

from globomap_api import config
from globomap_api.api.v2.auth.keystone.keystone_auth import KeystoneAuth
from globomap_api.config import KEYSTONE_AUTH_ENABLE
from globomap_api.exceptions import AuthException
from globomap_api.exceptions import InvalidToken
from globomap_api.models.redis import RedisClient


class Auth(object):

    def set_credentials(self, username=None, password=None):
        self.keystone_auth = KeystoneAuth(username, password)
        return self.keystone_auth

    def get_auth_token(self):
        return self.keystone_auth.conn.auth_ref['token']

    def is_enable(self):
        return True if KEYSTONE_AUTH_ENABLE == '1' else False

    def set_auth_token(self, value):
        self.auth_token = value

    def check_auth_token(self):
        if self.auth_token is not None and \
                self.auth_token.find('Token token=') == 0:
            token = self.auth_token[12:]
            token_data = self.get_cache_info_token(token)
            if not token_data:
                keystone_auth = self.set_credentials()
                token_data = keystone_auth.validate_token(token)
                if token_data:
                    token_data = token_data.to_dict()
                    self.set_cache_info_token(token_data)
                else:
                    app.logger.error('Invalid Token %s' % token)
                    raise InvalidToken('Invalid Token')
        else:
            app.logger.error('Invalid Token')
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
        conn.set(token, token_data, ex=ttl.seconds)
