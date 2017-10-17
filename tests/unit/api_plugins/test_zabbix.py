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
import unittest2
from unittest.mock import patch, Mock
from globomap_api.api_plugins.zabbix import ZabbixPlugin


class TestZabbix(unittest2.TestCase):

    def setUp(self):
        patch('globomap_api.api_plugins.zabbix.os.getenv').start()
        self.hosts = {'result':[{'hostid': 1}]}
        self.triggers = {'result':[{'triggerid': 1, 'description': 'CPU 99%', 'value': 1}]}

    def test_get_triggers(self):
        self._mock_py_zabbix(self.hosts, self.triggers)
        response = ZabbixPlugin().get_data({'ips': '10.0.0.1'})

        self.assertEqual(1, len(response))
        self.assertEqual('CPU 99%', response[0]['key'])
        self.assertEqual(1, response[0]['value'])
        self.assertIsNotNone(response[0]['properties'])

    def test_get_triggers_given_no_ips_provided(self):
        try:
            ZabbixPlugin().get_data({})
        except Exception as e:
            self.assertEquals("The field 'ips' is required", str(e))

    def test_get_triggers_given_host_not_found(self):
        try:
            self._mock_py_zabbix({'result':[]})
            ZabbixPlugin().get_data({'ips': '10.0.0.1'})
        except Exception as e:
            self.assertEquals("No hosts were found for IPs ['10.0.0.1']", str(e))

    def test_get_triggers_given_triggers_not_found(self):
        self._mock_py_zabbix(self.hosts, {'result': []})
        response = ZabbixPlugin().get_data({'ips': '10.0.0.1'})

        self.assertEqual(0, len(response))

    def test_get_triggers_given_api_error(self):
        with self.assertRaises(ConnectionError):
            self._mock_py_zabbix(ConnectionError())
            ZabbixPlugin().get_data({'ips': '10.0.0.1'})

    def _mock_py_zabbix(self, hosts, triggers=None):
        py_zabbix_mock = patch('globomap_api.api_plugins.zabbix.ZabbixAPI').start()
        do_request_mock = Mock()
        do_request_mock.do_request.side_effect = [hosts, triggers]
        py_zabbix_mock.return_value = do_request_mock
        return py_zabbix_mock
