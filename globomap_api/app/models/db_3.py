import os

from pyArango.connection import Connection


class DB(object):

    def __init__(self):

        self._connection()
        self._start_db(os.getenv('DB'))

    def _connection(self):

        self.username = os.getenv('USERNAME')
        self.password = os.getenv('PASSWORD')
        self.arangoURL = os.getenv('ARANGOURL')

        self.conn = Connection(
            username=self.username,
            password=self.password,
            arangoURL=self.arangoURL
        )

    def get_db(self, name):

        if self.conn.hasDatabase(name):
            self.db = self.conn[name]
            return self.db
        else:
            raise Exception('DB não existe')

    def get_graph(self, name):

        if self.db.hasGraph(name):
            self.graph = self.db.graphs[name]
            return self.graph
        else:
            raise Exception('Graph não existe')

    def get_colletion(self, name):

        if self.db.hasCollection(name):
            self.colletion = self.db.collections[name]
            return self.colletion
        else:
            raise Exception('Collection não existe')

    def _start_db(self, name):

        if not self.conn.hasDatabase(name):
            self.db = self.conn.createDatabase(name)
        else:
            self.db = self.conn[name]

    def _start_graph(self, name):
        if not self.db.hasGraph(name):
            self.graph = self.db.createGraph(name)
        else:
            self.graph = self.db.graphs[name]

    def _start_colletion(self, kind, name):

        if not self.db.hasCollection(name):
            self.colletion = self.db.createCollection(kind, name=name)
        else:
            self.colletion = self.db.collections[name]

    def create_db(self, name):

        if not self.conn.hasDatabase(name):
            self.db = self.conn.createDatabase(name)
            return self.db
        else:
            raise Exception('Já existe DB')

    def create_graph(self, name):

        if not self.db.hasGraph(name):
            self.graph = self.db.createGraph(name)
            return self.graph
        else:
            raise Exception('Já existe Graph')

    def create_colletion(self, kind, name):

        if not self.db.hasCollection(name):
            self.colletion = self.db.createCollection(kind, name=name)
            return self.colletion
        else:
            raise Exception('Já existe Collection')
