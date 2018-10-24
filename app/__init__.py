"""app Init"""
import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# local imports
from instance.config import app_config
from .database.conn import init_db

def create_app(config_name):
    """ create app """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    #Initialize database
    init_db()

    from .v2.food import food_api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/v2')

    from .v2.orders import orders_api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/v2')

    from .v2.users import users_api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/v2')

    @app.route('/')
    def index():
        """index page"""
        return render_template('index.html')

    @app.route('/login')
    def login():
        """login"""
        return render_template('login.html')

    @app.route('/signup')
    def signup():
        """signup"""
        return render_template('signup.html')

    @app.route('/menu')
    def user_home():
        """user home"""
        return render_template('user-home.html')

    @app.route('/history')
    def user_history():
        """user history"""
        return render_template('user-history.html')

    @app.route('/order')
    def user_order():
        """user order"""
        return render_template('user-order.html')

    @app.route('/profile')
    def user_profile():
        """user profile"""
        return render_template('user-profile.html')

    @app.route('/a-profile')
    def admin_profile():
        """admin profile"""
        return render_template('admin-profile.html')

    @app.route('/a-home')
    def admin_home():
        """admin home"""
        return render_template('admin-home.html')

    @app.route('/a-food')
    def admin_food():
        """admin food"""
        return render_template('admin-food.html')

    @app.route('/a-edit-food')
    def admin_edit_food():
        """"admin edit food"""
        return render_template('admin-edit-food.html')

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
