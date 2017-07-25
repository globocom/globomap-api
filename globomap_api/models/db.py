import os

from arango import ArangoClient
from arango import exceptions
from arango.aql import AQL
from flask import current_app as app


class DB(object):

    """DB"""

    collection = None
    database = None
    graph = None
    conn = None

    def __init__(self):

        self._connection()

    def _connection(self):

        self.username = app.config['ARANGO_USERNAME']
        self.password = app.config['ARANGO_PASSWORD']
        self.arango_protocol = app.config['ARANGO_PROTOCOL']
        self.arango_host = app.config['ARANGO_HOST']
        self.arango_port = app.config['ARANGO_PORT']

        self._conn = ArangoClient(
            protocol=self.arango_protocol,
            host=self.arango_host,
            port=self.arango_port,
            username=self.username,
            password=self.password,
            enable_logging=True
        )

    def has_database(self, name=''):
        """Return True if there database"""

        try:
            database = self._conn.database(name)
            database.properties()

        except exceptions.DatabasePropertiesError:
            return False

        else:
            return True

    def has_collection(self, name=''):
        """Return True if there collection"""

        try:
            collection = self.database.collection(name)
            collection.properties()

        except exceptions.CollectionPropertiesError:
            return False

        else:
            return True

    def has_graph(self, name=''):
        """Return True if there graph"""

        try:
            graph = self.database.graph(name)
            graph.properties()

        except exceptions.GraphPropertiesError:
            return False

        else:
            return True

    def get_db(self, name=''):
        """Return database"""

        if not name:
            name = app.config['ARANGO_DB']

        if self.has_database(name):
            self.database = self._conn.database(name)

        else:
            raise Exception('There no DB with name {}'.format(name))

        return self.database

    def get_collection(self, name=''):
        """Return collection"""

        if self.has_collection(name):
            self.collection = self.database.collection(name)

        else:
            raise Exception('There no Collection with name {}'.format(name))

        return self.collection

    def get_graph(self, name=''):
        """Return graph"""

        if self.has_graph(name):
            self.graph = self.database.graph(name)

        else:
            raise Exception('There no Graph with name {}'.format(name))

        return self.graph

    def create_db(self, name=''):
        """Create DB"""

        try:
            self.database = self._conn.create_database(name)

        except Exception:
            raise Exception(
                'There\'s already a database with name {}.'.format(name))

        return self.database

    def create_graph(self, name='', edge_definitions=[]):
        """Create Graph"""

        try:
            self.graph = self.database.create_graph(name)

        except Exception:
            raise Exception(
                'There\'s already a graph with name {}.'.format(name))
        else:
            for edge in edge_definitions:
                try:
                    self.graph.create_edge_definition(
                        name=edge.get('edge'),
                        from_collections=edge.get('from_collections'),
                        to_collections=edge.get('to_collections')
                    )
                except Exception as err:
                    self.graph = self.database.delete_graph(name)
                    raise Exception(
                        'Error to create edge_definition. {}'.format(err))

        return self.graph

    def create_collection(self, name='', edge=False):
        """Create Collection or Edge"""

        try:
            self.collection = self.database.create_collection(
                name=name, edge=edge)

        except Exception:
            raise Exception(
                'There\'s already a collection with name {}.'.format(name))
        return self.collection

    def delete_db(self, name=''):
        """Delete DB"""

        try:
            self.database = self._conn.delete_database(name)

        except Exception:
            raise Exception(
                'There no a database with name {}.'.format(name))

    def delete_graph(self, name=''):
        """Delete Graph"""

        try:
            self.database.delete_graph(name)

        except Exception:
            raise Exception(
                'There no a graph with name {}.'.format(name))

    def delete_collection(self, name=''):
        """Delete Collection or Edge"""

        try:
            self.collection = self.database.delete_collection(name=name)

        except Exception:
            raise Exception(
                'There no a collection with name {}.'.format(name))

    def search_document(self, collection, field, value):
        """Search Document"""

        result = self.database.aql.execute(
            '''FOR doc IN {}
                FILTER doc.`{}` like "%{}%"
                RETURN doc'''.format(collection, field, value),
            count=True,
            batch_size=1,
            ttl=10,
            optimizer_rules=['+all']
        )

        return result
