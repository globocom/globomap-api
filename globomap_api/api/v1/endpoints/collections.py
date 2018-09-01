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
import logging
from json.decoder import JSONDecodeError

from flask import request
from flask_restplus import Resource
from jsonspec.validators.exceptions import ValidationError

from globomap_api import exceptions as gmap_exc
from globomap_api.api import facade
from globomap_api.api.parsers import pagination_arguments
from globomap_api.api.v1 import api
from globomap_api.util import validate

logger = logging.getLogger(__name__)

ns = api.namespace(
    'collections', description='Operations related to collections')


@ns.deprecated
@ns.route('/<collection>/')
@api.doc(params={'collection': 'Name Of Collection'})
class Collection(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        404: 'Not Found'
    })
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
