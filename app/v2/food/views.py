"""/app/v1/food/views.py"""
from functools import wraps
import jwt
from flask import request, jsonify
from . import food_api
from app.v2.models import Food
from app.jwt_file import Auth, is_admin_loggedin

jwt_auth = Auth()

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

foodObject = Food()


def validate_data(data):
    """validate user details"""
    try:
        if data["food_name"] == "":
            return "Food name required"
        # check if food name has spaces
        elif " " in data["food_name"]:
            return "Food Name should be one word, no spaces"
        elif data["food_price"] == "":
            return "Food Price required"
        # check if food price has spaces
        elif " " in data["food_price"]:
            return "food price should be one word, no spaces"
        else:
            return "valid"
    except Exception as error:
        return "please provide all the fields, missing " + str(error)


@food_api.route('/menu', methods=["POST"])
@token_required
def create_food():
    """ Method to create and retrieve food."""
    if is_admin_loggedin() is True:
        data = request.get_json()
        res = validate_data(data)
        if res == "valid":
            food_name = data['food_name'].lower()
            food_price = data['food_price']
            food_image = data['food_image']
            response = foodObject.create_food(food_name, food_price, food_image)
            return response
        return jsonify({"message": res}), 400
    return jsonify({
        "message": "You dont have admin priviledges."}), 401


@food_api.route('/menu', methods=["GET"])
def get_all_food():
    """ Method to retrieve food."""
    data = foodObject.get_foods()
    return data


@food_api.route('/food/<int:food_id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def food_manipulation(food_id):
    """ GET/PUT/DEL food """
    if is_admin_loggedin() is True:
        if request.method == 'DELETE':
            # DELETE
            res = foodObject.delete_food(food_id)
            return res
        elif request.method == 'PUT':
            # PUT
            data = request.get_json()
            response = validate_data(data)
            if response == "valid":
                food_name = data['food_name']
                food_price = data['food_price']
                food_image = data['food_image']
                response = foodObject.update_food(
                    food_id,
                    food_name,
                    food_price,
                    food_image)

            return response
        else:
            #GET
            res = foodObject.get_food(food_id)
            return res
    return jsonify({
        "message": "You dont have admin priviledges."}), 401
