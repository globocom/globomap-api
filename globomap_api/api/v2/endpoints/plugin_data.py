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
import logging

from flask import request
from flask_restplus import Resource

from globomap_api.api.parsers import plugin_arguments
from globomap_api.api.v2 import api
from globomap_api.api.v2 import permissions
from globomap_api.api.v2.decorators import permission_classes
from globomap_api.api_plugins.abstract_plugin import PluginNotFoundException
from globomap_api.api_plugins.plugin_loader import ApiPluginLoader

logger = logging.getLogger(__name__)
ns = api.namespace('plugin_data', description='Plugins')


@ns.route('/<plugin_name>/')
@api.doc(params={'plugin_name': 'Name Of Plugin'})
@api.header(
    'Authorization',
    'Token Authorization',
    required=True,
    default='Token token='
)
class PluginData(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found'
    })
    @api.expect(plugin_arguments)
    @permission_classes((permissions.Read))
    def get(self, plugin_name):
        try:
            args = plugin_arguments.parse_args(request)
            plugin_instance = ApiPluginLoader().load_plugin(plugin_name)
            data = plugin_instance.get_data(args)
            return data
        except PluginNotFoundException as err:
            api.abort(404, errors=str(err))
            return data
        except:
            err_msg = 'Error in plugin'
            logger.exception(err_msg)
            api.abort(400, errors=err_msg)
