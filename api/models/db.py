import os

from arango import ArangoClient
from arango import exceptions


class DB(object):

    """DB"""

    colletion = None
    database = None
    graph = None
    conn = None

    def __init__(self):

        self._connection()
        self.get_db(os.getenv('DB'))

    def _connection(self):

        self.username = os.getenv('USERNAME')
        self.password = os.getenv('PASSWORD')
        self.arango_protocol = os.getenv('ARANGOPROTOCOL')
        self.arango_host = os.getenv('ARANGOHOST')
        self.arango_port = os.getenv('ARANGOPORT')

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

        if self.has_database(name):
            self.database = self._conn.database(name)

        else:
            raise Exception('There no DB with name {}'.format(name))

        return self.database

    def get_colletion(self, name=''):
        """Return collection"""

        if self.has_collection(name):
            self.colletion = self.database.collection(name)

        else:
            raise Exception('There no Collection with name {}'.format(name))

        return self.colletion

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

    def create_colletion(self, name='', edge=False):
        """Create Collection or Edge"""

        try:
            self.colletion = self.database.create_collection(
                name=name, edge=edge)

        except Exception:
            raise Exception(
                'There\'s already a collection with name {}.'.format(name))

        return self.colletion
