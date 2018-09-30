"""/app/v1/food/views.py"""
from flask import Flask, request, flash, redirect, url_for, jsonify, session
from . import food_api
from app.models import Food
import jwt, datetime
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*arg, **kwargs):
        token = session['token']

        try:
            data = jwt.decode(token, 'SECRET', algorithms=['HS256'])
        except:
            return jsonify({'message': 'Please login'}), 401

        return f(**kwargs)
    return decorated

"""instantiate class"""
foodObject = Food()

def validate_data(data):
    """validate user details"""
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
        res = foodObject.create_food(food_name, food_price, food_image)
        return res
    return jsonify({"message": res}), 400

@food_api.route('/menu', methods=["GET"])
def get_all_food():
    """ Method to retrieve food."""
    data = foodObject.get_foods()
    return data

@food_api.route('/food/<int:food_id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def food_manipulation(food_id, **kwargs):
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

    else:
        # GET
        res = foodObject.get_food(food_id)
        return res
