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

from globomap_api import exceptions as gmap_exceptions
from globomap_api.app import create_app
from globomap_api.models.db import DB


class TestDB(unittest.TestCase):

    def setUp(self):
        self.app = create_app('tests.config')
        with self.app.app_context():
            self.db_inst = DB()
            self._cleanup()
            self.db_inst.get_database()

    def _cleanup(self):
        dbs = ['test_database']
        for db_name in dbs:
            try:
                self.db_inst.delete_database(db_name)
            except Exception:
                pass

    def test_get_database(self):
        """Test get database"""

        with self.app.app_context():
            db_name = 'test_database'
            self.db_inst.create_database(db_name)
            col = self.db_inst.get_database(db_name)

            self.assertEqual(col.name, db_name)

    def test_create_database(self):
        """Test create database"""

        with self.app.app_context():
            db_name = 'test_database'
            col = self.db_inst.create_database(db_name)

            self.assertEqual(col.name, db_name)

    def test_delete_database(self):
        """Test delete database"""

        with self.app.app_context():
            db_name = 'test_database'
            self.db_inst.create_database(db_name)
            self.db_inst.delete_database(db_name)

            with self.assertRaises(gmap_exceptions.DatabaseNotExist):
                self.db_inst.get_database(db_name)

    def test_create_db_duplicated(self):
        """Test if create db with duplicated name"""

        with self.app.app_context():
            db_name = 'test_database'
            self.db_inst.create_database(db_name)
            with self.assertRaises(gmap_exceptions.DatabaseAlreadyExist):
                self.db_inst.create_database(db_name)

    def test_delete_db_not_exists(self):
        """Test if delete db that not exists"""

        with self.app.app_context():
            db_name = 'test_database_not_exist'
            with self.assertRaises(gmap_exceptions.DatabaseNotExist):
                self.db_inst.delete_database(db_name)


if __name__ == '__main__':
    unittest.main()
