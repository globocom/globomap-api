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


log = logging.getLogger(__name__)

ns = api.namespace('edges', description='Operations related to edges')


@ns.route('/')
class Edges(Resource):

    def get(self):
        """List all collections of kind edge from DB."""

        try:
            collections = facade.list_collections('edge')
            return collections, 200

        except gmap_exc.DatabaseNotExist as err:
            api.abort(404, errors=err.message)

    def post(self):
        """Create collection of kind edge in DB."""

        try:
            data = request.get_json()
            facade.create_collection_edge(data)
            return {}, 200

        except ValidationError as error:
            res = validate(error)
            api.abort(400, errors=res)

        except gmap_exc.CollectionNotExist as err:
            api.abort(404, errors=err.message)


@ns.route('/search/')
class Search(Resource):

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
                raise gmap_exc.SearchException('Parameter search is invalid')
            else:
                res = facade.search_collections(
                    collections, data, page, per_page)
                return res, 200

        except gmap_exc.CollectionNotExist as err:
            api.abort(404, errors=err.message)

        except ValidationError as error:
            res = validate(error)
            api.abort(400, errors=res)


@ns.route('/<edge>/')
class Edge(Resource):

    def post(self, edge):
        """Insert edge in DB."""

        try:
            data = request.get_json()
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
                api.abort(400, errors='Parameter search is invalid')
            else:
                res = facade.search(edge, data, page, per_page)
                return res, 200

        except gmap_exc.CollectionNotExist as err:
            api.abort(404, errors=err.message)

        except ValidationError as error:
            res = validate(error)
            api.abort(400, errors=res)


@ns.route('/<edge>/<key>/')
class Document(Resource):

    def put(self, edge, key):
        """Update edge."""

        try:
            data = request.get_json()
            res = facade.update_edge(edge, key, data)
            return res, 200

        except ValidationError as error:
            res = validate(error)
            api.abort(400, errors=res)

        except gmap_exc.EdgeNotExist as err:
            api.abort(404, errors=err.message)

        except gmap_exc.DocumentNotExist as err:
            api.abort(404, errors=err.message)

    def patch(self, edge, key):
        """Partial update edge."""

        try:
            data = request.get_json()
            res = facade.patch_edge(edge, key, data)
            return res, 200

        except ValidationError as error:
            res = validate(error)
            api.abort(400, errors=res)

        except gmap_exc.EdgeNotExist as err:
            api.abort(404, errors=err.message)

        except gmap_exc.DocumentNotExist as err:
            api.abort(404, errors=err.message)

    def get(self, edge, key):
        """Get edge by key."""

        try:
            res = facade.get_edge(edge, key)
            return res, 200

        except gmap_exc.EdgeNotExist as err:
            api.abort(404, errors=err.message)

        except gmap_exc.DocumentNotExist as err:
            api.abort(404, errors=err.message)

    def delete(self, edge, key):
        """Delete edge by key."""

        try:
            facade.delete_edge(edge, key)
            return {}, 200

        except gmap_exc.EdgeNotExist as err:
            api.abort(404, errors=err.message)

        except gmap_exc.DocumentNotExist as err:
            api.abort(404, errors=err.message)
