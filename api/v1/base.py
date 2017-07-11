from flask import request
from . import api
from ..decorators import json_response


@api.route('/search/', methods=['GET'])
@json_response
def search_elements():
    return {}, 200


@api.route('/<name>/', methods=['GET'])
@json_response
def get_element(name):
    return {}, 200


@api.route('/<name>/', methods=['POST'])
@json_response
def create_element(name):
    return {}, 201


@api.route('/<name>/<int:id>/', methods=['PUT'])
@json_response
def update_element(name, id):
    return {}, 200


@api.route('/<name>/<int:id>/', methods=['DELETE'])
@json_response
def delete_element(name, id):
    return {}, 200
