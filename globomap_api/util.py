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
