"""/app/v1/orders/views.py"""
from functools import wraps
import jwt
from flask import request, jsonify, session, render_template
from . import orders_api
from app.models import Order
from app.jwt import Auth
from app.database.conn import dbcon

jwt_auth = Auth()

conn = dbcon()
cur = conn.cursor()

def is_admin_loggedin():
    """ check if a user is an admin logged in"""
    header = request.headers.get('authorization')
    token = header.split(" ")[1]
    token = jwt.decode(token, 'SECRET_KEY', algorithms=['HS256'])
    user_id = token['userid']
    cur.execute("SELECT * FROM tbl_users WHERE userid=%(userid)s AND userRole=%(role)s",\
    {'userid': user_id, 'role': 'admin'})
    if cur.rowcount > 0:
        return True
    return False

def get_logged_in_user_id():
    header = request.headers.get('authorization')
    token = header.split(" ")[1]
    token = jwt.decode(token, 'SECRET_KEY', algorithms=['HS256'])
    user_id = token['userid']
    return user_id

def token_required(f):
    """check"""
    @wraps(f)
    def decorated(**kwargs):
        """decorator"""
        header = request.headers.get('authorization')

        if header is None:
            return jsonify({"message": "Authorization header missing"}), 403
        elif header.split(" ")[1] is None:
            return jsonify({"message": "Token missing"}), 403
        token = header.split(" ")[1]

        try:
            if jwt_auth.in_blacklist(token) is False:
                try:
                    data = jwt.decode(token, 'SECRET_KEY', algorithms=['HS256'])
                except jwt.ExpiredSignatureError:
                    # token expired blacklist token
                    jwt_auth.blacklist(token)
                    return jsonify({'message': 'Logged out. Please login and update token'}), 401
                except jwt.InvalidTokenError:
                    # token invalid blacklist token
                    jwt_auth.blacklist(token)
                    return jsonify({'message': 'Invalid Token. Please login'}), 401
            else:
                return jsonify({'message': 'Token blacklisted. Please login'}), 401
        except BaseException:
            return jsonify({'message': 'Please login'}), 401

        return f(**kwargs)
    return decorated


orderObject = Order()

def validate_create_data(data):
    """validate order details"""
    try:
        if " " in data["food_id"]:
            return "food_id should be one word, no spaces"
        # check if food_id is empty
        elif data["food_id"] == "":
            return "food_id required"
        # check if id is int
        elif data["food_id"].isalpha():
            return "Required to be an integer"
        # check if client_adress is empty
        elif data["client_adress"] == "":
            return "client_adress required"
        else:
            return "valid"
    except Exception as error:
        return "please provide all the fields, missing " + str(error)


def validate_update_data(data):
    """validate order details"""
    try:
        if " " in data["food_id"]:
            return "food_id should be one word, no spaces"
        # check if food_id is empty
        elif data["food_id"] == "":
            return "food_id required"
        # check if id is int
        elif data["food_id"].isalpha():
            return "Required to be an integer"
        # check if client_adress is empty
        elif data["client_adress"] == "":
            return "client_adress required"
        #check statuses
        elif data["status"].lower() != "pending" or data["status"].lower() != "accepted" or\
            data["status"].lower() != "declined" or data["status"].lower() != "completed":
            return "Wrong order status. Allowed statuses: accepted, declined, completed"
        else:
            return "valid"
    except Exception as error:
        return "please provide all the fields, missing " + str(error)

@orders_api.route('/users/orders', methods=["POST"])
@token_required
def order():
    """ Place an order for food."""
    data = request.get_json()
    #food_id = data['food_id']
    client_id = get_logged_in_user_id()
    client_adress = data['client_adress']
    response = orderObject.create_order(
        client_id,
        client_adress)
    return response


@orders_api.route('/users/pick_food/<int:food_id>', methods=["GET"])
def pick_food(food_id):
    """ Pick food in menu."""
    #add food to a session dict with food id and quantity
    response = orderObject.add_to_cart(food_id)
    return response


@orders_api.route('/users/cart_quantity', methods=["GET"])
def cart_quantity():
    """ Get cart quantity."""
    #return quantity session with food items picked
    response = orderObject.cart_quantity()
    return response


@orders_api.route('/users/cart', methods=["GET"])
def cart():
    """ Get all picked food."""
    #return quantity session with food items picked
    response = orderObject.cart_details()
    return response


@orders_api.route('/orders/', methods=["GET"])
@token_required
def all_order():
    """ Get all orders"""
    if is_admin_loggedin() is True:
        data = orderObject.get_orders()
        return data
    return jsonify({
        "message": "You dont have admin priviledges."}), 401


@orders_api.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def order_manipulation(order_id):
    """ GET/PUT/DEL order """
    if is_admin_loggedin() is True:
        if request.method == 'DELETE':
            # DELETE deletes a specific order
            res = orderObject.delete_order(order_id)
            return res
        elif request.method == 'PUT':
            # PUT Update the status  of an order
            data = request.get_json()
            food_id = data['food_id']
            client_id = get_logged_in_user_id()
            client_adress = data['client_adress']
            status = data['status'].lower()
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
    return jsonify({
        "message": "You dont have admin priviledges."}), 401


@orders_api.route('/users/orders/<int:client_id>', methods=['GET'])
@token_required
def user_orders(client_id):
    """ Get the order history for a particular user."""
    if is_admin_loggedin() is True:
        res = orderObject.get_user_orders(client_id)
        return res
    return jsonify({
        "message": "You dont have admin priviledges."}), 401


@orders_api.route('/users/orders', methods=['GET'])
@token_required
def logged_in_user_orders():
    """ Get logged in user order history."""
    client_id = get_logged_in_user_id()
    res = orderObject.get_user_orders(client_id)
    return res
