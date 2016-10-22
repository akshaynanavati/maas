from functools import wraps
import json

from flask import make_response, Response

from utils.exceptions import HTTPException


class API(object):
    """
    A wrapper on flask's routing mechanism that gives us some nice error handling
    and wraps dictionaries into JSON responses.
    """
    def __init__(self, bp, MaaS):
        self.bp = bp
        self.MaaS = MaaS

    def route(self, *args, **kwargs):
        def decorator(f):
            @wraps(f)
            def g(*args, **kwargs):
                try:
                    response = f(self.MaaS, *args, **kwargs)
                except HTTPException as e:
                    raise
                    return _process_response(e.to_json(), e.status_code)
                except Exception as e:
                    raise
                    return _process_response({'message': 'Server Error: {}'.format(e)}, 500)
                return _process_response(response)
            self.bp.route(*args, **kwargs)(g)
            return g
        return decorator


def _process_response(result, status_code=200):
    if isinstance(result, Response):
        return result
    else:
        data = json.dumps(result)
        return make_response(data, status_code, {'Content-Type': 'application/json'})
