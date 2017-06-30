from flask import request
from . import api
from ..decorators import json_response


@api.route('/vips/', methods=['GET'])
@json_response
def get_vips():
    return {}, 200


@api.route('/vips/<int:id>', methods=['GET'])
@json_response
def get_vip(id):
    return {}, 200


@api.route('/vips/', methods=['POST'])
@json_response
def create_vip():
    return {}, 201


@api.route('/vips/<int:id>', methods=['PUT'])
@json_response
def update_vip(id):
    return {}, 200


@api.route('/vips/<int:id>', methods=['DELETE'])
@json_response
def delete_vip(id):
    return {}, 200
