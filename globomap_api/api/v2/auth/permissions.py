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
from flask import current_app as app

from globomap_api.api.v2 import api


class BasePermission(object):

    def __init__(self, auth):
        self.auth = auth
        self.validate_token()

    def has_permission(self, token=None):
        return True

    def has_perm(self, token, role):
        roles = [usr_role['name'] for usr_role in token['roles']]
        if role in roles:
            return True
        return False

    def validate_token(self):
        token_data = self.auth.get_token_data_details()
        if not self.has_permission(token_data):
            api.abort(403, 'User have not permission to this action')
            app.logger.error('User have not permission to this action')


class Admin(BasePermission):

    def has_permission(self, token):
        return self.has_perm(token, app.config['ADMIN'])


class Read(BasePermission):

    def has_permission(self, token):
        return self.has_perm(token, app.config['READ'])


class Write(BasePermission):

    def has_permission(self, token):
        return self.has_perm(token, app.config['WRITE'])
