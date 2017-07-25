import os

import unittest2

from globomap_api.app import create_app
from globomap_api.models.db import DB

collections = [
    'test_collection_db'
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

    def test_search_document(self):
        """Test search document by property"""

        col_name = 'test_collection_db'
        self.db_inst.create_collection(col_name)
        self.db_inst.database.collection(col_name).import_bulk([
            {'_key': 'doc04', 'value': 1},
            {'_key': 'doc05', 'value': 1},
            {'_key': 'doc06', 'value': 3},
        ])
        docs = self.db_inst.search_document(col_name, 'value', '1')
        docs = (set(sorted([d['_key'] for d in docs])))
        self.assertEqual(docs, {'doc04', 'doc05'})


if __name__ == '__main__':
    unittest2.main()
