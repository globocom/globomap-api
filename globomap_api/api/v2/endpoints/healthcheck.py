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
import flask
import six
from flask import current_app as app
from flask_restplus import Resource

from globomap_api.api.v2 import api
from globomap_api.api.v2 import facade
from globomap_api.api.v2.auth.facade import Auth
from globomap_api.models.db import DB

ns = api.namespace('healthcheck', description='Healthcheck')


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
            app.logger.error(problems)
            self.representations = {}
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
        'auth': _is_auth_ok(),
        'arango': _is_arango_ok()
    }

    return deps


def _is_arango_ok():
    try:
        db = DB()
        db.get_database()
        graphs = facade.list_graphs()
        collections = facade.list_collections('document')
        edges = facade.list_collections('edge')
    except:
        app.logger.error('Failed to healthcheck arango.')
        deps = {'status': False}
    else:
        deps = {
            'status': True,
            'graphs': graphs,
            'collections': collections,
            'edges': edges
        }

    return deps


def _is_auth_ok():
    auth_inst = Auth()

    status = True
    if auth_inst.is_enable():
        status = auth_inst.is_url_ok()

    status = {
        'status': status
    }

    return status
