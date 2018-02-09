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
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

ZABBIX_UI_URL = os.getenv('ZABBIX_UI_URL')
ZABBIX_API_URL = os.getenv('ZABBIX_API_URL')
ZABBIX_API_USER = os.getenv('ZABBIX_API_USER')
ZABBIX_API_PASSWORD = os.getenv('ZABBIX_API_PASSWORD')

REDIS_SENTINEL_ENDPOINT_SIMPLE = os.getenv('REDIS_SENTINEL_ENDPOINT_SIMPLE')
REDIS_SENTINEL_SERVICE_NAME = os.getenv('REDIS_SENTINEL_SERVICE_NAME')
REDIS_SENTINEL_PASSWORD = os.getenv('REDIS_SENTINEL_PASSWORD')
REDIS_SENTINELS = os.getenv('REDIS_SENTINELS')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'stdout': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/tmp/globomap.log',
            'mode': 'a',
        },
    },
    'loggers': {
        'globomap_api': {
            'handlers': ['log_file', 'stdout'],
            'level': 'DEBUG',
            'formatter': 'verbose',
        }
    }
}
