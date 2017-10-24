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
import configparser
import importlib
import logging
from globomap_api.api_plugins.abstract_plugin import PluginNotFoundException
from flask import current_app as app


class ApiPluginLoader(object):

    logger = logging.getLogger(__name__)

    def load_plugin(self, plugin_name):
        plugins_config = configparser.ConfigParser()
        plugins_config.read(app.config['API_PLUGINS_CONFIG_FILE'])

        if not plugins_config.has_section(plugin_name):
            raise PluginNotFoundException(
                'Plugin {} not found'.format(plugin_name)
            )

        try:
            plugin_desc = plugins_config.get(plugin_name, 'description')
            plugin_module = plugins_config.get(plugin_name, 'module')
            self.logger.debug("Lading '{}'".format(plugin_desc))
            return self.create_plugin_instance(plugin_module)
        except:
            logging.exception("Error loading api plugin")
            raise PluginNotFoundException(
                "It was not possible to load plugin {}".format(plugin_name)
            )

    def create_plugin_instance(self, class_path):
        components = class_path.split('.')
        class_name = components[-1]
        package_path = ".".join(components[0:-1])
        plugin_class = getattr(
            importlib.import_module(package_path), class_name
        )
        return plugin_class()
