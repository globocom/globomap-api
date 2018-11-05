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
import base64
import logging
import shutil
from os import remove
from time import time

import requests
from flask import current_app as app
from flask import send_file
from pyzabbix import ZabbixAPI

from globomap_api.api_plugins.abstract_plugin import AbstractPlugin
from globomap_api.api_plugins.abstract_plugin import PluginError


class ZabbixPlugin(AbstractPlugin):

    logger = logging.getLogger(__name__)

    def __init__(self):
        url = app.config['ZABBIX_API_URL']
        if not url:
            self.logger.error('Zabbix endpoint is not set')
            raise Exception('Invalid plugin configuration')

        user = app.config['ZABBIX_API_USER']
        if not user:
            self.logger.error('Zabbix user is not set')
            raise Exception('Invalid plugin configuration')

        password = app.config['ZABBIX_API_PASSWORD']
        if not password:
            self.logger.error('Zabbix password is not set')
            raise Exception('Invalid plugin configuration')

        if not app.config['ZABBIX_UI_URL']:
            self.logger.error('Zabbix Ui is not set')
            raise Exception('Invalid plugin configuration')

        self.zabbix = ZabbixAPI(url=url, user=user, password=password)

    def get_data(self, params):
        ips = params.get('ips')
        graphid = params.get('graphid')
        encoded = params.get('encoded')
        if ips:
            return self.get_trigger(ips)
        elif graphid:
            return self.get_graph(graphid, encoded)
        else:
            raise PluginError("The field 'ips' or 'graphid' is required")

    def get_trigger(self, ips):
        try:
            ips = ips.split(',')

            hosts = self.zabbix.do_request('host.get', {
                'output': ['hostid'],
                'search': {'ip': ips},
                'searchByAny': 1
            })

            if hosts['result']:
                hostIds = [host['hostid'] for host in hosts['result']]

                triggers = self.zabbix.do_request('trigger.get', {
                    'output': ['description', 'status', 'state', 'value'],
                    'filter': {'hostid': hostIds},
                    'expandDescription': 1
                })

                if triggers['result']:
                    return self.format_response(triggers)
                else:
                    return []
            else:
                raise PluginError(
                    'No hosts were found for IPs {}'.format(ips)
                )
        except:
            logging.exception('Zabbix API error')
            raise

    def format_response(self, triggers):
        response = []
        for trigger in triggers['result']:
            response.append(
                {
                    'key': trigger['description'],
                    'value': trigger['value'],
                    'properties': trigger
                }
            )
        return response

    def get_graph(self, graphid, encoded=False):
        with requests.Session() as s:
            data = {
                'password': app.config['ZABBIX_API_PASSWORD'],
                'name': app.config['ZABBIX_API_USER'],
                'enter': 'Sign in'
            }
            url = '{}/index.php'.format(app.config['ZABBIX_UI_URL'])
            res = s.post(url, data=data, verify=False)
            url = '{}/chart2.php?graphid={}'.format(app.config['ZABBIX_UI_URL'],
                                                    graphid)
            res = s.get(url, verify=False, stream=True)
            if res.status_code == 200:
                name = '/tmp/{}_{}.png'.format(graphid, time())
                with open(name, 'wb') as out_file:
                    shutil.copyfileobj(res.raw, out_file)

                if encoded:
                    return self._get_base64(name)
                else:
                    return self._get_image(name)

            raise PluginError('Cannot get graph')

    def _get_base64(self, name):
        with open(name, 'rb') as f:
            encodedZip = base64.b64encode(f.read())
            return encodedZip.decode()

    def _get_image(self, name):
        try:
            data = send_file(name, mimetype='image/png')
        except:
            raise PluginError('Cannot get graph')
        finally:
            remove(name)
        return data
