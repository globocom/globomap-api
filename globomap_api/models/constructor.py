import string

from .db import DB


class Constructor(object):

    """Contructor of class of type Collection, Edges or Graph"""

    def __init__(self, spec):

        self.name = spec.get('name')
        self.kind = string.capwords(spec.get('type', ''))
        self.links = spec.get('links', [])

    def factory(self, create=False):
        """Return class of type Collection, Edges or Graph"""

        if self.kind == 'Collection':
            class_fact = self._class_collection_factory(create=create)
        elif self.kind == 'Edges':
            class_fact = self._class_edge_factory(create=create)
        elif self.kind == 'Graph':
            class_fact = self._class_graph_factory(create=create)
        else:
            raise Exception('Kind invalid')

        return class_fact

    def _class_collection_factory(self, create=False):

        db_inst = DB()
        if create:
            col = db_inst.create_colletion(name=self.name, edge=False)
        else:
            col = db_inst.get_colletion(self.name)

        return col

    def _class_edge_factory(self, create=False):

        db_inst = DB()
        if create:
            col = db_inst.create_colletion(name=self.name, edge=True)
        else:
            col = db_inst.get_colletion(self.name)

        return col

    def _class_graph_factory(self, create=False):

        db_inst = DB()
        if create:
            graph = db_inst.create_graph(self.name, self.links)
        else:
            graph = db_inst.get_graph(self.name)

        return graph
