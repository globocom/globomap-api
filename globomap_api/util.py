import json

from jsonspec.reference import resolve
from jsonspec.validators import load


def json_validate(json_file):

    with open(json_file) as data_file:
        data = json.load(data_file)
        validator = load(data)

    return validator


def validate(error):
    msg = list()

    if error.flatten():
        for pointer, reasons in error.flatten().items():
            valor = resolve(
                error[1], pointer) if pointer != '#/' else ''
            msg.append({
                'error_pointer': pointer,
                'received_value': valor,
                'error_reasons': list(reasons)
            })
    else:
        msg.append({
            'error_pointer': error[0],
            'received_value': None,
            'error_reasons': list(error[1])
        })
    res = {
        'errors': msg
    }

    return res


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
