from pyArango.collection import Collection
from pyArango.collection import Field


class CompUnit(Collection):
    _fields = {
        'id': Field(),
    }

    class compunit(Collection):
        _fields = {
            'id': Field(),
        }

    class port(Edges):
        _fields = {
            'number': Field(),
            'path': Field()
        }

    class poolcompunit(Edges):
        _fields = {
            'number': Field()
        }
