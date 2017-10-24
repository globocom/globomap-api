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
import logging
import os
from pyzabbix import ZabbixAPI
from globomap_api.api_plugins.abstract_plugin import AbstractPlugin


class ZabbixPlugin(AbstractPlugin):

    logger = logging.getLogger(__name__)

    def __init__(self):
        url = os.getenv('ZABBIX_API_URL')
        if not url:
            self.logger.error('Zabbix endpoint is not set')
            raise Exception('Invalid plugin configuration')
        user = os.getenv('ZABBIX_API_USER')
        if not url:
            self.logger.error('Zabbix user is not set')
            raise Exception('Invalid plugin configuration')
        password = os.getenv('ZABBIX_API_PASSWORD')
        if not url:
            self.logger.error('Zabbix password is not set')
            raise Exception('Invalid plugin configuration')

        self.zabbix = ZabbixAPI(url=url, user=user, password=password)

    def get_data(self, params):
        ips = params.get('ips')
        if not ips:
            raise Exception("The field 'ips' is required")

        try:
            ips = ips.split(',')

            hosts = self.zabbix.do_request('host.get', {
                "output": ['hostid'],
                'search': {'ip': ips},
                'searchByAny': 1
            })

            if hosts['result']:
                hostIds = [host['hostid'] for host in hosts['result']]

                triggers = self.zabbix.do_request('trigger.get', {
                    "output": ["description", "status", "state", "value"],
                    "filter": {"hostid": hostIds},
                    "expandDescription": 1
                })

                if triggers['result']:
                    return self.format_response(triggers)
                else:
                    return []
            else:
                raise Exception(
                    "No hosts were found for IPs {}".format(ips)
                )
        except:
            logging.exception("Zabbix API error")
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
