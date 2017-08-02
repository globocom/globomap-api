import string

from flask import current_app as app

from .db import DB
from globomap_api.exceptions import ConstructorException


class Constructor(object):

    """Contructor of class of type Collection, Edges or Graph"""

    name = None
    kind = None
    links = None
    create = False

    def _treat_param(self, kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def factory(self, **kwargs):
        """Return class of type Collection, Edges or Graph"""
        self._treat_param(kwargs)

        if self.kind == 'Collection':
            class_fact = self._class_collection_factory()
        elif self.kind == 'Edges':
            class_fact = self._class_edge_factory()
        elif self.kind == 'Graph':
            class_fact = self._class_graph_factory()
        else:
            raise ConstructorException('Kind invalid')
        return class_fact

    def _class_collection_factory(self):

        db_inst = DB()
        db_inst.get_database()
        if self.create:
            col = db_inst.create_collection(name=self.name)
        else:
            col = db_inst.get_collection(name=self.name)
        return col

    def _class_edge_factory(self):

        db_inst = DB()
        db_inst.get_database()
        if self.create:
            col = db_inst.create_edge(name=self.name)
        else:
            col = db_inst.get_edge(name=self.name)
        return col

    def _class_graph_factory(self):

        db_inst = DB()
        db_inst.get_database()
        if self.create and self.links:
            graph = db_inst.create_graph(self.name, self.links)
        else:
            graph = db_inst.get_graph(self.name)
        return graph
