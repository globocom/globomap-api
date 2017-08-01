import os
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

        db_name = 'test_database'
        self.db_inst.create_database(db_name)
        col = self.db_inst.get_database(db_name)

        self.assertEqual(col.name, db_name)

    def test_create_database(self):
        """Test create database"""

        db_name = 'test_database'
        col = self.db_inst.create_database(db_name)

        self.assertEqual(col.name, db_name)

    def test_delete_database(self):
        """Test delete database"""

        db_name = 'test_database'
        self.db_inst.create_database(db_name)
        self.db_inst.delete_database(db_name)

        with self.assertRaises(gmap_exceptions.DatabaseNotExist):
            self.db_inst.get_database(db_name)

    def test_create_db_duplicated(self):
        """Test if create db with duplicated name"""

        db_name = 'test_database'
        self.db_inst.create_database(db_name)
        with self.assertRaises(gmap_exceptions.DatabaseAlreadyExist):
            self.db_inst.create_database(db_name)

    def test_delete_db_not_exists(self):
        """Test if delete db that not exists"""

        db_name = 'test_database_not_exist'
        with self.assertRaises(gmap_exceptions.DatabaseNotExist):
            self.db_inst.delete_database(db_name)


if __name__ == '__main__':
    unittest.main()
