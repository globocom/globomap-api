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
from flask.cli import AppGroup

from globomap_api import config as app_config
from globomap_api import exceptions
from globomap_api.models.constructor import Constructor
from globomap_api.wsgi import application
meta_cli = AppGroup('meta')


@meta_cli.command('create')
def create_meta_collections():
    """Creates meta collections."""
    constructor = Constructor()

    try:
        constructor.factory(kind='Collection', create=True,
                            name=app_config.META_COLLECTION,
                            create_indexes=False)
    except exceptions.CollectionAlreadyExist:
        pass

    try:
        constructor.factory(kind='Collection', create=True,
                            name=app_config.META_GRAPH,
                            create_indexes=False)
    except exceptions.CollectionAlreadyExist:
        pass

    try:
        constructor.factory(kind='Collection', create=True,
                            name=app_config.META_QUERY,
                            create_indexes=False)
    except exceptions.CollectionAlreadyExist:
        pass

    try:
        constructor.factory(kind='Collection', create=True,
                            name=app_config.INTERNAL_METADATA,
                            create_indexes=False)
    except exceptions.CollectionAlreadyExist:
        pass

application.cli.add_command(meta_cli)
