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
import functools

from globomap_auth_manager.auth import Auth


def permission_classes(permission_classes):
    def outer(func):
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            auth = Auth()
            if auth.is_enable():
                for permission_class in permission_classes:
                    permission_class(auth)
            return func(self, *args, **kwargs)
        return inner
    return outer
