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
from globomap_api.models.document import Document


class TestDocument(unittest2.TestCase):

    def setUp(self):
        self.app = create_app('tests.config')
        self.db_inst = DB(self.app.config)

        self.conn_db()
        self.cleanup()
        self.db_inst.database.create_database('test')

        self.db_inst.conn_database('test')
        self.db_inst.database.create_collection('test_collection_db')
        self.db_inst.get_collection('test_collection_db')

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

    def test_search_document(self):
        """Test search document by property"""

        with self.app.app_context():
            col_name = 'test_collection_db'
            self._import_bulk(col_name)
            search = [[{'field': 'value', 'operator': '==', 'value': 1}]]
            docs = self.db_inst.search_in_collection(
                'test_collection_db', search)
            docs = (set(sorted([d['_key'] for d in docs])))

            self.assertEqual(docs, {'doc04', 'doc05'})

    def test_get_document(self):
        """Test get document"""

        with self.app.app_context():
            self._import_bulk('test_collection_db')
            inst_doc = Document(self.db_inst.collection)
            doc = inst_doc.get_document('doc04')
            doc = {'_key': doc['_key'], 'value': doc['value'], }

            self.assertDictEqual(doc, {'_key': 'doc04', 'value': 1})

    def test_create_document(self):
        """Test create document"""

        with self.app.app_context():
            inst_doc = Document(self.db_inst.collection)
            doc = inst_doc.create_document({'_key': 'doc04', 'value': 1})
            doc = {'_key': doc['_key'], '_id': doc['_id'], }

            self.assertDictEqual(
                doc, {'_key': 'doc04', '_id': 'test_collection_db/doc04', })

    def test_get_document_not_exist(self):
        """Test get document not existing"""

        with self.app.app_context():
            inst_doc = Document(self.db_inst.collection)

            with self.assertRaises(gmap_exceptions.DocumentNotExist):
                inst_doc.get_document('doc04')

    def test_delete_document(self):
        """Test delete document"""

        with self.app.app_context():
            col_name = 'test_collection_db'
            self._import_bulk(col_name)

            inst_doc = Document(self.db_inst.collection)
            inst_doc.delete_document('doc04')

            with self.assertRaises(gmap_exceptions.DocumentNotExist):
                inst_doc.get_document('doc04')

    def test_delete_document_not_exist(self):
        """Test delee document not existing"""

        with self.app.app_context():
            inst_doc = Document(self.db_inst.collection)

            with self.assertRaises(gmap_exceptions.DocumentNotExist):
                inst_doc.delete_document('doc04')

    def _import_bulk(self, col_name):
        collection = self.db_inst.database.collection(col_name)
        collection.import_bulk([
            {'_key': 'doc04', 'value': 1},
            {'_key': 'doc05', 'value': 1},
            {'_key': 'doc06', 'value': 3},
        ])
