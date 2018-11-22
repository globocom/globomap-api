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
from globomap_api.config import ADMIN
from globomap_api.config import API_PLUGINS_CONFIG_FILE
from globomap_api.config import ARANGO_DB
from globomap_api.config import ARANGO_HOST
from globomap_api.config import ARANGO_PASSWORD
from globomap_api.config import ARANGO_PORT
from globomap_api.config import ARANGO_PROTOCOL
from globomap_api.config import ARANGO_USERNAME
from globomap_api.config import COLLECTION
from globomap_api.config import EDGE
from globomap_api.config import GRAPH
from globomap_api.config import KEYSTONE_PASSWORD
from globomap_api.config import KEYSTONE_USERNAME
from globomap_api.config import META_COLLECTION
from globomap_api.config import META_GRAPH
from globomap_api.config import META_QUERY
from globomap_api.config import READ
from globomap_api.config import SPECS
from globomap_api.config import WRITE


__all__ = [
    'ADMIN', 'API_PLUGINS_CONFIG_FILE', 'ARANGO_DB', 'ARANGO_HOST',
    'ARANGO_PASSWORD', 'ARANGO_PORT', 'ARANGO_PROTOCOL', 'ARANGO_USERNAME',
    'COLLECTION', 'EDGE', 'GRAPH', 'KEYSTONE_PASSWORD', 'KEYSTONE_USERNAME',
    'META_COLLECTION', 'META_GRAPH', 'META_QUERY', 'READ', 'SPECS', 'WRITE',
    'ZABBIX_API_URL', 'ZABBIX_API_USER', 'ZABBIX_API_PASSWORD', 'ZABBIX_UI_URL',
    'LOGGING'
]


ZABBIX_API_URL = 'zabbix_api_url'
ZABBIX_API_USER = 'zabbix_api_user'
ZABBIX_API_PASSWORD = 'zabbix_api_password'
ZABBIX_UI_URL = 'zabbix_ui_url'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': 'level=%(levelname)s timestamp=%(asctime)s module=%(module)s line=%(lineno)d' +
            'message=%(message)s '
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'api': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
        'werkzeug': {'propagate': True},
    }
}
