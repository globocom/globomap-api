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
import os

ARANGO_DB = os.getenv('ARANGO_DB')
ARANGO_USERNAME = os.getenv('ARANGO_USERNAME')
ARANGO_PASSWORD = os.getenv('ARANGO_PASSWORD')
ARANGO_PROTOCOL = os.getenv('ARANGO_PROTOCOL')
ARANGO_HOST = os.getenv('ARANGO_HOST')
ARANGO_PORT = os.getenv('ARANGO_PORT')
FLASK_DEBUG = os.getenv('FLASK_DEBUG', False)
API_PLUGINS_CONFIG_FILE = 'api_plugins'
SPECS = {
    'documents': 'globomap_api/specs/documents.json',
    'edges': 'globomap_api/specs/edges.json',
    'documents_partial': 'globomap_api/specs/documents_partial.json',
    'edges_partial': 'globomap_api/specs/edges_partial.json',
    'collections': 'globomap_api/specs/collections.json',
    'graphs': 'globomap_api/specs/graphs.json',
    'search': 'globomap_api/specs/search.json',
    'clear': 'globomap_api/specs/clear.json',
}

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True

ZABBIX_UI_URL = os.getenv('ZABBIX_UI_URL')
ZABBIX_API_URL = os.getenv('ZABBIX_API_URL')
ZABBIX_API_USER = os.getenv('ZABBIX_API_USER')
ZABBIX_API_PASSWORD = os.getenv('ZABBIX_API_PASSWORD')

# Redis
REDIS_SENTINEL_ENDPOINT_SIMPLE = os.getenv('REDIS_SENTINEL_ENDPOINT_SIMPLE')
REDIS_SENTINEL_SERVICE_NAME = os.getenv('REDIS_SENTINEL_SERVICE_NAME')
REDIS_SENTINEL_PASSWORD = os.getenv('REDIS_SENTINEL_PASSWORD')
REDIS_SENTINELS_PORT = os.getenv('REDIS_SENTINELS_PORT')
REDIS_SENTINELS = os.getenv('REDIS_SENTINELS')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

# Keystone
KEYSTONE_AUTH_ENABLE = os.getenv('KEYSTONE_AUTH_ENABLE')
KEYSTONE_AUTH_URL = os.getenv('KEYSTONE_AUTH_URL')
KEYSTONE_USERNAME = os.getenv('KEYSTONE_USERNAME')
KEYSTONE_PASSWORD = os.getenv('KEYSTONE_PASSWORD')
KEYSTONE_TENANT_NAME = os.getenv('KEYSTONE_TENANT_NAME')

ADMIN = 'globomap_admin'
READ = 'globomap_read'
WRITE = 'globomap_write'
COLLECTION = 'globomap_collection'
EDGE = 'globomap_edge'
GRAPH = 'globomap_graph'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'api': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'werkzeug': {'propagate': True},
    }
}
