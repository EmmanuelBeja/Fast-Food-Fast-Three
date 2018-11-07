"""app/v1/users/__init__.py"""
from flask import Blueprint

users_api = Blueprint('users_api', __name__)

from . import views
