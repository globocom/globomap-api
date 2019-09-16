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
import configparser

from flask import current_app as app
from flask import request
from flask_restplus import Resource

from globomap_api.api.v2 import api
from globomap_api.api.v2.auth import permissions
from globomap_api.api.v2.auth.decorators import permission_classes
from globomap_api.api_plugins.abstract_plugin import PluginError
from globomap_api.api_plugins.abstract_plugin import PluginNotFoundException
from globomap_api.api_plugins.plugin_loader import ApiPluginLoader

ns = api.namespace('plugins', description='Plugins')


@ns.route('/')
@api.header(
    'Authorization',
    'Token Authorization',
    required=True,
    default='Token token='
)
class Plugins(Resource):

    @api.doc(responses={
        200: 'Success',
        401: 'Unauthorized',
        403: 'Forbidden'
    })
    @permission_classes((permissions.Read,))
    def get(self):
        try:
            plugins_config = configparser.ConfigParser()
            plugins_config.read(app.config['API_PLUGINS_CONFIG_FILE'])
            keys = plugins_config.sections()
            plugins = {}

            for key in keys:
                plugins[key] = {
                    'types': plugins_config.get(key, 'types'),
                    'parameters': plugins_config.get(key, 'parameters'),
                    'description': plugins_config.get(key, 'description'),
                    'uri': '{}{}/{}/'.format(api.base_url, 'plugins', key)
                }

            return plugins
        except Exception:
            err_msg = 'Error in plugin'
            app.logger.exception(err_msg)
            api.abort(500, errors=err_msg)


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
    @permission_classes((permissions.Read,))
    def get(self, plugin_name):
        try:
            query_string = request.query_string.decode("utf-8")
            query_list = []
            if query_string:
                query_list = query_string.split('&')
            args = {}

            for item in query_list:
                item_list = item.split('=')
                args[item_list[0]] = item_list[1]

            plugin_instance = ApiPluginLoader().load_plugin(plugin_name)
            data = plugin_instance.get_data(args)
            return data
        except PluginNotFoundException as err:
            app.logger.error(str(err))
            api.abort(404, errors=str(err))
            return data
        except PluginError as err:
            app.logger.error(str(err))
            api.abort(400, errors=str(err))
            return data
        except Exception:
            err_msg = 'Error in plugin'
            app.logger.exception(err_msg)
            api.abort(500, errors=err_msg)
