"""app/v1/users/views.py"""
from functools import wraps
import jwt
from flask import request, jsonify
from . import users_api
from app.v2.models import User
from app.jwt_file import Auth, is_admin_loggedin, get_logged_in_user_id

jwt_auth = Auth()
userObject = User()

def token_required(f):
    """check"""
    @wraps(f)
    def decorated(**kwargs):
        """decorator"""
        header = request.headers.get('Authorization')

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
        # check if password has spaces
        if " " in data["password"]:
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
        response = userObject.create_user(
            username,
            userphone,
            password)
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
    return jsonify({"message": res}), 403


@users_api.route('/users', methods=["GET"])
@token_required
def users():
    """get all users"""
    if is_admin_loggedin() is True:
        data = userObject.get_users()
        return data
    return jsonify({
        "message": "You dont have admin priviledges."}), 401


@users_api.route('/users', methods=["PUT"])
@token_required
def edit_profile():
    """edit user profile"""
    data = request.get_json()
    res = validate_data_signup(data)
    if res == "valid":
        userid = get_logged_in_user_id()
        username = data['username']
        userphone = data['userphone']
        password = data['password']
        response = userObject.update_user(
            userid,
            username,
            userphone,
            password)
        return response
    return jsonify({"message": res}), 400


@users_api.route('/users/<int:id>', methods=["GET", "DELETE"])
@token_required
def users_verbs(id):
    """run http verbs"""
    if is_admin_loggedin() is True:
        if request.method == "GET":
            data = userObject.get_specific_user(id)
            return data
        elif request.method == "DELETE":
            response = userObject.delete_user(id)
            return response
    return jsonify({
        "message": "You dont have admin priviledges."}), 401


@users_api.route('/auth/logout')
@token_required
def logout():
    """ Method to logout user."""
    header = request.headers.get('authorization')
    if header is None:
        return jsonify({"message": "No token provided"}), 400
    token = header.split(" ")[1]
    res = jwt_auth.blacklist(token)
    if res is True:
        return jsonify({"message": "Succefuly logout."}), 200
    return res
