from flask import Flask

from buggy.settings import ProdConfig


def create_app(config_object=ProdConfig):
    """
    Application factory, just like here:
    http://flask.pocoo.org/docs/0.12/patterns/appfactories/
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    return app
