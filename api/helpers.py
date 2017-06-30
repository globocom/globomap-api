import os

from pyArango.collection import Collection
from pyArango.connection import Connection
from pyArango.graph import Graph

from api.models.basegraph import BaseGraph
from api.models.compunit import CompUnit
from api.models.pool import Pool
from api.models.poolcompunit import PoolCompUnit
from api.models.port import Port
from api.models.vip import Vip


class Setup(object):

    def __init__(self):

        self._connection()
        self._start_db('globomap')

        self.vip = Vip
        self.pool = Pool
        self.compunit = CompUnit
        self.port = Port
        self.poolcompunit = PoolCompUnit
        self.basegraph = BaseGraph

        self.vip = self._start_colletion('Collection', 'Vip')
        self.pool = self._start_colletion('Collection', 'Pool')
        self.compunit = self._start_colletion('Collection', 'CompUnit')

        self.port = self._start_colletion('Edges', 'Port')
        self.poolcompunit = self._start_colletion('Edges', 'PoolCompUnit')

        self.basegraph = self._start_graph('BaseGraph')

    def _connection(self):

        self.username = os.getenv('USERNAME')
        self.password = os.getenv('PASSWORD')
        self.arangoURL = os.getenv('ARANGOURL')

        self.conn = Connection(
            username=self.username,
            password=self.password,
            arangoURL=self.arangoURL
        )

    def _start_db(self, database_name):

        if not self.conn.hasDatabase(database_name):
            self.conn.createDatabase(database_name)
        self.db = self.conn[database_name]

    def _start_graph(self, graph_name):

        if not self.db.hasGraph(graph_name):
            self.db.createGraph(graph_name)
        self.graph = Graph.getGraphClass(graph_name)

    def _start_colletion(self, kind, name):

        if not self.db.hasCollection(name):
            self.db.createCollection(kind, name=name)
        self.colletion = Collection.getCollectionClass(name)
