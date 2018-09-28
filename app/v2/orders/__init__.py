"""/app/v1/orders/__init__.py"""
from flask import Blueprint

orders_api = Blueprint('orders_api', __name__)

from . import views
