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
import json
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
from globomap_api.api.v2.parsers import edges as edges_parsers
from globomap_api.api.v2.parsers.base import search_parser
from globomap_api.api.v2.util import get_dict
from globomap_api.api.v2.util import validate

ns = api.namespace('edges', description='Operations related to edges')

specs = app.config['SPECS']


@ns.route('/')
@api.header(
    'Authorization',
    'Token Authorization',
    required=True,
    default='Token token='
)
class Edges(Resource):

    @api.doc(responses={
        200: 'Success',
        401: 'Unauthorized',
        403: 'Forbidden',
    })
    @api.expect(search_parser)
    @permission_classes((permissions.Read,))
    def get(self):
        """List all collections of kind edge from DB."""

        args = search_parser.parse_args(request)

        try:
            page = args.get('page')
            per_page = args.get('per_page')
            res = facade.list_collections('edge', page, per_page)
        except JSONDecodeError:
            raise gmap_exc.SearchException('Parameter query is invalid')
        else:
            return res, 200

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found'
    })
    @api.expect(api.schema_model('Edge', get_dict(specs.get('collections'))))
    @permission_classes((permissions.Admin,))
    def post(self):
        """Create collection of kind edge in DB."""

        try:
            data = request.get_json()
            app.logger.debug('Receive Data: %s', data)
            facade.create_collection_edge(data)
            return {}, 200

        except ValidationError as error:
            res = validate(error)
            app.logger.error(res)
            api.abort(400, errors=res)

        except gmap_exc.CollectionNotExist as err:
            app.logger.error(err.message)
            api.abort(404, errors=err.message)


@ns.route('/search/')
@api.header(
    'Authorization',
    'Token Authorization',
    required=True,
    default='Token token='
)
class EdgeSearch(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found'
    })
    @api.expect(edges_parsers.search_all_parser)
    @permission_classes((permissions.Read,))
    def get(self):
        """Search edge in collections of kind edge from DB."""

        args = edges_parsers.search_all_parser.parse_args(request)

        try:
            try:
                page = args.get('page')
                query = args.get('query') or '[]'
                per_page = args.get('per_page')
                edges = args.get('edges').split(',')
                data = json.loads(query)
            except JSONDecodeError:
                raise gmap_exc.SearchException('Parameter query is invalid')
            else:
                res = facade.search_collections(
                    edges, data, page, per_page)
                return res, 200

        except gmap_exc.CollectionNotExist as err:
            app.logger.error(err.message)
            api.abort(404, errors=err.message)

        except ValidationError as error:
            res = validate(error)
            app.logger.error(res)
            api.abort(400, errors=res)


@ns.route('/<edge>/clear/')
@api.header(
    'Authorization',
    'Token Authorization',
    required=True,
    default='Token token='
)
@api.doc(params={'edge': 'Name Of Edge(Collection)'})
class EdgeClear(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found'
    })
    @api.expect(api.schema_model('EdgeClear', get_dict(specs.get('clear'))))
    @permission_classes((permissions.Write,))
    def post(self, edge):
        """Clear documents in edge."""

        try:
            data = request.get_json()
            app.logger.debug('Receive Data: %s', data)
            res = facade.clear_collection(edge, data)
            return res, 200

        except gmap_exc.CollectionNotExist as err:
            app.logger.error(err.message)
            api.abort(404, errors=err.message)

        except ValidationError as error:
            res = validate(error)
            app.logger.error(res)
            api.abort(400, errors=res)


