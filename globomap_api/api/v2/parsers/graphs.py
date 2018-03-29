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


traversal_parser = reqparse.RequestParser()
traversal_parser.add_argument(
    'start_vertex',
    type=str,
    required=True,
    help='Start Vertex'
)
traversal_parser.add_argument(
    'direction',
    type=str,
    required=False,
    choices=['outbound', 'inbound', 'any'],
    default='outbound',
    help='Direction'
)
traversal_parser.add_argument(
    'item_order',
    type=str,
    required=False,
    choices=['forward', 'backward'],
    default='forward',
    help='Item Order'
)
traversal_parser.add_argument(
    'strategy',
    type=str,
    required=False,
    choices=['dfs', 'bfs'],
    default='dfs',
    help='Strategy'
)
traversal_parser.add_argument(
    'order',
    type=str,
    required=False,
    choices=['preorder', 'postorder',
             'preorder-expander'],
    default=None,
    help='Order'
)
traversal_parser.add_argument(
    'edge_uniqueness',
    type=str,
    required=False,
    choices=['global', 'path'],
    default=None,
    help='Edge Uniqueness'
)
traversal_parser.add_argument(
    'vertex_uniqueness',
    type=str,
    required=False,
    choices=['global', 'path'],
    default=None,
    help='Vertex Uniqueness'
)
traversal_parser.add_argument(
    'max_iter',
    type=int,
    required=False,
    default=None,
    help='Max Iteration'
)
traversal_parser.add_argument(
    'min_depth',
    type=int,
    required=False,
    default=None,
    help='Min Depth'
)
traversal_parser.add_argument(
    'max_depth',
    type=int,
    required=False,
    default=1,
    help='Max Depth'
)
traversal_parser.add_argument(
    'init_func',
    type=str,
    required=False,
    default=None, help='Init Func')
traversal_parser.add_argument(
    'sort_func',
    type=str,
    required=False,
    default=None,
    help='Sort Function'
)
traversal_parser.add_argument(
    'filter_func',
    type=str,
    required=False,
    default=None,
    help='Filter Function'
)
traversal_parser.add_argument(
    'visitor_func',
    type=str,
    required=False,
    default=None,
    help='Visitor Function'
)
traversal_parser.add_argument(
    'expander_func',
    type=str,
    required=False,
    default=None,
    help='Expander Function'
)

post_graph_parser = reqparse.RequestParser()
post_graph_parser.add_argument(
    'data',
    type=str,
    required=True,
    help='Graph',
    location='json'
)
