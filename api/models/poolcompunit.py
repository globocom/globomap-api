from pyArango.collection import Edges
from pyArango.collection import Field


class PoolCompUnit(Edges):
    _fields = {
        'id': Field(),
    }
