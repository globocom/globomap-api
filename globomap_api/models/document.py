"""
   Copyright 2018 Globo.com

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
from arango import exceptions
from flask import current_app as app

from globomap_api import exceptions as gmap_exceptions
from globomap_api.errors import DOCUMENT as doc_err


class Document:

    def __init__(self, collection):
        self.collection = collection

    def create_document(self, document):
        """Create Document"""

        try:
            return self.collection.insert(document)
        except exceptions.DocumentInsertError as err:

            if doc_err.get(err.error_code):
                if err.error_code == 1210:
                    app.logger.warning(err.message)
                    raise gmap_exceptions.DocumentAlreadyExist(
                        doc_err.get(err.error_code).format(document['_key']))
                else:
                    app.logger.error(err.message)
                    raise gmap_exceptions.DocumentException(
                        doc_err.get(err.error_code).format(document['_key']))

            else:
                raise gmap_exceptions.DocumentException(
                    doc_err.get(0).format(document['_key'], err.message))

        except Exception as err:
            app.logger.error(err.message)
            raise gmap_exceptions.DocumentException(
                doc_err.get(0).format(document['_key'], err.message))

    def update_document(self, document):
        """Update Document"""

        try:
            return self.collection.replace(document)
        except exceptions.DocumentReplaceError as err:
            if err.error_code == 1202:
                msg = 'There no document with key {}'.format(document['_key'])
                app.logger.warning(msg)
                raise gmap_exceptions.DocumentNotExist(msg)
            else:
                app.logger.error(err.message)
                raise gmap_exceptions.DocumentException(
                    doc_err.get(0).format(document['_key'], err.message))

        except Exception as err:
            app.logger.error(err.message)
            raise gmap_exceptions.DocumentException(
                doc_err.get(0).format(document['_key'], str(err)))

    def upsert_document(self, document):
        """Create/Update Document"""

        try:
            document = self.update_document(document)
        except gmap_exceptions.DocumentNotExist:
            document = self.create_document(document)
        else:
            return document

    def get_document(self, key):
        """Get Document"""

        try:
            document = self.collection.get(key)

        except Exception as err:
            app.logger.error(err.message)
            raise gmap_exceptions.DocumentException(
                doc_err.get(0).format(key, err.message))
        else:
            if document is None:
                msg = 'There no document with key {}'.format(key)
                app.logger.warning(msg)
                raise gmap_exceptions.DocumentNotExist(msg)

            return document

    def delete_document(self, key):
        """Delete Document"""

        try:
            self.collection.delete(key)
        except exceptions.DocumentDeleteError as err:

            if err.error_code == 1202:
                msg = 'There no document with key {}'.format(key)
                app.logger.warning(msg)
                raise gmap_exceptions.DocumentNotExist(msg)

            else:
                app.logger.error(err.message)
                raise gmap_exceptions.DocumentException(
                    doc_err.get(0).format(key, err.message))

        except Exception as err:
            app.logger.error(err.message)
            raise gmap_exceptions.DocumentException(
                doc_err.get(0).format(key, err.message))
        else:
            return True
