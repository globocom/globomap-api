from pyArango.collection import Collection
from pyArango.collection import Field


class Vip(Collection):
    _fields = {
        'id': Field(),
        'ip': Field(),
        'name': Field(),
    }
