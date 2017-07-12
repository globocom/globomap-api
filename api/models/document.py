from arango import exceptions
from errors import errors


class Document:

    def __init__(self, collection):
        self.collection = collection

    def create_document(self, document):
        """Create Document"""

        try:
            document = self.collection.insert(document)

        except exceptions.DocumentInsertError as err:
            if errors.get(err.error_code):
                raise Exception(
                    errors.get(err.error_code).format(document['_key']))
            else:
                raise Exception(
                    errors.get(0).format(document['_key'], err.message))
