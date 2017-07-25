import os

import unittest2

from globomap_api.app import create_app
from globomap_api.models.db import DB

graphs = ['test_graph_db']


class TestStringMethods(unittest2.TestCase):

    def setUp(self):
        self.app = create_app('tests.config')
        with self.app.app_context():
            self.db_inst = DB()
            self.db_inst.get_db()

    def tearDown(self):
        for graph in graphs:
            try:
                self.db_inst.delete_graph(graph)
            except Exception:
                pass

    def test_get_graph(self):
        """Test get graph"""

        graph_name = 'test_graph_db'
        self.db_inst.create_graph(graph_name)
        col = self.db_inst.get_graph(graph_name)
        self.assertEqual(col.name, graph_name)

    def test_create_graph_without_def(self):
        """Test create graph"""

        graph_name = 'test_graph_db'
        self.db_inst.create_graph(graph_name)
        col = self.db_inst.get_graph(graph_name)
        self.assertEqual(col.name, graph_name)
        self.assertEqual(col.name, graph_name)

    def test_create_graph_one_def(self):
        """Test create graph"""

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
        """Test create graph"""

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
        with self.assertRaises(Exception):
            self.db_inst.get_graph(graph_name)

    def test_get_graph_not_exists(self):
        """Test if get graph that not exists"""

        graph_name = 'test_graph_db_2'
        with self.assertRaises(Exception):
            self.db_inst.get_graph(graph_name)

    def test_create_graph_duplicated(self):
        """Test if create graph with duplicated name"""

        graph_name = 'test_graph_db'
        self.db_inst.create_graph(graph_name)
        with self.assertRaises(Exception):
            self.db_inst.create_graph(graph_name)

    def test_delete_graph_not_exists(self):
        """Test if delete graph that not exists"""

        graph_name = 'test_graph_db_2'
        with self.assertRaises(Exception):
            self.db_inst.delete_graph(graph_name)


if __name__ == '__main__':
    unittest2.main()
