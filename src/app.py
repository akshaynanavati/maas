import os

from flask import Blueprint
from flask import Flask

from controllers import base, health_check
from utils.api import API
import utils.misc as misc_utils


def create_app(**flask_options):
    # Construct the app
    app = Flask(__name__)
    app.config.update(flask_options)

    # Use some trickery to dynamically set up routing based on desired algorithm
    for maas in _get_maas_algorithms():
        bp, api = _create_blueprint(maas, '/{}'.format(maas.__name__))
        _route_unsorted(api)
        app.register_blueprint(bp)

        bp, api = _create_blueprint(maas, '/{}_status'.format(maas.__name__))
        _route_health_check(api)
        app.register_blueprint(bp)

    return app


def _get_maas_algorithms():
    for f in os.listdir('controllers/maas'):
        if f.endswith('.py') and not f.startswith('_'):
            yield misc_utils.import_from_dotted_path('controllers.maas.{}'.format(f[:-3]))


def _create_blueprint(maas, url_prefix):
    bp = Blueprint(url_prefix[1:], __name__, url_prefix=url_prefix)
    api = API(bp, maas.MaaS)
    return bp, api


def _route_unsorted(api):
    api.route('/', methods=['POST'])(base.insert)
    api.route('/median', methods=['GET'])(base.get_median)
    api.route('/', methods=['DELETE'])(base.reset)


def _route_health_check(api):
    api.route('/', methods=['GET'])(health_check.health_check)
