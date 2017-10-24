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
import json

import unittest2
from unittest.mock import patch, Mock
from globomap_api.app import create_app


class TestPluginData(unittest2.TestCase):

    def setUp(self):
        patch('globomap_api.api_plugins.zabbix.os.getenv').start()
        self.app = create_app('tests.config')
        self.client = self.app.test_client()

        self.hosts = {'result': [{'hostid': 1}]}
        self.triggers = {'result': [{'triggerid': 1, 'description': 'CPU 99%', 'value': 1}]}

    def test_get_zabbix_data(self):
        self._mock_zabbix_api(self.hosts, self.triggers)
        response = self._get('/v1/plugin_data/zabbix?ips=10.132.41.183')
        json_response = json.loads(response.data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(json_response))
        self.assertEqual('CPU 99%', json_response[0]['key'])
        self.assertEqual(1, json_response[0]['value'])

    def test_error_response(self):
        self._mock_zabbix_api(Exception('Error'))
        response = self._get('/v1/plugin_data/zabbix?ips=10.132.41.183')
        json_response = json.loads(response.data)

        self.assertEqual(500, response.status_code)
        self.assertEqual('Error', json_response['errors'])

    def test_get_data_from_invalid_plugin(self):
        response = self._get('/v1/plugin_data/UNKNOW?ips=10.132.41.183')
        json_response = json.loads(response.data)

        self.assertEqual(404, response.status_code)
        self.assertEqual('Plugin UNKNOW not found', json_response['errors'])

    def _get(self, uri):
        return self.client.get(uri, follow_redirects=True)

    def _mock_zabbix_api(self, hosts, triggers=None):
        py_zabbix_mock = patch('globomap_api.api_plugins.zabbix.ZabbixAPI').start()
        do_request_mock = Mock()
        do_request_mock.do_request.side_effect = [hosts, triggers]
        py_zabbix_mock.return_value = do_request_mock
        return py_zabbix_mock
