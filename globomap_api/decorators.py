import functools
import logging

from flask import jsonify

logger = logging.getLogger(__name__)


def json_response(f):
    """This decorator generates a JSON response from a Python dictionary"""

    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        rv = f(*args, **kwargs)
        status_or_headers = None
        headers = None
        if isinstance(rv, tuple):
            rv, status_or_headers, headers = rv + (None,) * (3 - len(rv))
        if isinstance(status_or_headers, (dict, list)):
            headers, status_or_headers = status_or_headers, None
        if not isinstance(rv, (dict, list)):
            if rv is not None:
                if status_or_headers != 200:
                    rv = {'errors': rv}
                    logger.error(rv)
                else:
                    rv = {'data': rv}

        rv = jsonify(rv)
        if status_or_headers is not None:
            rv.status_code = status_or_headers
        if headers is not None:
            rv.headers.extend(headers)
        logger.debug(rv)
        return rv
    return wrapped
