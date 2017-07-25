import os

import unittest2

from globomap_api.app import create_app
from globomap_api.models.db import DB

collections = [
    'test_collection_db',
    'test_collection_db_2',
    'test_edge_db',
    'test_edge_db_2',
]


class TestStringMethods(unittest2.TestCase):

    def setUp(self):
        self.app = create_app('tests.config')
        with self.app.app_context():
            self.db_inst = DB()
            self.db_inst.get_db()

    def tearDown(self):
        for collection in collections:
            try:
                self.db_inst.delete_collection(collection)
            except Exception:
                pass

    def test_get_collection(self):
        """Test get collection"""

        col_name = 'test_collection_db'
        self.db_inst.create_collection(col_name)
        col = self.db_inst.get_collection(col_name)
        self.assertEqual(col.name, col_name)

    def test_create_collection(self):
        """Test create collection"""

        col_name = 'test_collection_db_2'
        self.db_inst.create_collection(col_name)
        col = self.db_inst.get_collection(col_name)
        self.assertEqual(col.name, col_name)

    def test_create_edge(self):
        """Test create edge"""

        col_name = 'test_edge_db_2'
        self.db_inst.create_collection(col_name, edge=True)
        col = self.db_inst.get_collection(col_name)
        self.assertEqual(col.name, col_name)

    def test_delete_collection(self):
        """Test delete collection"""

        col_name = 'test_collection_db'
        self.db_inst.create_collection(col_name)
        self.db_inst.delete_collection(col_name)
        with self.assertRaises(Exception):
            self.db_inst.get_collection(col_name)

    def test_get_collection_not_exists(self):
        """Test if get collection that not exists"""

        col_name = 'test_collection_db_2'
        with self.assertRaises(Exception):
            self.db_inst.get_collection(col_name)

    def test_create_collection_duplicated(self):
        """Test if create collection with duplicated name"""

        col_name = 'test_collection_db'
        self.db_inst.create_collection(col_name)
        with self.assertRaises(Exception):
            self.db_inst.create_collection(col_name)

    def test_create_edge_duplicated(self):
        """Test if create edge with duplicated name"""

        col_name = 'test_edge_db_2'
        self.db_inst.create_collection(col_name, edge=True)
        with self.assertRaises(Exception):
            self.db_inst.create_collection(col_name, edge=True)

    def test_delete_collection_not_exists(self):
        """Test if delete collection that not exists"""

        col_name = 'test_collection_db_2'
        with self.assertRaises(Exception):
            self.db_inst.delete_collection(col_name)


if __name__ == '__main__':
    unittest2.main()
