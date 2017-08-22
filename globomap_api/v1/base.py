import json
from json.decoder import JSONDecodeError

from flask import current_app as app
from flask import request
from jsonspec.validators.exceptions import ValidationError

from . import api
from globomap_api import decorators
from globomap_api import exceptions as gmap_exc
from globomap_api.util import validate
from globomap_api.v1 import facade


##########
# Graphs #
##########
@api.route('/graphs', methods=['GET'])
@decorators.json_response
def list_graphs():
    """List all graphs from DB."""

    try:
        graphs = facade.list_graphs()
        return graphs, 200
    except gmap_exc.DatabaseNotExist as err:
        return err, 400
    except Exception as err:
        return str(err), 500


@api.route('/graphs', methods=['POST'])
@decorators.json_response
def create_graph():
    """Create graph in DB."""

    try:
        data = json.loads(request.data)
        facade.create_graph(data)
        return {}, 200
    except JSONDecodeError as err:
        return str(err), 400
    except ValidationError as error:
        res = validate(error)
        return res, 400
    except Exception as err:
        return str(err), 500


#########
# Edges #
#########
@api.route('/edges', methods=['GET'])
@decorators.json_response
def list_edges():
    """List all collections of kind edge from DB."""

    try:
        collections = facade.list_collections('edge')
        return collections, 200
    except gmap_exc.DatabaseNotExist as err:
        return err.message, 400
    except Exception as err:
        return str(err), 500


@api.route('/edges', methods=['POST'])
@decorators.json_response
def create_edge():
    """Create collection of kind edge in DB."""

    try:
        data = json.loads(request.data)
        facade.create_collection_edge(data)
        return {}, 200
    except JSONDecodeError as err:
        return str(err), 400
    except ValidationError as error:
        res = validate(error)
        return res, 400
    except gmap_exc.CollectionNotExist as err:
        return err.message, 404
    except Exception as err:
        return str(err), 500


@api.route('/edges/<edge>', methods=['POST'])
@decorators.json_response
def edges(edge):
    """Insert edge in DB."""

    try:
        data = json.loads(request.data)
        res = facade.create_edge(edge, data)
        return res, 200
    except gmap_exc.EdgeNotExist as err:
        return err.message, 404
    except JSONDecodeError as err:
        return str(err), 400
    except ValidationError as error:
        res = validate(error)
        return res, 400
    except gmap_exc.DocumentException as err:
        return err.message, 400
    except Exception as err:
        return str(err), 500


@api.route('/edges/<edge>/<key>', methods=['PUT'])
@decorators.json_response
def update_edge(edge, key):
    """Update edge."""

    try:
        data = json.loads(request.data)
        res = facade.update_edge(edge, key, data)
        return res, 200
    except JSONDecodeError as err:
        return str(err), 400
    except ValidationError as error:
        res = validate(error)
        return res, 400
    except gmap_exc.EdgeNotExist as err:
        return err.message, 404
    except gmap_exc.DocumentNotExist as err:
        return err.message, 404
    except Exception as err:
        return str(err), 500


@api.route('/edges/<edge>/<key>', methods=['PATCH'])
@decorators.json_response
def patch_edge(edge, key):
    """Partial update edge."""

    try:
        data = json.loads(request.data)
        res = facade.patch_edge(edge, key, data)
        return res, 200
    except JSONDecodeError as err:
        return str(err), 400
    except ValidationError as error:
        res = validate(error)
        return res, 400
    except gmap_exc.EdgeNotExist as err:
        return err.message, 404
    except gmap_exc.DocumentNotExist as err:
        return err.message, 404
    except Exception as err:
        return str(err), 500


@api.route('/edges/<edge>/<key>', methods=['GET'])
@decorators.json_response
def get_edge(edge, key):
    """Get edge by key."""

    try:
        res = facade.get_edge(edge, key)
        return res, 200
    except gmap_exc.EdgeNotExist as err:
        return err.message, 404
    except gmap_exc.DocumentNotExist as err:
        return err.message, 404
    except Exception as err:
        return str(err), 500


@api.route('/edges/<edge>/<key>', methods=['DELETE'])
@decorators.json_response
def delete_edge(edge, key):
    """Get edge by key."""

    try:
        facade.delete_edge(edge, key)
        return {}, 200
    except gmap_exc.EdgeNotExist as err:
        return err.message, 404
    except gmap_exc.DocumentNotExist as err:
        return err.message, 404
    except Exception as err:
        return str(err), 500


@api.route('/edges/<edge>', methods=['GET'])
@api.route('/edges/<edge>/search', methods=['GET'])
@decorators.json_response
def search_in_edge(edge):
    """List all edges from DB."""
    field = request.args.get('field')
    value = request.args.get('value')
    offset = request.args.get('offset', 0)
    count = request.args.get('count', 10)

    try:
        res = facade.search_document(edge, field, value, offset, count)
        return res, 200
    except gmap_exc.CollectionNotExist as err:
        return err.message, 404
    except Exception as err:
        return str(err), 500


