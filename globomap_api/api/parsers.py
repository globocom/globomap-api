"""
   Copyright 2018 Globo.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from flask_restplus import reqparse

pag_collections_arguments = reqparse.RequestParser()
pag_collections_arguments.add_argument(
    'page',
    type=int,
    required=False,
    default=1,
    help='Page number'
)
pag_collections_arguments.add_argument(
    'per_page',
    type=int,
    required=False,
    default=10,
    help='Items number per page'
)
pag_collections_arguments.add_argument(
    'query',
    type=str,
    required=False,
    default='[[{"field":"name","operator":"LIKE","value":""}]]',
    help='Query'
)
pag_collections_arguments.add_argument(
    'collections',
    type=str,
    required=True,
    default='',
    help='Collections'
)
pag_collections_arguments.add_argument(
    'Authorization',
    type=str,
    required=True,
    default='Token token=',
    location='headers'
)

pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument(
    'page',
    type=int,
    required=False,
    default=1,
    help='Page number'
)
pagination_arguments.add_argument(
    'per_page',
    type=int,
    required=False,
    default=10,
    help='Items number per page'
)
pagination_arguments.add_argument(
    'query',
    type=str,
    required=False,
    default='[[{"field":"name","operator":"LIKE","value":""}]]',
    help='Query'
)

plugin_arguments = reqparse.RequestParser()
plugin_arguments.add_argument(
    'ips',
    type=str,
    required=False,
    help='IPs'
)
plugin_arguments.add_argument(
    'graphid',
    type=int,
    required=False,
    help='Id of Graph'
)
plugin_arguments.add_argument(
    'encoded',
    type=int,
    required=False,
    default=0, help='Encode Image Base64'
)

traversal_arguments = reqparse.RequestParser()
traversal_arguments.add_argument(
    'start_vertex',
    type=str,
    required=True,
    help='Start Vertex'
)
traversal_arguments.add_argument(
    'direction',
    type=str,
    required=False,
    choices=['outbound', 'inbound', 'any'],
    default='outbound',
    help='Direction'
)
traversal_arguments.add_argument(
    'item_order',
    type=str,
    required=False,
    choices=['forward', 'backward'],
    default='forward',
    help='Item Order'
)
traversal_arguments.add_argument(
    'strategy',
    type=str,
    required=False,
    choices=['dfs', 'bfs'],
    default='dfs',
    help='Strategy'
)
traversal_arguments.add_argument(
    'order',
    type=str,
    required=False,
    choices=['preorder', 'postorder',
             'preorder-expander'],
    default=None,
    help='Order'
)
traversal_arguments.add_argument(
    'edge_uniqueness',
    type=str,
    required=False,
    choices=['global', 'path'],
    default=None,
    help='Edge_uniqueness'
)
traversal_arguments.add_argument(
    'vertex_uniqueness',
    type=str,
    required=False,
    choices=['global', 'path'],
    default=None,
    help='Vertex_uniqueness'
)
traversal_arguments.add_argument(
    'max_iter',
    type=int,
    required=False,
    default=None,
    help='max_iter'
)
traversal_arguments.add_argument(
    'min_depth',
    type=int,
    required=False,
    default=None,
    help='min_depth'
)
traversal_arguments.add_argument(
    'max_depth',
    type=int,
    required=False,
    default=1,
    help='max_depth'
)
traversal_arguments.add_argument(
    'init_func',
    type=str,
    required=False,
    default=None, help='init_func')
traversal_arguments.add_argument(
    'sort_func',
    type=str,
    required=False,
    default=None,
    help='sort_func'
)
traversal_arguments.add_argument(
    'filter_func',
    type=str,
    required=False,
    default=None,
    help='filter_func'
)
traversal_arguments.add_argument(
    'visitor_func',
    type=str,
    required=False,
    default=None,
    help='visitor_func'
)
traversal_arguments.add_argument(
    'expander_func',
    type=str,
    required=False,
    default=None,
    help='expander_func'
)
