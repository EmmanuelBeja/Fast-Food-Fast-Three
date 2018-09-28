# third-party imports
import os
from flask import Flask

# local imports
from instance.config import app_config
from .database.conn import init_db

def create_app(config_name):
    """ create app """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    #Initialize database
    init_db()

    from .v1.food import food_api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/v2')

    from .v1.orders import orders_api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/v2')

    from .v1.users import users_api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/v3')

    return app
