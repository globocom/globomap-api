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
from globomap_api.util import validate


ns = api.namespace('edges', description='Operations related to edges')


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
    @permission_classes((permissions.Read, permissions.Edge))
    def get(self):
        """List all collections of kind edge from DB."""

        collections = facade.list_collections('edge')
        return collections, 200

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found'
    })
    @api.expect(edges_parsers.post_edge_parser)
    @permission_classes((
        permissions.Write, permissions.Edge, permissions.Admin))
    def post(self):
        """Create collection of kind edge in DB."""

        edges_parsers.post_edge_parser.parse_args(request)

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
class Search(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found'
    })
    @api.expect(edges_parsers.search_all_parser)
    @permission_classes((permissions.Read, permissions.Edge))
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
    @api.expect(edges_parsers.clear_document_parser)
    @permission_classes((permissions.Write, permissions.Edge))
    def post(self, edge):
        """Clear documents in edge."""

        edges_parsers.clear_document_parser.parse_args(request)

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
    @api.expect(edges_parsers.post_document_parser)
    @permission_classes((permissions.Write, permissions.Edge))
    def post(self, edge):
        """Insert edge in DB."""

        edges_parsers.post_document_parser.parse_args(request)

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
    @permission_classes((permissions.Read, permissions.Edge))
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
class Document(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found'
    })
    @api.expect(edges_parsers.put_document_parser)
    @permission_classes((permissions.Write, permissions.Edge))
    def put(self, edge, key):
        """Update edge."""

        edges_parsers.put_document_parser.parse_args(request)

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
    @api.expect(edges_parsers.patch_document_parser)
    @permission_classes((permissions.Write, permissions.Edge))
    def patch(self, edge, key):
        """Partial update edge."""

        edges_parsers.patch_document_parser.parse_args(request)

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
    @permission_classes((permissions.Read, permissions.Edge))
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
    @permission_classes((permissions.Write, permissions.Edge))
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
