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
import binascii
import os
from logging import config

from flask import Flask
from flask_cors import CORS

from globomap_api import config as app_config
from globomap_api.api.v2.api import blueprint as api_v2
from globomap_api.models.db import DB


def create_app(config_module=None):
    app = Flask(__name__)
    app.secret_key = binascii.hexlify(os.urandom(24))
    app.config.from_object(config_module or os.environ.get('FLASK_CONFIG') or
                           'globomap_api.config')
    app.config['LOGGER_HANDLER_POLICY'] = 'default'
    app.config['LOGGER_NAME'] = 'api'
    app.config['BUNDLE_ERRORS'] = True
    app.config['RESTPLUS_VALIDATE'] = True

    app.logger
    config.dictConfig(app_config.LOGGING)

    app.config['ARANGO_CONN'] = DB(app_config)

    app.register_blueprint(api_v2)

    CORS(app, resources={
        r'/v2/*': {'origins': app_config.CORS}})

    return app
