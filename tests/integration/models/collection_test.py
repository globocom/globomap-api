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

from globomap_api import exceptions as gmap_exceptions
from globomap_api.app import create_app
from globomap_api.models.db import DB


class TestCollection(unittest2.TestCase):

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

    ##############
    # COLLECTION #
    ##############
    def test_get_collection(self):
        """Test get collection"""

        with self.app.app_context():
            col_name = 'get_collection'
            self.db_inst.create_collection(col_name)

            col = self.db_inst.get_collection(col_name)
            self.assertEqual(col.name, col_name)

    def test_create_collection(self):
        """Test create collection"""

        with self.app.app_context():
            col_name = 'create_collection'
            self.db_inst.create_collection(col_name)
            col = self.db_inst.get_collection(col_name)
            self.assertEqual(col.name, col_name)

    def test_delete_collection(self):
        """Test delete collection"""

        with self.app.app_context():
            col_name = 'delete_collection'
            self.db_inst.create_collection(col_name)
            self.db_inst.delete_collection(col_name)
            with self.assertRaises(gmap_exceptions.CollectionNotExist):
                self.db_inst.get_collection(col_name)

    def test_get_collection_not_exists(self):
        """Test if get collection not exists"""

        with self.app.app_context():
            col_name = 'collection_not_exist'
            with self.assertRaises(gmap_exceptions.CollectionNotExist):
                self.db_inst.get_collection(col_name)

    def test_create_collection_duplicated(self):
        """Test if create collection with duplicated name"""

        with self.app.app_context():
            col_name = 'collection_duplicated'
            self.db_inst.create_collection(col_name)
            with self.assertRaises(gmap_exceptions.CollectionAlreadyExist):
                self.db_inst.create_collection(col_name)

    def test_delete_collection_not_exists(self):
        """Test if delete collection not exists"""

        with self.app.app_context():
            col_name = 'collection_not_exist'
            with self.assertRaises(gmap_exceptions.CollectionNotExist):
                self.db_inst.delete_collection(col_name)

    #########
    # EDGES #
    #########
    def test_get_edge(self):
        """Test get edge"""

        with self.app.app_context():
            col_name = 'get_edge'
            self.db_inst.create_edge(col_name)

            col = self.db_inst.get_edge(col_name)
            self.assertEqual(col.name, col_name)

    def test_create_edge(self):
        """Test create edge"""

        with self.app.app_context():
            col_name = 'create_edge'
            self.db_inst.create_edge(col_name)
            col = self.db_inst.get_edge(col_name)
            self.assertEqual(col.name, col_name)

    def test_delete_edge(self):
        """Test delete edge"""

        with self.app.app_context():
            col_name = 'delete_edge'
            self.db_inst.create_edge(col_name)
            self.db_inst.delete_edge(col_name)
            with self.assertRaises(gmap_exceptions.EdgeNotExist):
                self.db_inst.get_edge(col_name)

    def test_get_edge_not_exists(self):
        """Test if get edge not exists"""

        with self.app.app_context():
            col_name = 'edge_not_exist'
            with self.assertRaises(gmap_exceptions.EdgeNotExist):
                self.db_inst.get_edge(col_name)

    def test_create_edge_duplicated(self):
        """Test if create edge with duplicated name"""

        with self.app.app_context():
            col_name = 'edge_duplicated'
            self.db_inst.create_edge(col_name)
            with self.assertRaises(gmap_exceptions.EdgeAlreadyExist):
                self.db_inst.create_edge(col_name)

    def test_delete_edge_not_exists(self):
        """Test if delete edge not exists"""

        with self.app.app_context():
            col_name = 'edge_not_exist'
            with self.assertRaises(gmap_exceptions.EdgeNotExist):
                self.db_inst.delete_edge(col_name)
