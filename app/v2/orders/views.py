"""/app/v1/orders/views.py"""
from functools import wraps
import jwt
from flask import request, jsonify, session
from . import orders_api
from app.models import Order


def token_required(f):
    """token validation"""
    @wraps(f)
    def decorated(**kwargs):
        """decorator"""
        try:
            session['token']
        except BaseException:
            session['token'] = None

        if session['token'] is None:
            return jsonify({'message': 'Please login'}), 401

        return f(**kwargs)
    return decorated


orderObject = Order()


def validate_data(data):
    """validate user details"""
    try:
        for index in data:
            if index is False:
                return index + " field required."
            i = True
        if i is True:
            return "valid"
    except Exception as error:
        return "please provide all the fields, missing " + str(error)


@orders_api.route('/users/orders', methods=["POST"])
@token_required
def order():
    """ Place an order for food."""
    data = request.get_json()

    res = validate_data(data)
    if res == "valid":
        food_id = data['food_id']
        client_id = data['client_id']
        client_adress = data['client_adress']
        status = "pending"
        response = orderObject.create_order(
            food_id,
            client_id,
            client_adress,
            status)
        return response
    return jsonify({"message": response}), 400


@orders_api.route('/orders/', methods=["GET"])
@token_required
def allorder():
    """ Get all orders"""
    data = orderObject.get_orders()
    return data


@orders_api.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def order_manipulation(order_id):
    """ GET/PUT/DEL order """
    if request.method == 'DELETE':
        # DELETE deletes a specific order
        res = orderObject.delete_order(order_id)
        return res

    elif request.method == 'PUT':
        # PUT Update the status  of an order
        data = request.get_json()
        data = request.get_json()
        food_id = data['food_id']
        client_id = data['client_id']
        client_adress = data['client_adress']
        status = data['status']
        res = orderObject.update_order(
            order_id,
            food_id,
            client_id,
            client_adress,
            status)
        return res
    # GET gets a specific order
    res = orderObject.get_order(order_id)
    return res


@orders_api.route('/users/orders/<int:client_id>', methods=['GET'])
@token_required
def userorders(client_id):
    """ Get the order history for a particular user."""
    res = orderObject.get_user_orders(client_id)
    return res
