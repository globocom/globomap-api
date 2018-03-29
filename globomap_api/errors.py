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
DOCUMENT = {
    1210: 'Cannot create document {}, document already created.',
    1202: 'Cannot update document {}, document not found.',
    0: 'Cannot create document {}. Error {}'
}

DATABASE = {
    1228: 'Database {} not found.',
    1207: 'Cannot create database {}, duplicate name.',
    1203: 'Collection {} not found.',
    0: 'Database {}. Error: {}',
    1: 'Error in search: {}',
}

COLLECTION = {
    1228: 'Collection {} not found.',
    1207: 'Cannot create collection {}, duplicate name.',
    0: 'Collection {}. Error: {}',
}

EDGE = {
    1228: 'Edge {} not found.',
    1207: 'Cannot create edge {}, duplicate name.',
    0: 'Edge {}. Error: {}',
}

GRAPH = {
    1924: 'Graph {} not found.',
    1925: 'Cannot create graph {}, duplicate name.',
    0: 'Graph {}. Error: {}',
    1: 'Error to create edge definition in graph {}. Error: {}'
}

GRAPH_TRAVERSE = {
    1202: 'Invalid startVertex.',
    0: 'Graph {}. Error: {}',
}
