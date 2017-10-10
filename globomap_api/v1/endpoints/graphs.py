"""
   Copyright 2017 Globo.com

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
# -*- coding: utf-8 -*-
import logging

from flask import request
from flask_restplus import Resource
from jsonspec.validators.exceptions import ValidationError

from globomap_api import exceptions as gmap_exc
from globomap_api.util import validate
from globomap_api.v1 import api
from globomap_api.v1 import facade
from globomap_api.v1.parsers import traversal_arguments


log = logging.getLogger(__name__)

ns = api.namespace('graphs', description='Operations related to graphs')


@ns.route('/')
class Graph(Resource):

    def get(self):
        """List all graphs from DB."""

        try:
            graphs = facade.list_graphs()
            return graphs, 200

        except gmap_exc.DatabaseNotExist as err:
            api.abort(404, errors=err.message)

    def post(self):
        """Create graph in DB."""

        try:
            data = request.get_json()
            facade.create_graph(data)
            return {}, 200

        except ValidationError as error:
            res = validate(error)
            api.abort(400, errors=res)


@ns.route('/<graph>/traversal/')
class GraphTraversal(Resource):

    @api.expect(traversal_arguments)
    def get(self, graph):
        """Search traversal."""

        args = traversal_arguments.parse_args(request)

        try:
            search_dict = {
                'graph_name': graph,
                'start_vertex': args.get('start_vertex'),
                'direction': args.get('direction'),
                'item_order': args.get('item_order'),
                'strategy': args.get('strategy'),
                'order': args.get('order'),
                'edge_uniqueness': args.get('edge_uniqueness'),
                'vertex_uniqueness': args.get('vertex_uniqueness'),
                'max_iter': args.get('max_iter'),
                'min_depth': args.get('min_depth'),
                'max_depth': args.get('max_depth'),
                'init_func': args.get('init_func'),
                'sort_func': args.get('sort_func'),
                'filter_func': args.get('filter_func'),
                'visitor_func': args.get('visitor_func'),
                'expander_func': args.get('expander_func')
            }

            res = facade.search_traversal(**search_dict)
            return res, 200

        except gmap_exc.GraphNotExist as err:
            api.abort(404, errors=err.message)
