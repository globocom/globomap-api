from . import api
from ..decorators import json_response
from ..models.db import DB


@api.route('/graphs', methods=['GET'])
@json_response
def list_graphs():
    """List all graphs from DB."""

    db_inst = DB()
    graphs = db_inst.database.graphs()
    return graphs, 200


@api.route('/collections/', methods=['GET'])
@json_response
def list_collections():
    """List all collections from DB."""

    db_inst = DB()
    colls = [coll for coll in db_inst.database.collections()
             if coll['system'] is False and coll['type'] == 'document']
    return colls, 200


@api.route('/edges/', methods=['GET'])
@json_response
def list_edges():
    """List all collections from DB."""

    db_inst = DB()
    colls = [coll for coll in db_inst.database.collections()
             if coll['system'] is False and coll['type'] == 'edge']

    return colls, 200

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
