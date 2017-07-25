import json

from flask import current_app as app
from flask import request
from jsonspec.validators.exceptions import ValidationError

from . import api
from ..decorators import json_response
from ..models.constructor import Constructor
from ..models.db import DB
from ..models.document import Document
from ..util import filter_transversal
from ..util import json_validate
from ..util import validate


@api.route('/graphs', methods=['GET', 'POST'])
@json_response
def list_graphs():
    """List all graphs from DB."""
    if request.method == 'POST':
        data = json.loads(request.data)
        try:
            json_validate(app.config['SPECS'].get('graphs')).validate(data)

        except ValidationError as error:
            res = validate(error)
            return res, 400

        else:
            errs = []
            for graph in data['graphs']:
                try:
                    graph['type'] = 'graph'
                    constructor = Constructor(graph)
                    constructor.factory(True)
                except Exception as err:
                    errs.append(str(err))
            if errs:
                return errs, 400

            return {}, 200
    else:

        db_inst = DB()
        db_inst.get_db()
        graphs = db_inst.database.graphs()
        return graphs, 200


@api.route('/collections', methods=['GET', 'POST'])
@json_response
def list_collections():
    """List all collections from DB."""
    if request.method == 'POST':
        data = json.loads(request.data)
        try:
            json_validate(app.config['SPECS'].get(
                'collections')).validate(data)

        except ValidationError as error:
            res = validate(error)
            return res, 400

        else:
            errs = []
            for collection in data['collections']:
                try:
                    constructor = Constructor(collection)
                    constructor.factory(True)
                except Exception as err:
                    errs.append(str(err))
            if errs:
                return errs, 400

            return {}, 200
    else:
        db_inst = DB()
        db_inst.get_db()
        colls = [coll for coll in db_inst.database.collections()
                 if coll['system'] is False and coll['type'] == 'document']
        return colls, 200


@api.route('/edges', methods=['GET'])
@json_response
def list_edges():
    """List all collections from DB."""

    db_inst = DB()
    db_inst.get_db()
    colls = [coll for coll in db_inst.database.collections()
             if coll['system'] is False and coll['type'] == 'edge']

    return colls, 200


@api.route('/traversal', methods=['GET'])
@json_response
def traversal():
    """List all collections from DB."""
    graph_name = request.args.get('graph')
    start_vertex = request.args.get('start_vertex')
    direction = request.args.get('direction', 'outbound')
    item_order = request.args.get('item_order', 'forward')
    strategy = request.args.get('strategy', None)
    order = request.args.get('order', None)
    edge_uniqueness = request.args.get('edge_uniqueness', None)
    vertex_uniqueness = request.args.get('vertex_uniqueness', None)
    max_iter = request.args.get('max_iter', None)
    min_depth = request.args.get('min_depth', None)
    max_depth = request.args.get('max_depth', None)
    init_func = request.args.get('init_func', None)
    sort_func = request.args.get('sort_func', None)
    filter_func = request.args.get('filter_func', None)
    visitor_func = request.args.get('visitor_func', None)
    expander_func = request.args.get('expander_func', None)

    try:
        db_inst = DB()
        db_inst.get_db()
        graph = db_inst.get_graph(graph_name)
        traversal_results = graph.traverse(
            start_vertex=start_vertex,
            direction=direction,
            item_order=item_order,
            strategy=strategy,
            order=order,
            edge_uniqueness=edge_uniqueness,
            vertex_uniqueness=vertex_uniqueness,
            max_iter=max_iter,
            min_depth=min_depth,
            max_depth=max_depth,
            init_func=init_func,
            sort_func=sort_func,
            filter_func=filter_func,
            visitor_func=visitor_func,
            expander_func=expander_func
        )
    except Exception as err:
        return str(err), 400
    else:
        traversal_results = filter_transversal(traversal_results)
        return traversal_results, 200


@api.route('/documens', methods=['GET', 'POST'])
@json_response
def documents():
    """Insert document in DB."""
    if request.method == 'POST':
        docs = json.loads(request.data)
        try:
            json_validate(app.config['SPECS'].get('documents')).validate(docs)

        except ValidationError as error:
            res = validate(error)
            return res, 400

        else:
            for document in docs['documents']:

                constructor = Constructor({
                    'type': 'collection',
                    'name': document['collection']
                })
                collection = constructor.factory()
                document['content']['_key'] = '{}_{}'.format(
                    document['content']['provider'],
                    document['content']['id']
                )

                try:
                    doc = Document(collection)
                    doc.upsert_document(document['content'])
                except Exception as err:
                    return str(err), 400

    return {}, 200


@api.route('/edges', methods=['GET', 'POST'])
@json_response
def edges():
    """Insert edge in DB."""
    if request.method == 'POST':
        docs = json.loads(request.data)
        try:
            json_validate(app.config['SPECS'].get('edges')).validate(docs)

        except ValidationError as error:
            res = validate(error)
            return res, 400

        for document in docs['edges']:

            constructor = Constructor({
                'type': 'edges',
                'name': document['collection']
            })
            collection = constructor.factory()
            document['content']['_key'] = '{}_{}'.format(
                document['content']['provider'],
                document['content']['id']
            )
            document['content']['_to'] = '{}/{}_{}'.format(
                document['to']['collection'],
                document['to']['provider'],
                document['to']['id']
            )
            document['content']['_from'] = '{}/{}_{}'.format(
                document['from']['collection'],
                document['from']['provider'],
                document['from']['id']
            )

            try:
                doc = Document(collection)
                doc.upsert_document(document['content'])
            except Exception as err:
                return str(err), 400
    return {}, 200


@api.route('/search', methods=['GET'])
@json_response
def egde():
    """List all collections from DB."""
    collection = request.args.get('collection')
    query = request.args.get('query')

    constructor = Constructor(graph)
    collection = constructor.factory()
    document['content']['_key'] = '{}_{}'.format(
        document['content']['provider'],
        document['content']['id']
    )

    try:
        doc = Document(collection)
        doc.create_document(document['content'])
    except Exception as e:
        raise Exception(e)

# @api.route('/search/', methods=['GET'])
# @json_response
# def search_elements():
#     return {}, 200


# @api.route('/<name>/', methods=['GET'])
# @json_response
# def get_element(name):
#     return {}, 200


# @api.route('/<name>/', methods=['POST'])
# @json_response
# def create_element(name):
#     return {}, 201


# @api.route('/<name>/<int:id>/', methods=['PUT'])
# @json_response
# def update_element(name, id):
#     return {}, 200


# @api.route('/<name>/<int:id>/', methods=['DELETE'])
# @json_response
# def delete_element(name, id):
#     return {}, 200
