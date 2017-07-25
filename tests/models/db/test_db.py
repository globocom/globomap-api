import os
import unittest

from globomap_api.app import create_app
from globomap_api.models.db import DB

dbs = ['test_db']


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.app = create_app('tests.config')
        with self.app.app_context():
            self.db_inst = DB()
            self.db_inst.get_db()

    def tearDown(self):
        for db in dbs:
            try:
                self.db_inst.delete_db(db)
            except Exception:
                pass

    def test_get_db(self):
        """Test get db"""

        db_name = 'test_db'
        self.db_inst.create_db(db_name)
        col = self.db_inst.get_db(db_name)
        self.assertEqual(col.name, db_name)

    def test_create_db(self):
        """Test create db"""

        db_name = 'test_db'
        self.db_inst.create_db(db_name)
        col = self.db_inst.get_db(db_name)
        self.assertEqual(col.name, db_name)

    def test_delete_db(self):
        """Test delete db"""

        db_name = 'test_db'
        self.db_inst.create_db(db_name)
        self.db_inst.delete_db(db_name)
        with self.assertRaises(Exception):
            self.db_inst.get_db(db_name)

    def test_create_db_duplicated(self):
        """Test if create db with duplicated name"""

        db_name = 'test_db'
        self.db_inst.create_db(db_name)
        with self.assertRaises(Exception):
            self.db_inst.create_db(db_name)

    def test_delete_db_not_exists(self):
        """Test if delete db that not exists"""

        db_name = 'test_db_2'
        with self.assertRaises(Exception):
            self.db_inst.delete_db(db_name)


if __name__ == '__main__':
    unittest.main()
