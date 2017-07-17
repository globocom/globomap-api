import os

from flask import Flask


def create_app(config_module=None):
    app = Flask(__name__)
    app.config.from_object(config_module or
                           os.environ.get('FLASK_CONFIG') or
                           'config')

    from globomap_api.v1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/v1')
    return app
