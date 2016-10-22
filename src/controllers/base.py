from flask import request

from utils.exceptions import BadRequest, InsufficientStorage


def insert(MaaS):
    json = request.get_json()
    if json:
        to_insert = json['x']
    else:
        to_insert = [request.args.get('x')]
    if not to_insert or to_insert[0] is None:
        raise BadRequest('Must specify `x` as a url arg or in the json body.')
    try:
        to_insert = map(float, to_insert)
    except ValueError:
        raise BadRequest('`x` must be an int or a list of floats')
    n = min(len(to_insert), MaaS.remaining_space())
    if not n:
        raise InsufficientStorage('Buffer is full')
    return MaaS.insert(to_insert[:n])


def get_median(MaaS):
    return MaaS.get_median()


def reset(MaaS):
    return MaaS.reset()
