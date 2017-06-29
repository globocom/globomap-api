from flask import request
from . import api
from ..decorators import json_response


@api.route('/pools/', methods=['GET'])
@json_response
def get_pools():
    return {}, 200


@api.route('/pools/<int:id>', methods=['GET'])
@json_response
def get_pool(id):
    return {}, 200


@api.route('/pools/', methods=['POST'])
@json_response
def create_pool():
    return {}, 201


@api.route('/pools/<int:id>', methods=['PUT'])
@json_response
def update_pool(id):
    return {}, 200


@api.route('/pools/<int:id>', methods=['DELETE'])
@json_response
def delete_pool(id):
    return {}, 200
