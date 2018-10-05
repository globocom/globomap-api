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

graphs = ['test_graph_db']


class TestGraph(unittest2.TestCase):

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

    def test_get_graph(self):
        """Test get graph"""

        graph_name = 'test_graph_db'
        self.db_inst.create_graph(graph_name)
        col = self.db_inst.get_graph(graph_name)
        self.assertEqual(col.name, graph_name)

    def test_create_graph_without_def(self):
        """Test create graph without def"""

        graph_name = 'test_graph_db'
        self.db_inst.create_graph(graph_name)
        col = self.db_inst.get_graph(graph_name)
        self.assertEqual(col.name, graph_name)
        self.assertEqual(col.name, graph_name)

    def test_create_graph_one_def(self):
        """Test create graph with one def """

        graph_name = 'test_graph_db'
        definitions = [{
            'edge': 'edge_test',
            'from_collections': ['coll_test'],
            'to_collections': ['coll_test']
        }]
        self.db_inst.create_graph(graph_name, definitions)
        col = self.db_inst.get_graph(graph_name)
        self.assertEqual(col.name, graph_name)
        self.assertEqual(col.name, graph_name)

    def test_create_graph_two_def(self):
        """Test create 2 graphs with def"""

        graph_name = 'test_graph_db'
        definitions = [{
            'edge': 'edge_test',
            'from_collections': ['coll_test'],
            'to_collections': ['coll_test']
        }, {
            'edge': 'edge_test2',
            'from_collections': ['coll_test2'],
            'to_collections': ['coll_test2']
        }]
        self.db_inst.create_graph(graph_name, definitions)
        col = self.db_inst.get_graph(graph_name)
        self.assertEqual(col.name, graph_name)

    def test_delete_graph(self):
        """Test delete graph"""

        graph_name = 'test_graph_db'
        self.db_inst.create_graph(graph_name)
        self.db_inst.delete_graph(graph_name)
        with self.assertRaises(gmap_exceptions.GraphNotExist):
            self.db_inst.get_graph(graph_name)

    def test_get_graph_not_exists(self):
        """Test if get graph that not exists"""

        graph_name = 'test_graph_db_2'
        with self.assertRaises(gmap_exceptions.GraphNotExist):
            self.db_inst.get_graph(graph_name)

    def test_create_graph_duplicated(self):
        """Test if create graph with duplicated name"""

        graph_name = 'test_graph_db'
        self.db_inst.create_graph(graph_name)
        with self.assertRaises(gmap_exceptions.GraphAlreadyExist):
            self.db_inst.create_graph(graph_name)

    def test_delete_graph_not_exists(self):
        """Test if delete graph that not exists"""

        graph_name = 'test_graph_db_2'
        with self.assertRaises(gmap_exceptions.GraphNotExist):
            self.db_inst.delete_graph(graph_name)
