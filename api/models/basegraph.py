from pyArango.graph import EdgeDefinition
from pyArango.graph import Graph


class BaseGraph(Graph):

    _edgeDefinitions = (
        EdgeDefinition('Port',
                       fromCollections=['Vip'],
                       toCollections=['Pool']),
        EdgeDefinition('PoolCompUnit',
                       fromCollections=['Pool'],
                       toCollections=['CompUnit']),
    )
    _orphanedCollections = []