###############
# Collections #
###############
@api.route('/collections', methods=['GET'])
@decorators.json_response
def list_collections():
    """List all collections of kind document from DB."""

    try:
        collections = facade.list_collections(kind='document')
        return collections, 200
    except gmap_exc.DatabaseNotExist as err:
        return err.message, 400
    except Exception as err:
        return str(err), 500


@api.route('/collections', methods=['POST'])
@decorators.json_response
def create_collection():
    """Create collection of kind document in DB."""

    try:
        data = json.loads(request.data)
        facade.create_collection_document(data)
        return {}, 200
    except JSONDecodeError as err:
        return str(err), 400
    except ValidationError as error:
        res = validate(error)
        return res, 400
    except gmap_exc.CollectionNotExist as err:
        return err.message, 404
    except Exception as err:
        return str(err), 500


@api.route('/collections/<collection>', methods=['POST'])
@decorators.json_response
def create_document(collection):
    """Insert document in DB."""

    try:
        data = json.loads(request.data)
        res = facade.create_document(collection, data)
        return res, 200
    except JSONDecodeError as err:
        return str(err), 400
    except ValidationError as error:
        res = validate(error)
        return res, 400
    except gmap_exc.CollectionNotExist as err:
        return err.message, 404
    except gmap_exc.DocumentException as err:
        return err.message, 400
    except Exception as err:
        return str(err), 500


@api.route('/collections/<collection>/<key>', methods=['PUT'])
@decorators.json_response
def update_document(collection, key):
    """Update document."""

    try:
        data = json.loads(request.data)
        res = facade.update_document(collection, key, data)
        return res, 200
    except JSONDecodeError as err:
        return str(err), 400
    except ValidationError as error:
        res = validate(error)
        return res, 400
    except gmap_exc.CollectionNotExist as err:
        return err.message, 404
    except gmap_exc.DocumentNotExist as err:
        return err.message, 404
    except Exception as err:
        return str(err), 500


@api.route('/collections/<collection>/<key>', methods=['PATCH'])
@decorators.json_response
def patch_document(collection, key):
    """Partial update document."""

    try:
        data = json.loads(request.data)
        res = facade.patch_document(collection, key, data)
        return res, 200
    except JSONDecodeError as err:
        return str(err), 400
    except ValidationError as error:
        res = validate(error)
        return res, 400
    except gmap_exc.CollectionNotExist as err:
        return err.message, 404
    except gmap_exc.DocumentNotExist as err:
        return err.message, 404
    except Exception as err:
        return str(err), 500


@api.route('/collections/<collection>/<key>', methods=['GET'])
@decorators.json_response
def get_document(collection, key):
    """Get document by key."""

    try:
        res = facade.get_document(collection, key)
        return res, 200
    except gmap_exc.CollectionNotExist as err:
        return err.message, 404
    except gmap_exc.DocumentNotExist as err:
        return err.message, 404
    except Exception as err:
        return str(err), 500


@api.route('/collections/<collection>/<key>', methods=['DELETE'])
@decorators.json_response
def delete_document(collection, key):
    """Delete document by key."""

    try:
        facade.delete_document(collection, key)
        return {}, 200
    except gmap_exc.CollectionNotExist as err:
        return err.message, 404
    except gmap_exc.DocumentNotExist as err:
        return err.message, 404
    except Exception as err:
        return str(err), 500


@api.route('/collections/<collection>', methods=['GET'])
@api.route('/collections/<collection>/search', methods=['GET'])
@decorators.json_response
def search_in_collection(collection):
    """List all collections from DB."""
    field = request.args.get('field')
    value = request.args.get('value')
    offset = request.args.get('offset', 0)
    count = request.args.get('count', 10)

    try:
        res = facade.search_document(collection, field, value, offset, count)
        return res, 200
    except gmap_exc.CollectionNotExist as err:
        return err.message, 404
    except Exception as err:
        return str(err), 500


##########
# Search #
##########
@api.route('/traversal', methods=['GET'])
@decorators.json_response
def traversal():
    """Search traversal."""

    try:
        search_dict = {
            'graph_name': request.args.get('graph'),
            'start_vertex': request.args.get('start_vertex'),
            'direction': request.args.get('direction', 'outbound'),
            'item_order': request.args.get('item_order', 'forward'),
            'strategy': request.args.get('strategy', None),
            'order': request.args.get('order', None),
            'edge_uniqueness': request.args.get('edge_uniqueness', None),
            'vertex_uniqueness': request.args.get('vertex_uniqueness', None),
            'max_iter': request.args.get('max_iter', None),
            'min_depth': request.args.get('min_depth', None),
            'max_depth': request.args.get('max_depth', None),
            'init_func': request.args.get('init_func', None),
            'sort_func': request.args.get('sort_func', None),
            'filter_func': request.args.get('filter_func', None),
            'visitor_func': request.args.get('visitor_func', None),
            'expander_func': request.args.get('expander_func', None)
        }

        res = facade.search_traversal(**search_dict)
        return res, 200
    except gmap_exc.GraphNotExist as err:
        return err.message, 404
    except Exception as err:
        return str(err), 500
