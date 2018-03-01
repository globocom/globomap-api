import functools

from flask import current_app as app
from globomap_auth_manager.auth import Auth

from globomap_api.api.v2.auth import facade


def permission_classes(permission_classes):
    def outer(func):
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            auth = Auth()
            if app.config['KEYSTONE_AUTH_ENABLE'] == '1':
                facade.set_config_redis(auth)
                auth.start_conn()
                for permission_class in permission_classes:
                    permission_class(auth)
            return func(self, *args, **kwargs)
        return inner
    return outer
