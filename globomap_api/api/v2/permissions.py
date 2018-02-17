# -*- coding: utf-8 -*-
"""
   Copyright 2018 Globo.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import logging

from flask import request
from flask_restplus import reqparse

from globomap_api import config
from globomap_api import exceptions
from globomap_api.api.v2 import api
from globomap_api.api.v2.keystone.keystone_auth import KeystoneAuth
from globomap_api.config import KEYSTONE_AUTH_ENABLE

logger = logging.getLogger(__name__)


class BasePermission(object):

    def __init__(self):
        if KEYSTONE_AUTH_ENABLE:
            token = self.validate_token()
            if not self.has_permission(token):
                api.abort(403)

    def has_permission(self):
        return True

    def has_perm(self, token, role):
        roles = [usr_role['name'] for usr_role in token['user']['roles']]
        if role in roles:
            return True
        return False

    def validate_token(self):

        try:
            value = request.headers.get('Authorization')
            auth = KeystoneAuth(value)
            token_data = auth.check_auth_token()
            return token_data

        except exceptions.InvalidToken:
            logger.error('Invalid Token %s' % token)
            api.abort(401, errors='Invalid Token')

        except:
            err_msg = 'Error to validate token'
            logger.exception(err_msg)
            api.abort(401, errors=err_msg)


class Admin(BasePermission):

    def has_permission(self, token):
        return self.has_perm(token, config.ADMIN)


class Read(BasePermission):

    def has_permission(self, token):
        return self.has_perm(token, config.READ)


class Write(BasePermission):

    def has_permission(self, token):
        return self.has_perm(token, config.WRITE)


class Collection(BasePermission):

    def has_permission(self, token):
        return self.has_perm(token, config.COLLECTION)


class Edge(BasePermission):

    def has_permission(self, token):
        return self.has_perm(token, config.EDGE)


class Graph(BasePermission):

    def has_permission(self, token):
        return self.has_perm(token, config.GRAPH)
