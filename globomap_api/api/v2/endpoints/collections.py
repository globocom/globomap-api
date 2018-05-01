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
from globomap_api.api.v2.parsers import collections as coll_parsers
from globomap_api.config import SPECS
from globomap_api.util import get_dict
from globomap_api.util import validate

ns = api.namespace(
    'collections', description='Operations related to collections')


@ns.route('/')
@api.header(
    'Authorization',
    'Token Authorization',
    required=True,
    default='Token token='
)
class Collections(Resource):

    @api.doc(responses={
        200: 'Success',
        401: 'Unauthorized',
        403: 'Forbidden',
    })
    @permission_classes((permissions.Read, permissions.Collection))
    def get(self):
        """List all collections of kind document from DB."""

        collections = facade.list_collections(kind='document')
        return collections, 200

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found'
    })
    @api.expect(api.schema_model('Collections',
                                 get_dict(SPECS.get('collections'))))
    @permission_classes((permissions.Write, permissions.Collection,
                         permissions.Admin))
    def post(self):
        """Create collection of kind document in DB."""

        try:
            data = request.get_json()

            app.logger.debug('Receive Data: %s', data)
            facade.create_collection_document(data)
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
    @api.expect(coll_parsers.search_all_parser)
    @permission_classes((permissions.Read, permissions.Collection))
    def get(self):
        """Search document in collections of kind document from DB."""

        args = coll_parsers.search_all_parser.parse_args(request)

        try:
            try:
                page = args.get('page')
                query = args.get('query') or '[]'
                per_page = args.get('per_page')
                collections = args.get('collections').split(',')
                data = json.loads(query)
                app.logger.debug('Receive Data: %s', data)
            except JSONDecodeError:
                raise gmap_exc.SearchException('Parameter query is invalid')
            else:
                res = facade.search_collections(
                    collections, data, page, per_page)
                return res, 200

        except gmap_exc.CollectionNotExist as err:
            app.logger.error(err.message)
            api.abort(404, errors=err.message)

        except ValidationError as error:
            res = validate(error)
            app.logger.error(res)
            api.abort(400, errors=res)


@ns.route('/<collection>/')
@api.doc(params={'collection': 'Name Of Collection'})
@api.header(
    'Authorization',
    'Token Authorization',
    required=True,
    default='Token token='
)
class Collection(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        409: 'Document Already Exists'
    })
    @api.expect(api.schema_model('DocumentPost',
                                 get_dict(SPECS.get('documents'))))
    @permission_classes((permissions.Write, permissions.Collection))
    def post(self, collection):
        """Insert document in DB."""

        try:
            data = request.get_json()
            app.logger.debug('Receive Data: %s', data)
            res = facade.create_document(collection, data)
            return res, 200

        except ValidationError as error:
            res = validate(error)
            app.logger.error(res)
            api.abort(400, errors=res)

        except gmap_exc.CollectionNotExist as err:
            app.logger.error(err.message)
            api.abort(404, errors=err.message)

        except gmap_exc.DocumentAlreadyExist as err:
            app.logger.warning(err.message)
            api.abort(409, errors=err.message)

        except gmap_exc.DocumentException as err:
            app.logger.error(err.message)
            api.abort(400, errors=err.message)

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        409: 'Document Already Exists'
    })
    @api.expect(coll_parsers.search_parser)
    @permission_classes((permissions.Read, permissions.Collection))
    def get(self, collection):
        """Search documents from collection."""

        args = coll_parsers.search_parser.parse_args(request)

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
            app.logger.error(err.message)
            api.abort(404, errors=err.message)

        except ValidationError as error:
            res = validate(error)
            app.logger.error(res)
            api.abort(400, errors=res)


@ns.route('/<collection>/clear/')
@api.doc(params={'collection': 'Name Of Collection'})
@api.header(
    'Authorization',
    'Token Authorization',
    required=True,
    default='Token token='
)
class CollectionClear(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found'
    })
    @api.expect(api.schema_model('DocumentClear',
                                 get_dict(SPECS.get('clear'))))
    @permission_classes((permissions.Write, permissions.Collection))
    def post(self, collection):
        """Clear documents in collection."""

        try:
            data = request.get_json()
            app.logger.debug('Receive Data: %s', data)
            res = facade.clear_collection(collection, data)
            return res, 200

        except gmap_exc.CollectionNotExist as err:
            app.logger.error(err.message)
            api.abort(404, errors=err.message)

        except ValidationError as error:
            res = validate(error)
            app.logger.error(res)
            api.abort(400, errors=res)


@ns.route('/<collection>/<key>/')
@api.doc(params={
    'collection': 'Name Of Collection',
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
    @api.expect(api.schema_model('DocumentPut',
                                 get_dict(SPECS.get('documents'))))
    @permission_classes((permissions.Write, permissions.Collection))
    def put(self, collection, key):
        """Update document."""

        try:
            data = request.get_json()
            app.logger.debug('Receive Data: %s', data)
            res = facade.update_document(collection, key, data)
            return res, 200

        except ValidationError as error:
            res = validate(error)
            app.logger.error(res)
            api.abort(400, errors=res)

        except gmap_exc.CollectionNotExist as err:
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
    @api.expect(api.schema_model('DocumentPatch',
                                 get_dict(SPECS.get('documents_partial'))))
    @permission_classes((permissions.Write, permissions.Collection))
    def patch(self, collection, key):
        """Partial update document."""

        try:
            data = request.get_json()
            app.logger.debug('Receive Data: %s', data)
            res = facade.patch_document(collection, key, data)
            return res, 200

        except ValidationError as error:
            res = validate(error)
            app.logger.error(res)
            api.abort(400, errors=res)

        except gmap_exc.CollectionNotExist as err:
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
    @permission_classes((permissions.Read, permissions.Collection))
    def get(self, collection, key):
        """Get document by key."""

        try:
            res = facade.get_document(collection, key)
            return res, 200

        except gmap_exc.CollectionNotExist as err:
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
    @permission_classes((permissions.Write, permissions.Collection))
    def delete(self, collection, key):
        """Delete document by key."""

        try:
            facade.delete_document(collection, key)
            return {}, 200

        except gmap_exc.CollectionNotExist as err:
            app.logger.error(err.message)
            api.abort(404, errors=err.message)

        except gmap_exc.DocumentNotExist as err:
            app.logger.warning(err.message)
            api.abort(404, errors=err.message)