@ns.route('/<edge>/')
@api.header(
    'Authorization',
    'Token Authorization',
    required=True,
    default='Token token='
)
@api.doc(params={'edge': 'Name Of Edge(Collection)'})
class Edge(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        409: 'Document Already Exists'
    })
    @api.expect(api.schema_model('EdgePost', get_dict(specs.get('edges'))))
    @permission_classes((permissions.Write,))
    def post(self, edge):
        """Insert edge in DB."""

        try:
            data = request.get_json()
            app.logger.debug('Receive Data: %s', data)
            res = facade.create_edge(edge, data)
            return res, 200

        except gmap_exc.EdgeNotExist as err:
            app.logger.error(err.message)
            api.abort(404, errors=err.message)

        except gmap_exc.DocumentAlreadyExist as err:
            app.logger.warning(err.message)
            api.abort(409, errors=err.message)

        except ValidationError as error:
            res = validate(error)
            app.logger.error(res)
            api.abort(400, errors=res)

        except gmap_exc.DocumentException as err:
            api.abort(400, errors=err.message)

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found'
    })
    @api.expect(edges_parsers.search_parser)
    @permission_classes((permissions.Read,))
    def get(self, edge):
        """Search documents from collection."""

        args = edges_parsers.search_parser.parse_args(request)

        try:
            try:
                page = args.get('page')
                query = args.get('query') or '[]'
                per_page = args.get('per_page')
                data = json.loads(query)
            except JSONDecodeError:
                api.abort(400, errors='Parameter query is invalid')
            else:
                res = facade.search(edge, data, page, per_page)
                return res, 200

        except gmap_exc.CollectionNotExist as err:
            app.logger.error(err.message)
            api.abort(404, errors=err.message)

        except ValidationError as error:
            res = validate(error)
            app.logger.error(res)
            api.abort(400, errors=res)


@ns.route('/<edge>/<key>/')
@api.doc(params={
    'edge': 'Name Of Edge(Collection)',
    'key': 'Key Of Document'
})
@api.header(
    'Authorization',
    'Token Authorization',
    required=True,
    default='Token token='
)
class DocumentEdge(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found'
    })
    @api.expect(api.schema_model('EdgePut', get_dict(specs.get('edges'))))
    @permission_classes((permissions.Write,))
    def put(self, edge, key):
        """Update edge."""

        try:
            data = request.get_json()
            app.logger.debug('Receive Data: %s', data)
            res = facade.update_edge(edge, key, data)
            return res, 200

        except ValidationError as error:
            res = validate(error)
            app.logger.error(res)
            api.abort(400, errors=res)

        except gmap_exc.EdgeNotExist as err:
            app.logger.error(err.message)
            api.abort(404, errors=err.message)

        except gmap_exc.DocumentNotExist as err:
            app.logger.warning(err.message)
            api.abort(404, errors=err.message)

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found'
    })
    @api.expect(api.schema_model('EdgePatch',
                                 get_dict(specs.get('edges_partial'))))
    @permission_classes((permissions.Write,))
    def patch(self, edge, key):
        """Partial update edge."""

        try:
            data = request.get_json()
            app.logger.debug('Receive Data: %s', data)
            res = facade.patch_edge(edge, key, data)
            return res, 200

        except ValidationError as error:
            res = validate(error)
            app.logger.error(res)
            api.abort(400, errors=res)

        except gmap_exc.EdgeNotExist as err:
            app.logger.error(err.message)
            api.abort(404, errors=err.message)

        except gmap_exc.DocumentNotExist as err:
            app.logger.warning(err.message)
            api.abort(404, errors=err.message)

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found'
    })
    @permission_classes((permissions.Read,))
    def get(self, edge, key):
        """Get edge by key."""

        try:
            res = facade.get_edge(edge, key)
            return res, 200

        except gmap_exc.EdgeNotExist as err:
            app.logger.error(err.message)
            api.abort(404, errors=err.message)

        except gmap_exc.DocumentNotExist as err:
            app.logger.warning(err.message)
            api.abort(404, errors=err.message)

    @api.doc(responses={
        200: 'Success',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found'
    })
    @permission_classes((permissions.Write,))
    def delete(self, edge, key):
        """Delete edge by key."""

        try:
            facade.delete_edge(edge, key)
            return {}, 200

        except gmap_exc.EdgeNotExist as err:
            app.logger.error(err.message)
            api.abort(404, errors=err.message)

        except gmap_exc.DocumentNotExist as err:
            app.logger.warning(err.message)
            api.abort(404, errors=err.message)
