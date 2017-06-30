from pyArango.collection import Collection
from pyArango.collection import Field


class Pool(Collection):
    _fields = {
        'id': Field(),
    }
