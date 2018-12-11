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
from globomap_api.api.v2 import util
from globomap_api.errors import GRAPH_TRAVERSE as traverse_err
from globomap_api.models.constructor import Constructor
from globomap_api.models.document import Document


#########
# GRAPH #
#########
def create_graph(data):
    """Create graph in Database"""

    constructor = Constructor()
    name = data.get('name')
    links = data.get('links')
    constructor.factory(kind='Graph', create=True, name=name, links=links)
    create_meta_graph_doc(data)

    return True


def create_meta_graph_doc(data):
    """Create document in meta_graph"""

    constructor = Constructor()
    inst_coll = constructor.factory(
        kind='Collection', name=app.config['META_GRAPH'])

    inst_doc = Document(inst_coll)
    document = {
        '_key': data.get('name'),
        'name': data.get('name'),
        'links': data.get('links'),
        'alias': data.get('alias'),
        'icon': data.get('icon'),
        'description': data.get('description'),
    }
    doc = inst_doc.create_document(document)

    return doc


def list_graphs(page=1, per_page=10):
    """Return all graph from Database"""

    db_inst = app.config['ARANGO_CONN']
    db_inst.get_database()
    cursor = db_inst.search_in_collection(
        app.config['META_GRAPH'], None, page, per_page)

    total_pages = int(math.ceil(cursor.statistics()[
                      'fullCount'] / (per_page * 1.0)))
    total_graphs = cursor.statistics()['fullCount']

    graphs = util.filter_graphs(cursor)
    res = {
        'total_pages': total_pages,
        'total': len(graphs),
        'total_graphs': total_graphs,
        'graphs': graphs
    }

    return res


##############
# COLLECTION #
##############
def create_meta_collection_doc(data, kind):
    """Create document in meta_collection"""

    constructor = Constructor()
    inst_coll = constructor.factory(
        kind='Collection', name=app.config['META_COLLECTION'])

    inst_doc = Document(inst_coll)
    document = {
        '_key': data.get('name'),
        'name': data.get('name'),
        'alias': data.get('alias'),
        'kind': kind,
        'icon': data.get('icon'),
        'description': data.get('description'),
        'users': data.get('users'),
    }
    doc = inst_doc.create_document(document)

    return doc


def create_collection_document(data):
    """Create collection in Database"""

    constructor = Constructor()
    name = data.get('name')
    constructor.factory(kind='Collection', create=True, name=name)
    create_meta_collection_doc(data, 'document')

    return True


def create_collection_edge(data):
    """Create edge in Database"""

    constructor = Constructor()
    name = data.get('name')
    constructor.factory(kind='Edges', create=True, name=name)
    create_meta_collection_doc(data, 'edge')

    return True


def list_collections(kind, data=[], page=1, per_page=10):
    """Return all collections or edges from Database"""

    db_inst = app.config['ARANGO_CONN']
    db_inst.get_database()
    filter_coll = [{
        'field': 'kind',
        'operator': '==',
        'value': kind,
    }]
    for idx, _ in enumerate(data):
        data[idx] += filter_coll
    cursor = db_inst.search_in_collection(
        app.config['META_COLLECTION'], data, page, per_page)

    total_pages = int(math.ceil(cursor.statistics()[
                      'fullCount'] / (per_page * 1.0)))
    total_collections = cursor.statistics()['fullCount']

    collections = util.filter_collections(cursor)
    res = {
        'total_pages': total_pages,
        'total': len(collections),
        'total_collections': total_collections,
        'collections': collections
    }

    return res


############
# DOCUMENT #
############
def create_document(name, data):
    """Create document in Database"""

    constructor = Constructor()
    inst_coll = constructor.factory(kind='Collection', name=name)

    document = data
    document = {
        '_key': util.make_key(data),
        'id': data['id'],
        'name': data.get('name', ''),
        'provider': data['provider'],
        'timestamp': data['timestamp'],
        'properties': data.get('properties'),
        'properties_metadata': data.get('properties_metadata')
    }

    inst_doc = Document(inst_coll)
    doc = inst_doc.create_document(document)

    return doc


def get_document(name, key):
    """Get document from Database"""

    constructor = Constructor()
    inst_coll = constructor.factory(kind='Collection', name=name)

    inst_doc = Document(inst_coll)
    doc = inst_doc.get_document(key)

    return doc


def update_document(name, key, data):
    """Update document from Database"""

    get_document(name, key)
    document = {
        '_key': key,
        'id': data['id'],
        'name': data.get('name', ''),
        'provider': data['provider'],
        'timestamp': data['timestamp'],
        'properties': data.get('properties'),
        'properties_metadata': data.get('properties_metadata')
    }

    constructor = Constructor()
    inst_coll = constructor.factory(kind='Collection', name=name)

    inst_doc = Document(inst_coll)
    doc = inst_doc.update_document(document)

    return doc


def patch_document(name, key, data):
    """Partial update document from Database"""

    document = get_document(name, key)

    for key in data:
        if key == 'properties':
            for idx in data[key]:
                document['properties'][idx] = data[key][idx]
        elif key == 'properties_metadata':
            for idx in data[key]:
                document['properties_metadata'][idx] = data[key][idx]
        elif key == 'name':
            if data[key]:
                document[key] = data[key]
        else:
            document[key] = data[key]

    constructor = Constructor()
    inst_coll = constructor.factory(kind='Collection', name=name)

    inst_doc = Document(inst_coll)
    doc = inst_doc.update_document(document)

    return doc


