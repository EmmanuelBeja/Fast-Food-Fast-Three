"""app/v1/users/views.py"""
from functools import wraps
import jwt
from flask import request, jsonify, session
from . import users_api
from app.models import User


def token_required(f):
    """check"""
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


userObject = User()


def validate_data_signup(data):
    """validate user details"""
    try:
        # check if the username is more than 3 characters
        if len(data['username'].strip()) < 3:
            return "username must be more than 3 characters"
        # check if password has spaces
        elif " " in data["password"]:
            return "password should be one word, no spaces"
        # check if password is empty
        elif data["password"] == "":
            return "password required"
        # check if username has spaces
        elif " " in data["username"]:
            return "username should be one word, no spaces"
        # check if username is empty
        elif data["username"] == "":
            return "username required"
        # check if userphone has spaces
        elif " " in data["userphone"]:
            return "userphone should be one word, no spaces"
        # check if userphone empty
        elif data["userphone"] == "":
            return "userphone required"
        # check if userRole has spaces
        elif " " in data["userRole"]:
            return "userRole should be one word, no spaces"
        # check if userRole is empty
        elif data["userRole"] == "":
            return "userRole required"
        elif len(data['password'].strip()) < 5:
            return "Password should have atleast 5 characters"
        # check if the passwords match
        elif data['password'] != data['confirmpass']:
            return "passwords do not match"
        else:
            return "valid"
    except Exception as error:
        return "please provide all the fields, missing " + str(error)


def validate_data_login(data):
    """validate user details"""
    try:
        # check if the username is more than 3 characters
        if len(data['username'].strip()) < 3:
            return "username must be more than 3 characters"
        # check if password has spaces
        elif " " in data["password"]:
            return "password should be one word, no spaces"
        # check if password is empty
        elif data["password"] == "":
            return "password required"
        # check if username has spaces
        elif " " in data["username"]:
            return "username should be one word, no spaces"
        # check if username is empty
        elif data["username"] == "":
            return "username required"
        else:
            return "valid"
    except Exception as error:
        return "please provide all the fields, missing " + str(error)


@users_api.route('/auth/signup', methods=["POST"])
def reg():
    """ Method to create user account."""
    data = request.get_json()
    res = validate_data_signup(data)

    if res == "valid":
        username = data['username']
        userphone = data['userphone']
        password = data['password']
        userRole = data['userRole']
        response = userObject.create_user(
            username,
            userphone,
            password,
            userRole)
        return response
    return jsonify({"message": res}), 400


@users_api.route('/auth/login', methods=["POST"])
def login():
    """ Method to login user """
    data = request.get_json()
    res = validate_data_login(data)
    if res == "valid":
        username = data['username']
        password = data['password']
        response = userObject.login(username, password)
        return response
    return jsonify({"message": res}), 401


@users_api.route('/users', methods=["GET"])
@token_required
def users():
    """get all users"""
    data = userObject.get_users()
    return data


@users_api.route('/users/<int:id>', methods=["GET", "DELETE", "PUT"])
@token_required
def users_verbs(id):
    """run http verbs"""
    if request.method == "GET":
        data = userObject.get_specific_user(id)
        return data
    elif request.method == "PUT":
        data = request.get_json()
        res = validate_data_signup(data)

        if res == "valid":
            username = data['username']
            userphone = data['userphone']
            password = data['password']
            userRole = data['userRole']
            response = userObject.update_user(
                id,
                username,
                userphone,
                password,
                userRole)
            return response
        return jsonify({"message": res}), 400
    elif request.method == "DELETE":
        response = userObject.delete_user(id)
        return response


@users_api.route('/auth/logout')
def logout():
    """ Method to logout user."""
    if 'token' in session:
        session.clear()
        return jsonify({"message": "Succeffully logout."})
    return jsonify({
        "message": "Not logged in."}), 200
