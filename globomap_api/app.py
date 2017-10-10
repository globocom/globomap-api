"""
   Copyright 2017 Globo.com

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

from flask import Blueprint
from flask import Flask
from flask import jsonify
from flask import request

from globomap_api import config
from globomap_api import exceptions
from globomap_api.v1 import api
from globomap_api.v1.endpoints.collections import ns as collections_namespace
from globomap_api.v1.endpoints.edges import ns as edges_namespace
from globomap_api.v1.endpoints.graphs import ns as graphs_namespace


def create_app(config_module=None):
    app = Flask(__name__)
    app.config.from_object(config_module or
                           os.environ.get('FLASK_CONFIG') or
                           'globomap_api.config')

    blueprint = Blueprint('api', __name__, url_prefix='/v1')

    api.init_app(blueprint)

    api.add_namespace(graphs_namespace)
    api.add_namespace(edges_namespace)
    api.add_namespace(collections_namespace)

    app.register_blueprint(blueprint)

    return app
