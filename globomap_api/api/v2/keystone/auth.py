import logging

from flask import current_app as app
from keystoneauth1 import session
from keystoneauth1.exceptions.http import NotFound
from keystoneauth1.identity import v2
from keystoneclient.v2_0 import client

from globomap_api import config
from globomap_api.exceptions import AuthException
from globomap_api.exceptions import InvalidToken


class Auth(object):

    def __init__(self):

        kwargs = {
            'insecure': True,
            'username': config.KEYSTONE_USERNAME,
            'password': config.KEYSTONE_PASSWORD,
            'tenant_name': config.KEYSTONE_TENANT_NAME,
            'auth_url': config.KEYSTONE_AUTH_URL,
            'timeout': 3
        }

        self.conn = client.Client(**kwargs)

    def validate_token(self, token):
        try:
            return self.conn.tokens.validate(token=token)
        except NotFound:
            app.logger.error('Cannot validate token %s' % token)
            raise InvalidToken('Invalid Token')
        except:
            raise AuthException('Error to validate token')
