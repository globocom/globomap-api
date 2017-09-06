from flask import current_app as app

from globomap_api import util
from globomap_api.models.constructor import Constructor
from globomap_api.models.db import DB
from globomap_api.models.document import Document


def create_graph(data):
    """Create graph in Database"""

    spec = app.config['SPECS'].get('graphs')
    util.json_validate(spec).validate(data)

    constructor = Constructor()
    name = data.get('name')
    links = data.get('links')
    graph = constructor.factory(
        kind='Graph', create=True, name=name, links=links)

    return True


def create_collection_document(data):
    """Create collection in Database"""

    spec = app.config['SPECS'].get('collections')
    util.json_validate(spec).validate(data)

    constructor = Constructor()
    name = data.get('name')
    collection = constructor.factory(
        kind='Collection', create=True, name=name)

    return True


def create_collection_edge(data):
    """Create edge in Database"""

    spec = app.config['SPECS'].get('collections')
    util.json_validate(spec).validate(data)

    constructor = Constructor()
    name = data.get('name')
    edge = constructor.factory(
        kind='Edges', create=True, name=name)

    return True


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


def create_document(name, data):
    """Create document in Database"""

    spec = app.config['SPECS'].get('documents')
    util.json_validate(spec).validate(data)

    constructor = Constructor()
    inst_coll = constructor.factory(kind='Collection', name=name)

    document = data
    document = {
        '_key': util.make_key(data),
        'id': data['id'],
        'name': data['name'],
        'provider': data['provider'],
        'timestamp': data['timestamp'],
        'properties': data.get('properties'),
        'metadata': data.get('metadata')
    }

    inst_doc = Document(inst_coll)
    doc = inst_doc.create_document(document)

    return doc


def create_edge(name, data):
    """Create document-edge in Database"""

    spec = app.config['SPECS'].get('edges')
    util.json_validate(spec).validate(data)

    constructor = Constructor()
    inst_edge = constructor.factory(kind='Edges', name=name)
    edge = {
        '_key': util.make_key(data),
        '_from': data['from'],
        '_to': data['to'],
        'id': data['id'],
        'name': data['name'],
        'provider': data['provider'],
        'timestamp': data['timestamp'],
        'properties': data.get('properties'),
        'metadata': data.get('metadata')
    }

    inst_doc = Document(inst_edge)
    doc = inst_doc.create_document(edge)

    return doc


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


def update_edge(name, key, data):
    """Update edge from Database"""

    get_edge(name, key)

    spec = app.config['SPECS'].get('edges')
    util.json_validate(spec).validate(data)
    edge = {
        '_key': key,
        '_from': data['from'],
        '_to': data['to'],
        'id': data['id'],
        'name': data['name'],
        'provider': data['provider'],
        'timestamp': data['timestamp'],
        'properties': data.get('properties'),
        'metadata': data.get('metadata')
    }

    constructor = Constructor()
    inst_edge = constructor.factory(kind='Edges', name=name)

    inst_doc = Document(inst_edge)
    doc = inst_doc.update_document(edge)

    return doc


def update_document(name, key, data):
    """Update document from Database"""

    get_document(name, key)

    spec = app.config['SPECS'].get('documents')
    util.json_validate(spec).validate(data)
    document = {
        '_key': key,
        'id': data['id'],
        'name': data['name'],
        'provider': data['provider'],
        'timestamp': data['timestamp'],
        'properties': data.get('properties'),
        'metadata': data.get('metadata')
    }

    constructor = Constructor()
    inst_coll = constructor.factory(kind='Collection', name=name)

    inst_doc = Document(inst_coll)
    doc = inst_doc.update_document(document)

    return doc


def patch_edge(name, key, data):
    """Partial update edge from Database"""

    edge = get_edge(name, key)

    spec = app.config['SPECS'].get('edges_partial')
    util.json_validate(spec).validate(data)
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


def patch_document(name, key, data):
    """Partial update document from Database"""

    document = get_document(name, key)

    spec = app.config['SPECS'].get('documents_partial')
    util.json_validate(spec).validate(data)

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
    doc = inst_doc.delete_document(key)

    return True


def delete_edge(name, key):
    """Get edge from Database"""

    constructor = Constructor()
    inst_edge = constructor.factory(kind='Edges', name=name)

    inst_doc = Document(inst_edge)
    doc = inst_doc.delete_document(key)

    return True


def search_document(name, field, value, offset=0, count=100):
    """Search in Database"""

    db_inst = DB()
    db_inst.get_database()
    cursor = db_inst.search_in_database(
        name, field, value, offset, count)
    docs = [doc for doc in cursor]

    return docs


def search_traversal(**kwargs):
    """Search Traversal in Database"""

    db_inst = DB()
    db_inst.get_database()
    graph = db_inst.get_graph(kwargs.get('graph_name'))

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

    traversal_results = util.filter_transversal(traversal_results)
    traversal_results.update({'graph': kwargs.get('graph_name')})

    return traversal_results
