"""/app/v1/food/views.py"""
from flask import Flask, request, flash, redirect, url_for, jsonify, session
from . import food_api
from app.models import Food

"""instantiate class"""
foodObject = Food()


def validate_data(data):
    """validate user details"""
    try:
        # check if food_name is empty
        if data["food_name"] is False:
            return "food_name required"
            # check if food_price is empty
        elif data["food_price"] is False:
            return "food_price required"
            # check if food_image is empty
        elif data["food_image"] is False:
            return "food_image required"
        else:
            return "valid"
    except Exception as error:
        return "please provide all the fields, missing " + str(error)

@food_api.route('/menu', methods=["GET", "POST"])
def food():
    """ Method to create and retrieve food."""
    if request.method == "POST":
        data = request.get_json()
        res = validate_data(data)
        if res == "valid":
            food_name = data['food_name']
            food_price = data['food_price']
            food_image = data['food_image']
            res = foodObject.create_food(food_name, food_price, food_image)
            return res
        return jsonify({"message": res}), 400
    data = foodObject.get_foods()
    return data


@food_api.route('/food/<int:food_id>', methods=['GET', 'PUT', 'DELETE'])
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
