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
from globomap_auth_manager.auth import Auth

from globomap_api.api.v2.auth.exceptions import AuthException


def create_token(username=None, password=None):

    auth_inst = Auth()
    if auth_inst.is_enable():
        auth_inst.set_credentials(username, password)
        token = auth_inst.get_token_data()
    else:
        raise AuthException('Auth is not enabled')

    return token
