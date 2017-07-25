from arango import exceptions

from ..errors import errors


class Document:

    def __init__(self, collection):
        self.collection = collection

    def create_document(self, document):
        """Create Document"""

        try:
            self.collection.insert(document)

        except exceptions.DocumentInsertError as err:
            if errors.get(err.error_code):
                raise Exception(
                    errors.get(err.error_code).format(document['_key']))
            else:
                raise Exception(
                    errors.get(0).format(document['_key'], err.message))

    def upsert_document(self, document):
        """Create Document"""

        try:
            document = self.collection.update(document)
        except exceptions.DocumentUpdateError as err:
            if err.error_code == 1202:
                self.create_document(document)

            elif errors.get(err.error_code):
                raise Exception(
                    errors.get(err.error_code).format(document['_key']))
            else:
                raise Exception(
                    errors.get(0).format(document['_key'], err.message))
