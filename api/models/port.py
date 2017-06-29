from pyArango.collection import Edges
from pyArango.collection import Field


class Port(Edges):
    _fields = {
        'number': Field(),
        'path': Field()
    }
