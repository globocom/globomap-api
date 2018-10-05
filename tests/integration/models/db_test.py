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
import unittest

from globomap_api.app import create_app
from globomap_api.models.db import DB


class TestDB(unittest.TestCase):

    def setUp(self):
        self.app = create_app('tests.config')
        self.db_inst = DB(self.app.config)

        self.conn_db()
        self.cleanup()
        self.db_inst.database.create_database('test')

        self.db_inst.conn_database('test')

    def tearDown(self):
        self.conn_db()
        self.cleanup()

    def conn_db(self):
        db_name = self.app.config['ARANGO_DB']
        self.db_inst.conn_database(db_name)

    def cleanup(self):
        try:
            self.db_inst.database.delete_database('test')
        except:
            pass

    def test_get_database(self):
        """Test get database"""

        col = self.db_inst.get_database('test')
        self.assertEqual(col.name, 'test')
