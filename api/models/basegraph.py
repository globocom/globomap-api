from pyArango.graph import EdgeDefinition
from pyArango.graph import Graph


class BaseGraph(Graph):

    _edgeDefinitions = (
        EdgeDefinition('port',
                       fromCollections=['vip'],
                       toCollections=['pool']),
        EdgeDefinition('poolcompunit',
                       fromCollections=['pool'],
                       toCollections=['compunit']),
    )
    _orphanedCollections = []
