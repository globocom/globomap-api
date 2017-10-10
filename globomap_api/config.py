import os

ARANGO_DB = os.getenv('ARANGO_DB')
ARANGO_USERNAME = os.getenv('ARANGO_USERNAME')
ARANGO_PASSWORD = os.getenv('ARANGO_PASSWORD')
ARANGO_PROTOCOL = os.getenv('ARANGO_PROTOCOL')
ARANGO_HOST = os.getenv('ARANGO_HOST')
ARANGO_PORT = os.getenv('ARANGO_PORT')
FLASK_DEBUG = os.getenv('FLASK_DEBUG', False)
SPECS = {
    'documents': 'globomap_api/specs/documents.json',
    'edges': 'globomap_api/specs/edges.json',
    'documents_partial': 'globomap_api/specs/documents_partial.json',
    'edges_partial': 'globomap_api/specs/edges_partial.json',
    'collections': 'globomap_api/specs/collections.json',
    'graphs': 'globomap_api/specs/graphs.json',
    'search': 'globomap_api/specs/search.json',
}

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False
