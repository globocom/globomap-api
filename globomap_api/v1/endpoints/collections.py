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

ns = api.namespace(
    'collections', description='Operations related to collections')


@ns.route('/')
class Collections(Resource):

    def get(self):
        """List all collections of kind document from DB."""

        try:
            collections = facade.list_collections(kind='document')
            return collections, 200

        except gmap_exc.DatabaseNotExist as err:
            api.abort(404, errors=err.message)

    def post(self):
        """Create collection of kind document in DB."""

        try:
            data = request.get_json()
            logger.debug('Receive Data: %s', data)
            facade.create_collection_document(data)
            return {}, 200

        except ValidationError as error:
            res = validate(error)
            api.abort(400, errors=res)

        except gmap_exc.CollectionNotExist as err:
            api.abort(404, errors=err.message)


@ns.route('/search/')
class Search(Resource):

    def get(self):
        """Search document in collections of kind document from DB."""

        args = pag_collections_arguments.parse_args(request)

        try:
            try:
                page = args.get('page')
                query = args.get('query') or '[]'
                per_page = args.get('per_page')
                collections = args.get('collections').split(',')
                data = json.loads(query)
                logger.debug('Receive Data: %s', data)
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


@ns.route('/<collection>/')
class Collection(Resource):

    def post(self, collection):
        """Insert document in DB."""

        try:
            data = request.get_json()
            logger.debug('Receive Data: %s', data)
            res = facade.create_document(collection, data)
            return res, 200

        except ValidationError as error:
            res = validate(error)
            api.abort(400, errors=res)

        except gmap_exc.CollectionNotExist as err:
            api.abort(404, errors=err.message)

        except gmap_exc.DocumentAlreadyExist as err:
            api.abort(409, errors=err.message)

        except gmap_exc.DocumentException as err:
            api.abort(404, errors=err.message)

    @api.expect(pagination_arguments)
    def get(self, collection):
        """Search documents from collection."""

        args = pagination_arguments.parse_args(request)

        try:
            try:
                page = args.get('page')
                query = args.get('query') or '[]'
                per_page = args.get('per_page')
                data = json.loads(query)
            except JSONDecodeError:
                raise gmap_exc.SearchException('Parameter query is invalid')
            else:
                res = facade.search(collection, data, page, per_page)
                return res, 200

        except gmap_exc.CollectionNotExist as err:
            api.abort(404, errors=err.message)

        except ValidationError as error:
            res = validate(error)
            api.abort(400, errors=res)


@ns.route('/<collection>/clear/')
class CollectionClear(Resource):

    def post(self, collection):
        """Clear documents in collection."""

        try:
            data = request.get_json()
            logger.debug('Receive Data: %s', data)
            res = facade.clear_collection(collection, data)
            return res, 200

        except gmap_exc.CollectionNotExist as err:
            api.abort(404, errors=err.message)

        except ValidationError as error:
            res = validate(error)
            api.abort(400, errors=res)


@ns.route('/<collection>/<key>/')
class Document(Resource):

    def put(self, collection, key):
        """Update document."""

        try:
            data = request.get_json()
            logger.debug('Receive Data: %s', data)
            res = facade.update_document(collection, key, data)
            return res, 200

        except ValidationError as error:
            res = validate(error)
            api.abort(400, errors=res)

        except gmap_exc.CollectionNotExist as err:
            api.abort(404, errors=err.message)

        except gmap_exc.DocumentNotExist as err:
            api.abort(404, errors=err.message)

    def patch(self, collection, key):
        """Partial update document."""

        try:
            data = request.get_json()
            logger.debug('Receive Data: %s', data)
            res = facade.patch_document(collection, key, data)
            return res, 200

        except ValidationError as error:
            res = validate(error)
            api.abort(400, errors=res)

        except gmap_exc.CollectionNotExist as err:
            api.abort(404, errors=err.message)

        except gmap_exc.DocumentNotExist as err:
            api.abort(404, errors=err.message)

    def get(self, collection, key):
        """Get document by key."""

        try:
            res = facade.get_document(collection, key)
            return res, 200

        except gmap_exc.CollectionNotExist as err:
            api.abort(404, errors=err.message)

        except gmap_exc.DocumentNotExist as err:
            api.abort(404, errors=err.message)

    def delete(self, collection, key):
        """Delete document by key."""

        try:
            facade.delete_document(collection, key)
            return {}, 200

        except gmap_exc.CollectionNotExist as err:
            api.abort(404, errors=err.message)

        except gmap_exc.DocumentNotExist as err:
            api.abort(404, errors=err.message)
