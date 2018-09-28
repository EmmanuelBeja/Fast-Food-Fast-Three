"""/app/v1/orders/views.py"""
from flask import Flask, request, flash, redirect, url_for, jsonify, session
from . import orders_api
from app.models import Order

"""instantiate class"""
orderObject = Order()


def validate_data(data):
    """validate user details"""
    try:
        # check if food_id is empty
        if data["food_id"] is False:
            return "food_id required"
            # check if client_id is empty
        elif data["client_id"] is False:
            return "client_id required"
            # check if client_adress is empty
        elif data["client_adress"] is False:
            return "client_adress required"
        else:
            return "valid"
    except Exception as error:
        return "please provide all the fields, missing " + str(error)

@orders_api.route('/users/orders', methods=["POST"])
def order():
    """ Place an order for food."""
    data = request.get_json()

    res = validate_data(data)
    if res == "valid":
        food_id = data['food_id']
        client_id = data['client_id']
        client_adress = data['client_adress']
        status = "pending"
        res = orderObject.create_order(
            food_id,
            client_id,
            client_adress,
            status)
        return res
    return jsonify({"message": res}), 400

@orders_api.route('/orders/', methods=["GET"])
def allorder():
    """ Get all orders"""
    data = orderObject.get_orders()
    return data

@orders_api.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def order_manipulation(order_id, **kwargs):
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
    else:
        # GET gets a specific order
        res = orderObject.get_order(order_id)
        return res


@orders_api.route('/users/orders/<int:client_id>', methods=['GET'])
def userorders(client_id, **kwargs):
    """ Get the order history for a particular user."""
    res = orderObject.get_user_orders(client_id)
    return res
