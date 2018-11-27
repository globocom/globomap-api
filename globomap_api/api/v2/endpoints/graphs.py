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
from json.decoder import JSONDecodeError

from flask import current_app as app
from flask import request
from flask_restplus import Resource
from jsonspec.validators.exceptions import ValidationError

from globomap_api import exceptions as gmap_exc
from globomap_api.api.v2 import api
from globomap_api.api.v2 import facade
from globomap_api.api.v2.auth import permissions
from globomap_api.api.v2.auth.decorators import permission_classes
from globomap_api.api.v2.parsers import graphs as graphs_parsers
from globomap_api.api.v2.parsers.base import search_parser
from globomap_api.api.v2.util import get_dict
from globomap_api.api.v2.util import validate

ns = api.namespace('graphs', description='Operations related to graphs')

specs = app.config['SPECS']


@ns.route('/')
@api.header(
    'Authorization',
    'Token Authorization',
    required=True,
    default='Token token='
)
class Graph(Resource):

    @api.doc(responses={
        200: 'Success',
        401: 'Unauthorized',
        403: 'Forbidden'
    })
    @api.expect(search_parser)
    @permission_classes((permissions.Read,))
    def get(self):
        """List all graphs from DB."""

        args = search_parser.parse_args(request)

        try:
            page = args.get('page')
            per_page = args.get('per_page')
            res = facade.list_graphs(page, per_page)
        except JSONDecodeError:
            raise gmap_exc.SearchException('Parameter query is invalid')
        else:
            return res, 200

    @api.doc(responses={
        200: 'Success',
        401: 'Unauthorized',
        403: 'Forbidden',
        400: 'Validation Error',
    })
    @api.expect(api.schema_model('GraphPost', get_dict(specs.get('graphs'))))
    @permission_classes((permissions.Admin,))
    def post(self):
        """Create graph in DB."""

        try:
            data = request.get_json()
            app.logger.debug('Receive Data: %s', data)
            facade.create_graph(data)
            return {}, 200

        except ValidationError as error:
            res = validate(error)
            app.logger.error(res)
            api.abort(400, errors=res)


@ns.route('/<graph>/traversal/')
@api.doc(params={'graph': 'Name Of Graph'})
@api.header(
    'Authorization',
    'Token Authorization',
    required=True,
    default='Token token='
)
class GraphTraversal(Resource):

    @api.doc(responses={
        200: 'Success',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found'
    })
    @api.expect(graphs_parsers.traversal_parser)
    @permission_classes((permissions.Read,))
    def get(self, graph):
        """Search traversal."""

        args = graphs_parsers.traversal_parser.parse_args(request)

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

        except gmap_exc.GraphTraverseException as err:
            app.logger.error(err.message)
            api.abort(400, errors=err.message)

        except gmap_exc.GraphNotExist as err:
            app.logger.error(err.message)
            api.abort(404, errors=err.message)
