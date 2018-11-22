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
import json

import unittest2

from globomap_api.app import create_app
from tests.integration.cleanup import cleanup


def login_user(self):
    return self.client.post(
        '/v2/auth/',
        data=json.dumps(dict(
            username='u_globomap_api',
            password='u_globomap_api'
        )),
        content_type='application/json'
    )


class CollectionsTestCase(unittest2.TestCase):

    def setUp(self):
        self.app = create_app('tests.config')
        self.client = self.app.test_client()

    @classmethod
    def setUpClass(cls):
        cleanup()

    @classmethod
    def tearDownClass(cls):
        cleanup()

    def test_order1(self):
        """Test list collections empty"""

        login_response = login_user(self)
        response = self.client.get(
            '/v2/collections/',
            headers=dict(
                Authorization='Token token=' + json.loads(
                    login_response.data.decode()
                ).get('token')
            )
        )
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(data['collections'], [])

    def test_order2(self):
        """Test create collection"""

        login_response = login_user(self)
        data = dict(
            name='coll',
            icon='coll_icon',
            description='Test Coll',
            alias='Collection',
            users=['user_abc'],
        )
        response = self.client.post(
            '/v2/collections/',
            json=data,
            headers=dict(
                Authorization='Token token=' + json.loads(
                    login_response.data.decode()
                ).get('token')
            )
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())

    def test_order3(self):
        """Test list collections again"""

        login_response = login_user(self)
        response = self.client.get(
            '/v2/collections/',
            headers=dict(
                Authorization='Token token=' + json.loads(
                    login_response.data.decode()
                ).get('token')
            )
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        collections = [
            {
                'alias': 'Collection',
                'name': 'coll',
                'kind': 'document',
                'icon': 'coll_icon',
                'description': 'Test Coll',
                'users': ['user_abc']
            }
        ]
        self.assertListEqual(data['collections'], collections)
