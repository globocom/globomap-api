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
__all__ = ['api', 'blueprint']

from globomap_api.api.v1 import api
from globomap_api.api.v1 import blueprint
from globomap_api.api.v1.endpoints.collections import ns as collections_namespace
from globomap_api.api.v1.endpoints.edges import ns as edges_namespace

api.add_namespace(edges_namespace)
api.add_namespace(collections_namespace)
