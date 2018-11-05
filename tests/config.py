ARANGO_DB = '_system'
ARANGO_USERNAME = 'root'
ARANGO_PASSWORD = ''
ARANGO_PROTOCOL = 'http'
ARANGO_HOST = 'globomap_db'
ARANGO_PORT = '8529'

API_PLUGINS_CONFIG_FILE = 'api_plugins'

ZABBIX_API_URL = 'zabbix_api_url'
ZABBIX_API_USER = 'zabbix_api_user'
ZABBIX_API_PASSWORD = 'zabbix_api_password'
ZABBIX_UI_URL = 'zabbix_ui_url'

SPECS = {
    'auth': 'globomap_api/specs/auth.json',
    'documents': 'globomap_api/specs/documents.json',
    'edges': 'globomap_api/specs/edges.json',
    'documents_partial': 'globomap_api/specs/documents_partial.json',
    'edges_partial': 'globomap_api/specs/edges_partial.json',
    'collections': 'globomap_api/specs/collections.json',
    'graphs': 'globomap_api/specs/graphs.json',
    'search': 'globomap_api/specs/search.json',
    'clear': 'globomap_api/specs/clear.json',
    'queries': 'globomap_api/specs/queries.json',
}

# Keystone
KEYSTONE_USERNAME = 'u_globomap_api'
KEYSTONE_PASSWORD = 'u_globomap_api'

# Roles
ADMIN = 'globomap_admin'
READ = 'globomap_read'
WRITE = 'globomap_write'
COLLECTION = 'globomap_collection'
EDGE = 'globomap_edge'
GRAPH = 'globomap_graph'

# Meta Collections
META_COLLECTION = 'meta_collection'
META_GRAPH = 'meta_graph'
META_QUERY = 'meta_query'

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
