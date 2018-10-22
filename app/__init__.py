"""app Init"""
import os
from flask import Flask, request, jsonify

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

    from .v2.food import food_api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/v2')

    from .v2.orders import orders_api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/v2')

    from .v2.users import users_api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/v2')

    @app.errorhandler(404)
    def page_not_found_error(error):
        """handle error code 404"""
        return jsonify({'message': 'The page/endpoint you are requesting {!r} does not exist'\
        .format(request.path)}), error.code

    @app.errorhandler(405)
    def method_not_allowed_error(error):
        """handle error code 405"""
        return jsonify({'message': 'The url you are requesting is not correct'\
        .format(request.path)}), error.code

    @app.errorhandler(500)
    def unknown_error(error):
        """handle error code 500"""
        return jsonify({'message': 'Alert! Something somewhere went wrong'\
        .format(request.path)}), error.code



    return app
