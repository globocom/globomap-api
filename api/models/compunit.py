from pyArango.collection import Collection
from pyArango.collection import Field


class CompUnit(Collection):
    _fields = {
        'id': Field(),
    }
