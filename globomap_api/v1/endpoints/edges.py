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
import json
import logging
from json.decoder import JSONDecodeError

from flask import request
from flask_restplus import Resource
from jsonspec.validators.exceptions import ValidationError

from globomap_api import exceptions as gmap_exc
from globomap_api.util import validate
from globomap_api.v1 import api
from globomap_api.v1 import facade
from globomap_api.v1.parsers import pag_collections_arguments
from globomap_api.v1.parsers import pagination_arguments


logger = logging.getLogger(__name__)

ns = api.namespace('edges', description='Operations related to edges')


@ns.route('/')
class Edges(Resource):

    @api.doc(responses={200: 'Success'})
    def get(self):
        """List all collections of kind edge from DB."""

        collections = facade.list_collections('edge')
        return collections, 200

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        404: 'Not Found'
    })
    def post(self):
        """Create collection of kind edge in DB."""

        try:
            data = request.get_json()
            logger.debug('Receive Data: %s', data)
            facade.create_collection_edge(data)
            return {}, 200

        except ValidationError as error:
            res = validate(error)
            api.abort(400, errors=res)

        except gmap_exc.CollectionNotExist as err:
            api.abort(404, errors=err.message)


@ns.route('/search/')
class Search(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        404: 'Not Found'
    })
    @api.expect(pag_collections_arguments)
    def get(self):
        """Search edge in collections of kind edge from DB."""

        args = pag_collections_arguments.parse_args(request)

        try:
            try:
                page = args.get('page')
                query = args.get('query') or '[]'
                per_page = args.get('per_page')
                collections = args.get('collections').split(',')
                data = json.loads(query)
            except JSONDecodeError:
                raise gmap_exc.SearchException('Parameter query is invalid')
            else:
                res = facade.search_collections(
                    collections, data, page, per_page)
                return res, 200

        except gmap_exc.CollectionNotExist as err:
            api.abort(404, errors=err.message)

        except ValidationError as error:
            res = validate(error)
            api.abort(400, errors=res)


@ns.route('/<edge>/clear/')
@api.doc(params={'edge': 'Name Of Edge(Collection)'})
class EdgeClear(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        404: 'Not Found'
    })
    def post(self, edge):
        """Clear documents in edge."""

        try:
            data = request.get_json()
            logger.debug('Receive Data: %s', data)
            res = facade.clear_collection(edge, data)
            return res, 200

        except gmap_exc.CollectionNotExist as err:
            api.abort(404, errors=err.message)

        except ValidationError as error:
            res = validate(error)
            api.abort(400, errors=res)


@ns.route('/<edge>/')
@api.doc(params={'edge': 'Name Of Edge(Collection)'})
class Edge(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        404: 'Not Found',
        409: 'Document Already Exists'
    })
    def post(self, edge):
        """Insert edge in DB."""

        try:
            data = request.get_json()
            logger.debug('Receive Data: %s', data)
            res = facade.create_edge(edge, data)
            return res, 200

        except gmap_exc.EdgeNotExist as err:
            api.abort(404, errors=err.message)

        except gmap_exc.DocumentAlreadyExist as err:
            api.abort(409, errors=err.message)

        except ValidationError as error:
            res = validate(error)
            api.abort(400, errors=res)

        except gmap_exc.DocumentException as err:
            api.abort(400, errors=err.message)

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        404: 'Not Found'
    })
    @api.expect(pagination_arguments)
    def get(self, edge):
        """Search documents from collection."""

        args = pagination_arguments.parse_args(request)

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
            api.abort(404, errors=err.message)

        except ValidationError as error:
            res = validate(error)
            api.abort(400, errors=res)


@ns.route('/<edge>/<key>/')
@api.doc(params={
    'edge': 'Name Of Edge(Collection)',
    'key': 'Key Of Document'
})
class Document(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        404: 'Not Found'
    })
    def put(self, edge, key):
        """Update edge."""

        try:
            data = request.get_json()
            logger.debug('Receive Data: %s', data)
            res = facade.update_edge(edge, key, data)
            return res, 200

        except ValidationError as error:
            res = validate(error)
            api.abort(400, errors=res)

        except gmap_exc.EdgeNotExist as err:
            api.abort(404, errors=err.message)

        except gmap_exc.DocumentNotExist as err:
            api.abort(404, errors=err.message)

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        404: 'Not Found'
    })
    def patch(self, edge, key):
        """Partial update edge."""

        try:
            data = request.get_json()
            logger.debug('Receive Data: %s', data)
            res = facade.patch_edge(edge, key, data)
            return res, 200

        except ValidationError as error:
            res = validate(error)
            api.abort(400, errors=res)

        except gmap_exc.EdgeNotExist as err:
            api.abort(404, errors=err.message)

        except gmap_exc.DocumentNotExist as err:
            api.abort(404, errors=err.message)

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        404: 'Not Found'
    })
    def get(self, edge, key):
        """Get edge by key."""

        try:
            res = facade.get_edge(edge, key)
            return res, 200

        except gmap_exc.EdgeNotExist as err:
            api.abort(404, errors=err.message)

        except gmap_exc.DocumentNotExist as err:
            api.abort(404, errors=err.message)

    @api.doc(responses={
        200: 'Success',
        404: 'Not Found'
    })
    def delete(self, edge, key):
        """Delete edge by key."""

        try:
            facade.delete_edge(edge, key)
            return {}, 200

        except gmap_exc.EdgeNotExist as err:
            api.abort(404, errors=err.message)

        except gmap_exc.DocumentNotExist as err:
            api.abort(404, errors=err.message)
