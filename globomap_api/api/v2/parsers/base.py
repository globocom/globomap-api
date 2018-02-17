import logging

from flask import session
from flask_restplus import reqparse

from globomap_api import exceptions
from globomap_api.api.v2.keystone.keystone_auth import KeystoneAuth
from globomap_api.config import KEYSTONE_AUTH_ENABLE


search_parser = reqparse.RequestParser()
search_parser.add_argument(
    'page',
    type=int,
    required=False,
    default=1,
    help='Page number'
)
search_parser.add_argument(
    'per_page',
    type=int,
    required=False,
    default=10,
    help='Items number per page'
)
search_parser.add_argument(
    'query',
    type=str,
    required=False,
    default='[[{"field":"name","operator":"LIKE","value":""}]]',
    help='Query'
)
