import os

import unittest2

from globomap_api import exceptions as gmap_exceptions
from globomap_api.app import create_app
from globomap_api.models.db import DB


class TestCollection(unittest2.TestCase):

    def setUp(self):
        self.app = create_app('tests.config')
        self.db_name = self.app.config['ARANGO_DB']
        with self.app.app_context():
            self.db_inst = DB()
            self._cleanup()
            self.db_inst.get_database()

    def _cleanup(self):
        try:
            self.db_inst.delete_database(self.db_name)
        except Exception:
            pass
        finally:
            self.db_inst.create_database(self.db_name)

    ##############
    # COLLECTION #
    ##############
    def test_get_collection(self):
        """Test get collection"""

        col_name = 'get_collection'
        self.db_inst.create_collection(col_name)

        col = self.db_inst.get_collection(col_name)
        self.assertEqual(col.name, col_name)

    def test_create_collection(self):
        """Test create collection"""

        col_name = 'create_collection'
        self.db_inst.create_collection(col_name)
        col = self.db_inst.get_collection(col_name)
        self.assertEqual(col.name, col_name)

    def test_delete_collection(self):
        """Test delete collection"""

        col_name = 'delete_collection'
        self.db_inst.create_collection(col_name)
        self.db_inst.delete_collection(col_name)
        with self.assertRaises(gmap_exceptions.CollectionNotExist):
            self.db_inst.get_collection(col_name)

    def test_get_collection_not_exists(self):
        """Test if get collection not exists"""

        col_name = 'collection_not_exist'
        with self.assertRaises(gmap_exceptions.CollectionNotExist):
            self.db_inst.get_collection(col_name)

    def test_create_collection_duplicated(self):
        """Test if create collection with duplicated name"""

        col_name = 'collection_duplicated'
        self.db_inst.create_collection(col_name)
        with self.assertRaises(gmap_exceptions.CollectionAlreadyExist):
            self.db_inst.create_collection(col_name)

    def test_delete_collection_not_exists(self):
        """Test if delete collection not exists"""

        col_name = 'collection_not_exist'
        with self.assertRaises(gmap_exceptions.CollectionNotExist):
            self.db_inst.delete_collection(col_name)

    #########
    # EDGES #
    #########
    def test_get_edge(self):
        """Test get edge"""

        col_name = 'get_edge'
        self.db_inst.create_edge(col_name)

        col = self.db_inst.get_edge(col_name)
        self.assertEqual(col.name, col_name)

    def test_create_edge(self):
        """Test create edge"""

        col_name = 'create_edge'
        self.db_inst.create_edge(col_name)
        col = self.db_inst.get_edge(col_name)
        self.assertEqual(col.name, col_name)

    def test_delete_edge(self):
        """Test delete edge"""

        col_name = 'delete_edge'
        self.db_inst.create_edge(col_name)
        self.db_inst.delete_edge(col_name)
        with self.assertRaises(gmap_exceptions.EdgeNotExist):
            self.db_inst.get_edge(col_name)

    def test_get_edge_not_exists(self):
        """Test if get edge not exists"""

        col_name = 'edge_not_exist'
        with self.assertRaises(gmap_exceptions.EdgeNotExist):
            self.db_inst.get_edge(col_name)

    def test_create_edge_duplicated(self):
        """Test if create edge with duplicated name"""

        col_name = 'edge_duplicated'
        self.db_inst.create_edge(col_name)
        with self.assertRaises(gmap_exceptions.EdgeAlreadyExist):
            self.db_inst.create_edge(col_name)

    def test_delete_edge_not_exists(self):
        """Test if delete edge not exists"""

        col_name = 'edge_not_exist'
        with self.assertRaises(gmap_exceptions.EdgeNotExist):
            self.db_inst.delete_edge(col_name)


if __name__ == '__main__':
    unittest2.main()
