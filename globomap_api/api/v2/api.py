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
from globomap_api.api.v2 import api
from globomap_api.api.v2 import blueprint
from globomap_api.api.v2.endpoints.collections import ns as coll_ns
from globomap_api.api.v2.endpoints.edges import ns as edges_ns
from globomap_api.api.v2.endpoints.graphs import ns as graphs_ns
from globomap_api.api.v2.endpoints.healthcheck import ns as healthcheck_ns
from globomap_api.api.v2.endpoints.plugin_data import ns as plugin_ns

api.add_namespace(graphs_ns)
api.add_namespace(edges_ns)
api.add_namespace(coll_ns)
api.add_namespace(plugin_ns)
api.add_namespace(healthcheck_ns)
