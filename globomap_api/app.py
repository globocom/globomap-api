import os

from flask import Flask
from flask_cors import CORS
from flask_cors import cross_origin


def create_app(config_module=None):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_module or
                           os.environ.get('FLASK_CONFIG') or
                           'globomap_api.config')

    from globomap_api.v1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/v1')
    return app