def delete_document(name, key):
    """Get document from Database"""

    constructor = Constructor()
    inst_coll = constructor.factory(kind='Collection', name=name)

    inst_doc = Document(inst_coll)
    inst_doc.delete_document(key)

    return True


########
# EDGE #
########
def create_edge(name, data):
    """Create document-edge in Database"""

    constructor = Constructor()
    inst_edge = constructor.factory(kind='Edges', name=name)
    edge = {
        '_key': util.make_key(data),
        '_from': data['from'],
        '_to': data['to'],
        'id': data['id'],
        'name': data.get('name', ''),
        'provider': data['provider'],
        'timestamp': data['timestamp'],
        'properties': data.get('properties'),
        'properties_metadata': data.get('properties_metadata')
    }

    inst_doc = Document(inst_edge)
    doc = inst_doc.create_document(edge)

    return doc


def get_edge(name, key):
    """Get edge from Database"""

    constructor = Constructor()
    inst_edge = constructor.factory(kind='Edges', name=name)

    inst_doc = Document(inst_edge)
    doc = inst_doc.get_document(key)

    return doc


def update_edge(name, key, data):
    """Update edge from Database"""

    get_edge(name, key)
    edge = {
        '_key': key,
        '_from': data['from'],
        '_to': data['to'],
        'id': data['id'],
        'name': data.get('name', ''),
        'provider': data['provider'],
        'timestamp': data['timestamp'],
        'properties': data.get('properties'),
        'properties_metadata': data.get('properties_metadata')
    }

    constructor = Constructor()
    inst_edge = constructor.factory(kind='Edges', name=name)

    inst_doc = Document(inst_edge)
    doc = inst_doc.update_document(edge)

    return doc


def patch_edge(name, key, data):
    """Partial update edge from Database"""

    edge = get_edge(name, key)
    for key in data:
        if key == 'from':
            edge['_from'] = data[key]
        elif key == 'to':
            edge['_to'] = data[key]
        elif key == 'properties':
            for idx in data[key]:
                edge['properties'][idx] = data[key][idx]
        elif key == 'properties_metadata':
            for idx in data[key]:
                edge['properties_metadata'][idx] = data[key][idx]
        elif key == 'name':
            if data[key]:
                edge[key] = data[key]
        else:
            edge[key] = data[key]

    constructor = Constructor()
    inst_edge = constructor.factory(kind='Edges', name=name)

    inst_doc = Document(inst_edge)
    doc = inst_doc.update_document(edge)

    return doc


def delete_edge(name, key):
    """Get edge from Database"""

    constructor = Constructor()
    inst_edge = constructor.factory(kind='Edges', name=name)

    inst_doc = Document(inst_edge)
    inst_doc.delete_document(key)

    return True


##########
# SEARCH #
##########
def search_traversal(**kwargs):
    """Search Traversal in Database"""

    db_inst = app.config['ARANGO_CONN']
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
            traverse_err.get(0).format(kwargs.get('graph_name'), err))

    traversal_results = util.filter_transversal(traversal_results)
    traversal_results.update({'graph': kwargs.get('graph_name')})

    return traversal_results


def search(name, data, page, per_page):
    """Search in Database"""

    db_inst = app.config['ARANGO_CONN']

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


def clear_collection(name, data):
    """Clear document in Collection"""

    db_inst = app.config['ARANGO_CONN']

    db_inst.get_database()
    db_inst.clear_collection(name, data)

    return {}


def search_collections(collections, data, page, per_page):
    """Search in Database"""

    db_inst = app.config['ARANGO_CONN']

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


###########
# QUERIES #
###########
def make_query(data):
    """Validate query and make document"""

    query = data
    key = 'query_{}'.format(data.get('name'))
    query = {
        '_key': key,
        'name': data.get('name'),
        'description': data.get('description'),
        'query': data.get('query'),
        'params': data.get('params'),
        'collection': data.get('collection')
    }

    db_inst = app.config['ARANGO_CONN']
    db_inst.get_database()
    db_inst.validate_aql(data.get('query'))

    return query


def create_query(data):
    """Create query in Database"""

    query = make_query(data)

    constructor = Constructor()
    inst_coll = constructor.factory(kind='Collection',
                                    name=app.config['META_QUERY'])

    inst_doc = Document(inst_coll)
    doc = inst_doc.create_document(query)

    return doc


def update_query(key, data):
    """Update query in Database"""

    query = make_query(data)

    constructor = Constructor()
    inst_coll = constructor.factory(kind='Collection',
                                    name=app.config['META_QUERY'])

    inst_doc = Document(inst_coll)
    doc = inst_doc.update_document(query)

    return doc


def get_query(key):
    """Get query from Database"""

    # TODO: validate key
    return get_document(app.config['META_QUERY'], key)


def delete_query(key):
    """Delete query in Database"""

    # TODO: validate key
    return delete_document(app.config['META_QUERY'], key)


def list_query(data, page, per_page):
    """List query in Database"""

    return search(app.config['META_QUERY'], data, page, per_page)


def execute_query(key, variable):
    query = get_query(key)
    if variable:
        query['params']['variable'] = variable

    db_inst = app.config['ARANGO_CONN']

    db_inst.get_database()
    cursor = db_inst.execute_aql(query['query'], query['params'])

    docs = [doc for doc in cursor]

    return docs
