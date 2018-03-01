from flask import current_app as app
from globomap_auth_manager.auth import Auth


def auth(username=None, password=None):

    auth_url = app.config['KEYSTONE_AUTH_URL']
    tenant_name = app.config['KEYSTONE_TENANT_NAME']

    auth_inst = Auth()
    set_config_redis(auth_inst)
    auth_inst.set_config_keystone(auth_url, tenant_name, username, password)
    auth_inst.start_conn()
    token = auth_inst.get_token_data()

    return token


def set_config_redis(auth_inst):
    sentinel_endpoint_simple = app.config['REDIS_SENTINEL_ENDPOINT_SIMPLE']
    sentinel_service_name = app.config['REDIS_SENTINEL_SERVICE_NAME']
    sentinel_password = app.config['REDIS_SENTINEL_PASSWORD']
    sentinels_port = app.config['REDIS_SENTINELS_PORT']
    sentinels = app.config['REDIS_SENTINELS']
    host = app.config['REDIS_HOST']
    port = app.config['REDIS_PORT']
    password = app.config['REDIS_PASSWORD']
    if sentinel_endpoint_simple:
        auth_inst.set_config_sentinel(
            sentinel_endpoint_simple, sentinels_port, sentinels,
            sentinel_service_name, sentinel_password
        )
    else:
        auth_inst.set_config(host, port, password)
