"""/app/v1/food/__init__.py"""
from flask import Blueprint

food_api = Blueprint('food_api', __name__)

from . import views
