# -*- coding: utf-8 -*-
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
import logging

import flask
import six
from flask_restplus import Resource
from flask_restplus.representations import output_json

from globomap_api.api import facade
from globomap_api.api.v2 import api
from globomap_api.models.db import DB
from globomap_api.models.redis import RedisClient

ns = api.namespace('healthcheck', description='Healthcheck')
logger = logging.getLogger(__name__)


def text(data, code, headers=None):
    return flask.make_response(six.text_type(data))


@ns.route('/')
class Healthcheck(Resource):
    representations = {
        'text/plain': text,
    }

    @api.doc(responses={
        200: 'Success',
        503: 'Service Unavailable',
    })
    def get(self):
        deps = _list_deps()
        problems = {}
        for key in deps:
            if deps[key].get('status') is False:
                problems.update({key: deps[key]})
        if problems:
            return problems, 503
        return 'WORKING', 200


@ns.route('/deps/')
class HealthcheckDeps(Resource):

    @api.doc(responses={200: 'Success'})
    def get(self):
        deps = _list_deps()
        return deps, 200


def _list_deps():
    deps = {
        'redis': _is_redis_ok(),
        'arango': _is_arango_ok()
    }

    return deps


def _is_redis_ok():
    try:
        conn = RedisClient().get_redis_conn()
    except:
        logger.error('Failed to healthcheck redis.')
        return {'status': False}
    else:
        if not conn.ping():
            logger.error('Failed to healthcheck redis.')
            return {'status': False}
        else:
            return {'status': True}


def _is_arango_ok():
    try:
        db = DB()
        db.get_database()
        graphs = facade.list_graphs()
        collections = facade.list_collections('document')
        edges = facade.list_collections('edge')
    except:
        logger.error('Failed to healthcheck arango.')
        deps = {'status': False}
    else:
        deps = {
            'status': True,
            'graphs': graphs,
            'collections': collections,
            'edges': edges
        }

    return deps
