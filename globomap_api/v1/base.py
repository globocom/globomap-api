import json
from json.decoder import JSONDecodeError

from flask import current_app as app
from flask import request
from jsonspec.validators.exceptions import ValidationError

from . import api
from ..decorators import json_response
from ..exceptions import CollectionNotExist
from ..exceptions import DocumentException
from ..exceptions import DocumentNotExist
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


############
# Document #
############
@api.route('/collections/<collection>/document/', methods=['POST'])
@json_response
def create_document(collection):
    """Insert document in DB."""
    try:
        inst_coll = get_inst_collection('collection', collection)
    except CollectionNotExist as err:
        return str(err), 404
    except Exception as err:
        return str(err), 500

    try:
        document = json.loads(request.data)
    except JSONDecodeError as err:
        return str(err), 400
    except Exception as err:
        return str(err), 500

    try:
        json_validate(app.config['SPECS'].get('documents')).validate(document)
    except ValidationError as error:
        res = validate(error)
        return res, 400
    except Exception as err:
        return str(err), 500

    try:
        document = document['content']
        document['_key'] = make_key(document)
        doc = Document(inst_coll)
        res = doc.upsert_document(document)
    except DocumentException as err:
        return str(err), 400
    except Exception as err:
        return str(err), 500
    else:
        return res, 200


@api.route('/collections/<collection>/document/<document>/', methods=['GET'])
@json_response
def get_document(collection, document):
    """Get document by key."""
    try:
        inst_coll = get_inst_collection('collections', collection)
    except CollectionNotExist as err:
        return str(err), 404

    try:
        doc = Document(inst_coll)
        res = doc.get_document(document)
    except DocumentNotExist as err:
        return str(err), 404
    else:
        return res, 200


@api.route('/collections/<collection>/document/<document>/', methods=['DELETE'])
@json_response
def delete_document(edge, document):
    return {}, 200

########
# Edge #
########


@api.route('/edges/<edge>/document/', methods=['POST'])
@json_response
def edges(edge):
    """Insert edge in DB."""
    try:
        inst_edge = get_inst_collection('edges', edge)
    except CollectionNotExist as err:
        return str(err), 404
    except Exception as err:
        return str(err), 500

    try:
        document = json.loads(request.data)
    except JSONDecodeError as err:
        return str(err), 400
    except Exception as err:
        return str(err), 500

    try:
        json_validate(app.config['SPECS'].get('edges')).validate(document)
    except ValidationError as error:
        res = validate(error)
        return res, 400
    except Exception as err:
        return str(err), 500

    try:
        document['content']['_to'] = make_key_way(document['to'])
        document['content']['_from'] = make_key_way(document['from'])
        document['content']['_key'] = make_key(document['content'])
        document = document['content']
        doc = Document(inst_edge)
        res = doc.upsert_document(document)
    except DocumentException as err:
        return str(err), 400
    except Exception as err:
        return str(err), 500
    else:
        return res, 200


@api.route('/edges/<edge>/document/<document>/', methods=['GET'])
@json_response
def get_edge(edge, document):
    """Get edge by key."""
    try:
        inst_coll = get_inst_collection('edges', edge)
    except CollectionNotExist as err:
        return str(err), 404

    try:
        doc = Document(inst_coll)
        res = doc.get_document(document)
    except DocumentNotExist as err:
        return str(err), 404
    else:
        return res, 200


@api.route('/edges/<edge>/document/<document>/', methods=['DELETE'])
@json_response
def delete_edge(edge, document):
    return {}, 200


#########
# Utils #
#########
def get_inst_collection(kind, collection):
    constructor = Constructor({
        'type': kind,
        'name': collection
    })
    inst = constructor.factory()
    return inst


def make_key(document):
    key = '{}_{}'.format(
        document['provider'],
        document['id']
    )
    return key


def make_key_way(document):
    key = '{}/{}_{}'.format(
        document['collection'],
        document['provider'],
        document['id']
    )
    return key


# @api.route('/search', methods=['GET'])
# @json_response
# def egde():
#     """List all collections from DB."""
#     collection = request.args.get('collection')
#     query = request.args.get('query')

#     constructor = Constructor(graph)
#     collection = constructor.factory()
#     document['content']['_key'] = '{}_{}'.format(
#         document['content']['provider'],
#         document['content']['id']
#     )

#     try:
#         doc = Document(collection)
#         doc.create_document(document['content'])
#     except Exception as e:
#         raise Exception(e)

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
