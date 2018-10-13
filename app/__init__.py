"""app Init"""
import os
from flask import Flask, render_template
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
        return render_template('index.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/signup')
    def signup():
        return render_template('signup.html')

    @app.route('/menu')
    def user_home():
        return render_template('user-home.html')

    @app.route('/history')
    def user_history():
        return render_template('user-history.html')

    @app.route('/order')
    def user_order():
        return render_template('user-order.html')

    @app.route('/profile')
    def user_profile():
        return render_template('user-profile.html')

    @app.route('/admin-profile')
    def admin_profile():
        return render_template('admin-profile.html')

    @app.route('/admin-home')
    def admin_home():
        return render_template('admin-home.html')

    @app.route('/admin-food')
    def admin_food():
        return render_template('admin-food.html')

    @app.route('/admin-edit-food')
    def admin_edit_food():
        return render_template('admin-edit-food.html')

    return app
