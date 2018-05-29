"""
   Copyright 2018 Globo.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import math

from arango.exceptions import GraphTraverseError
from flask import current_app as app

from globomap_api import exceptions as gmap_exceptions
from globomap_api import util
from globomap_api.errors import GRAPH_TRAVERSE as traverse_err
from globomap_api.models.constructor import Constructor
from globomap_api.models.db import DB
from globomap_api.models.document import Document


def list_graphs():
    """Return all graph from Database"""

    db_inst = DB()
    db_inst.get_database()
    graphs = db_inst.database.graphs()
    graphs = util.filter_graphs(graphs)

    return graphs


def list_collections(kind):
    """Return all collections or edges from Database"""

    db_inst = DB()
    db_inst.get_database()
    collections = db_inst.database.collections()
    collections = util.filter_collections(collections, kind)

    return collections


def get_document(name, key):
    """Get document from Database"""

    constructor = Constructor()
    inst_coll = constructor.factory(kind='Collection', name=name)

    inst_doc = Document(inst_coll)
    doc = inst_doc.get_document(key)

    return doc


def get_edge(name, key):
    """Get edge from Database"""

    constructor = Constructor()
    inst_edge = constructor.factory(kind='Edges', name=name)

    inst_doc = Document(inst_edge)
    doc = inst_doc.get_document(key)

    return doc


def search_traversal(**kwargs):
    """Search Traversal in Database"""

    db_inst = DB()
    db_inst.get_database()
    graph = db_inst.get_graph(kwargs.get('graph_name'))
    try:
        traversal_results = graph.traverse(
            start_vertex=kwargs.get('start_vertex'),
            direction=kwargs.get('direction'),
            item_order=kwargs.get('item_order'),
            strategy=kwargs.get('strategy'),
            order=kwargs.get('order'),
            edge_uniqueness=kwargs.get('edge_uniqueness'),
            vertex_uniqueness=kwargs.get('vertex_uniqueness'),
            max_iter=kwargs.get('max_iter'),
            min_depth=kwargs.get('min_depth'),
            max_depth=kwargs.get('max_depth'),
            init_func=kwargs.get('init_func'),
            sort_func=kwargs.get('sort_func'),
            filter_func=kwargs.get('filter_func'),
            visitor_func=kwargs.get('visitor_func'),
            expander_func=kwargs.get('expander_func')
        )
    except GraphTraverseError as err:

        if traverse_err.get(err.error_code):
            if err.error_code == 1202:
                msg = traverse_err.get(1202)
                raise gmap_exceptions.GraphTraverseException(msg)
            raise gmap_exceptions.GraphTraverseException(
                traverse_err.get(err.error_code).format(err.message))

        else:
            raise gmap_exceptions.GraphTraverseException(
                traverse_err.get(0).format(
                    kwargs.get('graph_name'), err.message))

    except Exception as err:
        raise gmap_exceptions.GraphTraverseException(
            traverse_err.get(0).format(kwargs.get('graph_name'), err.message))

    traversal_results = util.filter_transversal(traversal_results)
    traversal_results.update({'graph': kwargs.get('graph_name')})

    return traversal_results


def search(name, data, page, per_page):
    """Search in Database"""

    spec = app.config['SPECS'].get('search')
    util.json_validate(spec).validate(data)

    db_inst = DB()

    db_inst.get_database()
    cursor = db_inst.search_in_collection(name, data, page, per_page)

    total_pages = int(math.ceil(cursor.statistics()[
                      'fullCount'] / (per_page * 1.0)))
    total_documents = cursor.statistics()['fullCount']

    docs = [doc for doc in cursor]

    res = {
        'total_pages': total_pages,
        'total': len(docs),
        'total_documents': total_documents,
        'documents': docs
    }

    return res


def search_collections(collections, data, page, per_page):
    """Search in Database"""

    spec = app.config['SPECS'].get('search')
    util.json_validate(spec).validate(data)

    db_inst = DB()

    db_inst.get_database()
    cursor = db_inst.search_in_collections(collections, data, page, per_page)

    total_pages = int(math.ceil(cursor.statistics()[
                      'fullCount'] / (per_page * 1.0)))
    total_documents = cursor.statistics()['fullCount']

    docs = [doc for doc in cursor]

    res = {
        'total_pages': total_pages,
        'total': len(docs),
        'total_documents': total_documents,
        'documents': docs
    }

    return res
