import logging

from flask import current_app as app
from keystoneauth1 import session
from keystoneauth1.exceptions.http import NotFound
from keystoneauth1.exceptions.http import Unauthorized
from keystoneauth1.identity import v2
from keystoneclient.v2_0 import client

from globomap_api import config
from globomap_api import exceptions as globomap_exc


class KeystoneAuth(object):

    def __init__(self, username=None, password=None):

        username = username if username else config.KEYSTONE_USERNAME
        password = password if password else config.KEYSTONE_PASSWORD

        if config.KEYSTONE_TENANT_NAME is None:
            msg = 'Auth not working. KEYSTONE_TENANT_NAME is not set'
            app.logger.exception(msg)
            raise globomap_exc.AuthException(msg)

        if config is None:
            msg = 'Auth not working. Username is not set'
            app.logger.exception(msg)
            raise globomap_exc.AuthException(msg)

        if password is None:
            msg = 'Auth not working. Password is not set'
            app.logger.exception(msg)
            raise globomap_exc.AuthException(msg)

        if config.KEYSTONE_AUTH_URL is None:
            msg = 'Auth not working. KEYSTONE_AUTH_URL is not set'
            app.logger.exception(msg)
            raise globomap_exc.AuthException(msg)

        kwargs = {
            'insecure': True,
            'username': username,
            'password': password,
            'tenant_name': config.KEYSTONE_TENANT_NAME,
            'auth_url': config.KEYSTONE_AUTH_URL,
            'timeout': 3
        }

        try:
            self.conn = client.Client(**kwargs)
        except Unauthorized:
            raise globomap_exc.Unauthorized('Unauthorized')

    def validate_token(self, token):
        try:
            return self.conn.tokens.validate(token=token)
        except NotFound:
            app.logger.error('Cannot validate token %s' % token)
            raise globomap_exc.InvalidToken('Invalid Token')
        except:
            raise globomap_exc.AuthException('Error to validate token')
