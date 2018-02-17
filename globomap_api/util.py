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
import json

from jsonspec.reference import resolve
from jsonspec.validators import load

from globomap_api.models.constructor import Constructor


def json_validate(json_file):

    with open(json_file) as data_file:
        data = json.load(data_file)
        validator = load(data)

    return validator


def validate(error):
    msg = list()
    if error.flatten():
        for pointer, reasons in error.flatten().items():
            msg.append({
                'error_pointer': pointer,
                'error_reasons': list(reasons)
            })
    else:
        msg.append({
            'error_pointer': error[0],
            'error_reasons': list(error[1])
        })
    return msg


def filter_transversal(data):
    edges = []
    nodes = []
    for p in data.get('paths'):
        edges += p.get('edges', [])
        nodes += p.get('vertices', [])
    for v in data.get('vertices'):
        nodes += v.get('vertices', [])

    nodes = list({node['_id']: node for node in nodes}.values())
    edges = list({edge['_id']: edge for edge in edges}.values())

    data = {
        'nodes': nodes,
        'edges': edges
    }
    return data


def filter_graphs(data):
    graphs = []
    for graph in data:
        gra = {
            'name': graph['name'],
            'links': []
        }
        for edge_definition in graph['edge_definitions']:
            edge = {
                'edge': edge_definition['collection'],
                'from_collections': edge_definition['from'],
                'to_collections': edge_definition['to']
            }
            gra['links'].append(edge)
        graphs.append(gra)
    return graphs


def filter_collections(data, kind):
    collections = [coll['name'] for coll in data
                   if coll['system'] is False and
                   coll['name'] != 'internal_metadata' and
                   coll['type'] == kind]
    return collections


def make_key(document):
    key = '{}_{}'.format(
        document['provider'],
        document['id']
    )
    return key
