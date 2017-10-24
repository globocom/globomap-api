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
# -*- coding: utf-8 -*-
import logging

from flask import request
from flask_restplus import Resource

from globomap_api.api_plugins.abstract_plugin import PluginNotFoundException
from globomap_api.api_plugins.plugin_loader import ApiPluginLoader
from globomap_api.v1 import api


log = logging.getLogger(__name__)

ns = api.namespace('plugin_data', description='test')


@ns.route('/<plugin_name>/')
class PluginData(Resource):

    def get(self, plugin_name):
        try:
            plugin_instance = ApiPluginLoader().load_plugin(plugin_name)
            return plugin_instance.get_data(request.args), 200
        except PluginNotFoundException as err:
            api.abort(404, errors=str(err))
        except Exception as err:
            api.abort(500, errors=str(err))
