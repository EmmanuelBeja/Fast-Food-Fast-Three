"""/app/v1/food/views.py"""
from functools import wraps
import jwt
from flask import request, jsonify, session
from . import food_api
from app.models import Food


def token_required(f):
    """token required"""
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


foodObject = Food()


def validate_data(data):
    """validate user details"""
    index = False
    try:
        for index in data:
            if index is False:
                return index + " field required."
            index = True
        if index is True:
            return "valid"
    except Exception as error:
        return "please provide all the fields, missing " + str(error)


@food_api.route('/menu', methods=["POST"])
@token_required
def create_food():
    """ Method to create and retrieve food."""
    data = request.get_json()
    res = validate_data(data)
    if res == "valid":
        food_name = data['food_name']
        food_price = data['food_price']
        food_image = data['food_image']
        response = foodObject.create_food(food_name, food_price, food_image)
        return response
    return jsonify({"message": res}), 400


@food_api.route('/menu', methods=["GET"])
def get_all_food():
    """ Method to retrieve food."""
    data = foodObject.get_foods()
    return data


@food_api.route('/food/<int:food_id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def food_manipulation(food_id):
    """ GET/PUT/DEL food """
    if request.method == 'DELETE':
        # DELETE
        res = foodObject.delete_food(food_id)
        return res

    elif request.method == 'PUT':
        # PUT
        data = request.get_json()
        food_name = data['food_name']
        food_price = data['food_price']
        food_image = data['food_image']
        res = foodObject.update_food(
            food_id,
            food_name,
            food_price,
            food_image)
        return res
    res = foodObject.get_food(food_id)
    return res
