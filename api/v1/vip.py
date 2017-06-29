from flask import request
from . import api


@api.route('/vips/', methods=['GET']):
def get_vips():
    return [], 200


@api.route('/vips/<int:id>', methods=['GET']):
def get_vip(id):
    return [], 200


@api.route('/vips/', methods=['POST']):
def create_vip():
    return [], 201


@api.route('/vips/<int:id>', methods=['PUT']):
def update_vip(id):
    return [], 200


@api.route('/vips/<int:id>', methods=['DELETE']):
def delete_vip(id):
    return [], 200
