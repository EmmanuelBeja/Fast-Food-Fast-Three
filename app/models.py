"""app/v1/users/models.py"""
from flask import jsonify, session
import re


class User(object):
    def __init__(self):
        """ Initialize empty user list"""
        self.user_list = []
        self.notfound = None

    def create_user(self, username, userphone, password, userRole):
        """Create users"""
        self.users = {}
        if not self.valid_username(username):

            self.id = len(self.user_list)
            self.users['username'] = username
            self.users['userphone'] = userphone
            self.users['password'] = password
            self.users['userRole'] = userRole
            self.users['userid'] = self.id + 1
            self.user_list.append(self.users)

            #remove password from response
            userlistclone = {}
            for user in self.user_list:
                if user['userid'] == self.users['userid']:
                    #remove password from response
                    userlistclone.update({
                        'user_id': user['userid'],
                        'username': user['username'],
                        'userRole': user['userRole'],
                        'userPhone': user['userphone']})
            return jsonify({"message": "Successful", "user": userlistclone}), 201
        return jsonify({"message": "Username is taken."}), 400

    def login(self, username, password):
        """login users"""
        if len(self.user_list) == 0:
            return jsonify({"message": "Please register first."}), 400
        else:
            userlistclone = {}
            for user in self.user_list:
                if username == user['username']:
                    if password == user['password']:
                        session['userid'] = user['userid']
                        session['username'] = user['username']
                        session['userrole'] = user['userRole']
                        #remove password from response
                        userlistclone.update({
                            'user_id': user['userid'],
                            'username': user['username'],
                            'userRole': user['userRole'],
                            'userPhone': user['userphone']})
                        return jsonify({
                            "message": "You are successfully logged in",
                            "user": userlistclone}), 200
                    else:
                        return jsonify({
                            "message": "Wrong username or password"}), 401
                else:
                    self.notfound = True
            if self.notfound is True:
                return jsonify({"message": "user does not exist"}), 400

    def get_specific_user(self, id):
        """get specific user """
        userlistclone = {}
        if len(self.user_list) > 0:
            for user in self.user_list:
                if user['userid'] == id:
                    #remove password from response
                    userlistclone.update({
                        'user_id': user['userid'],
                        'username': user['username'],
                        'userRole': user['userRole'],
                        'userPhone': user['userphone']})
                    return jsonify({
                    "message": "Successful",
                    "User": userlistclone}), 200
                self.notfound = True
            if self.notfound is True:
                return jsonify({"message": "user does not exist"}), 400
        return jsonify({"message": "user does not exist"}), 400


    def get_users(self):
        """get all user """
        userlistclone = {}
        result = []
        if len(self.user_list) > 0:
            for user in self.user_list:
                #remove password from response
                userlistclone.update({
                    'user_id': user['userid'],
                    'username': user['username'],
                    'userRole': user['userRole'],
                    'userPhone': user['userphone']})
                result.append(dict(userlistclone))
            return jsonify({
                "message": "Successful.",
                "Users": result}), 200
        return jsonify({
            "message": "No user."}), 400


    def update_user(
            self,
            id,
            username,
            userphone,
            password,
            userRole):
        """ update User """

        userlistclone = {}
        if len(self.user_list) > 0:
            for user in self.user_list:
                if user['userid'] == id:
                    user['username'] = username
                    user['userphone'] = userphone
                    user['password'] = password
                    user['userRole'] = userRole
                    #remove password from result
                    userlistclone.update({
                        'user_id': user['userid'],
                        'username': user['username'],
                        'userRole': user['userRole'],
                        'userPhone': user['userphone']})
                    return jsonify({
                        "message": "Update Successful.",
                        "Users": userlistclone}), 201
                self.notfound = True
            if self.notfound is True:
                return jsonify({
                    "message": "User doesn't exist."}), 400
        return jsonify({
            "message": "No user."}), 400

    def delete_user(self, id):
        """ delete User """
        if len(self.user_list) > 0:
            for user in self.user_list:
                if user['userid'] == id:
                    self.user_list.remove(user)
                    return jsonify({
                        "message": "Delete Successful."}), 201
                self.notfound = True
        return jsonify({
                "message": "user doesn't exist."}), 400

    def valid_username(self, username):
        """check if username exist"""
        if len(self.user_list) > 0:
            for user in self.user_list:
                if user['username'] == username:
                    return True
                self.notfound = True
            if self.notfound is True:
                    return False
        return False

    def valid_password(self, password):
        """check password length and special characters"""
        if len(password) < 3 or not re.match("^[a-zA-Z0-9_ ]*$", password):
            return False
        else:
            return True


class Order(object):
    def __init__(self):
        """ Initialize empty Order list"""
        self.order_list = []
        self.notfound = None

    def create_order(self, food_id, client_id, client_adress, status):
        """Create order_item"""
        self.orders = {}
        if self.is_loggedin() is True:
            self.orderId = len(self.order_list)
            self.orders['food_id'] = food_id
            self.orders['client_id'] = client_id
            self.orders['client_adress'] = client_adress
            self.orders['status'] = status
            self.orders['order_id'] = self.orderId + 1
            self.order_list.append(self.orders)
            return jsonify({
                "message": "Successful.",
                "Orders": self.order_list}), 201
        return jsonify({
            "message": "Please login first."}), 401

    def get_orders(self):
        """ get all Orders """
        if self.is_loggedin() is True:
            if self.is_admin() is True:
                if len(self.order_list) > 0:
                    return jsonify({
                    "message": "Successful.",
                    "Order": self.order_list}), 200
                return jsonify({
                    "message": "No order."}), 400
            return jsonify({
                "message": "You dont have admin priviledges."}), 401
        return jsonify({
            "message": "Please login first."}), 401

    def delete_order(self, order_id):
        """ delete Order """
        if self.is_loggedin() is True:
            if self.is_admin() is True:
                if len(self.order_list) > 0:
                    for order in self.order_list:
                        if order['order_id'] == order_id:
                            self.order_list.remove(order)
                            return jsonify({
                                "message": "Delete Successful.",
                                "Orders": self.order_list}), 201
                        self.notfound = True
                    if self.notfound is True:
                        return jsonify({
                            "message": "No order with that id."}), 400
                return jsonify({
                    "message": "No order."}), 400
            return jsonify({
                "message": "You dont have admin priviledges."}), 401
        return jsonify({
            "message": "Please login first."}), 401

    def update_order(
            self,
            order_id,
            food_id,
            client_id,
            client_adress,
            status):
        """ update Order """
        if self.is_loggedin() is True:
            if self.is_admin() is True:
                if len(self.order_list) > 0:
                    for order in self.order_list:
                        if order['order_id'] == order_id:
                            order['food_id'] = food_id
                            order['client_id'] = client_id
                            order['client_adress'] = client_adress
                            order['status'] = status
                            return jsonify({
                                "message": "Update Successful.",
                                "Orders": self.order_list}), 201
                        self.notfound = True
                    if self.notfound is True:
                        return jsonify({
                            "message": "No order with that id."}), 400
                return jsonify({
                    "message": "No order."}), 400
            return jsonify({
                "message": "You dont have admin priviledges."}), 401
        return jsonify({
            "message": "Please login first."}), 401

    def get_order(self, order_id):
        """ get Order """
        if self.is_loggedin() is True:
            if self.is_admin() is True:
                if len(self.order_list) > 0:
                    for order in self.order_list:
                        if order['order_id'] == order_id:
                            return jsonify({
                                "message": "Successful.",
                                "Order": order}), 200
                        self.notfound = True

                    if self.notfound is True:
                        return jsonify({
                            "message": "No order with that id."}), 400
                return jsonify({
                    "message": "No order."}), 400
            return jsonify({
                "message": "You dont have admin priviledges."}), 401
        return jsonify({
            "message": "Please login first."}), 401


    def get_user_orders(self, client_id):
        result = []
        if self.is_loggedin() is True:
            if len(self.order_list) > 0:
                for order in self.order_list:
                    if order['client_id'] == client_id:
                        # add content in a list and display
                        result.append(order)
                    self.notfound = True
                return jsonify({"message": "Successful", "Order": result})
            return jsonify({
                "message": "No order."}), 400
        return jsonify({
            "message": "Please login first."}), 400

    def is_loggedin(self):
        if 'username' in session:
            if session['username']:
                return True
        return False

    def is_admin(self):
        if 'userrole' in session:
            if session['userrole'] == 'admin':
                return True
        return False


class Food(object):
    def __init__(self):
        """ Initialize empty Order list"""
        self.food_list = []
        self.notfound = None

    def create_food(self, food_name, food_price, food_image):
        """Create food_item"""
        self.foods = {}
        if self.is_loggedin() is True:
            if self.is_admin() is True:
                self.foodId = len(self.food_list)
                self.foods['food_name'] = food_name
                self.foods['food_price'] = food_price
                self.foods['food_image'] = food_image
                self.foods['food_id'] = self.foodId + 1
                self.food_list.append(self.foods)
                return jsonify({
                    "message": "Successful.",
                    "Food": self.food_list}), 201
            return jsonify({
                "message": "You dont have admin priviledges."}), 401
        return jsonify({
            "message": "Please login first."}), 401

    def get_foods(self):
        """ get all Foods """
        if len(self.food_list) > 0:
            return jsonify({
                "message": "Successful.",
                "Food": self.food_list}), 200
        return jsonify({
            "message": "No food."}), 400


    def delete_food(self, food_id):
        """ delete Food """
        if self.is_loggedin() is True:
            if self.is_admin() is True:
                if len(self.food_list) > 0:
                    for food in self.food_list:
                        if food['food_id'] == food_id:
                            self.food_list.remove(food)
                            return jsonify({
                                "message": "Delete Successful.",
                                "Food": self.food_list}), 201
                        self.notfound = True
                    if self.notfound is True:
                        return jsonify({
                            "message": "No food with that id.",
                            "Food": self.food_list}), 400
                return jsonify({
                    "message": "No food."}), 400
            return jsonify({
                "message": "You dont have admin priviledges."}), 401
        return jsonify({
            "message": "Please login first."}), 401

    def update_food(self, food_id, food_name, food_price, food_image):
        """ update Food """
        if self.is_loggedin() is True:
            if self.is_admin() is True:
                if len(self.food_list) > 0:
                    for food in self.food_list:
                        if food['food_id'] == food_id:
                            food['food_name'] = food_name
                            food['food_price'] = food_price
                            food['food_image'] = food_image
                            return jsonify({
                                "message": "Update Successful."}), 201
                        self.notfound = True
                    if self.notfound is True:
                        return jsonify({
                            "message": "No food with that id."}), 400
                return jsonify({
                    "message": "No food."}), 400
            return jsonify({
                "message": "You dont have admin priviledges."}), 401
        return jsonify({
            "message": "Please login first."}), 401

    def get_food(self, food_id):
        """ get Food """
        if len(self.food_list) > 0:
            for food in self.food_list:
                if food['food_id'] == food_id:
                    return jsonify({
                        "message": "Successful.",
                        "Food": food}), 200
                self.notfound = True
            if self.notfound is True:
                return jsonify({
                    "message": "No food with that id."}), 400
        return jsonify({
            "message": "No food."}), 400

    def is_loggedin(self):
        if 'username' in session:
            if session['username']:
                return True
        return False

    def is_admin(self):
        if 'userrole' in session:
            if session['userrole'] == 'admin':
                return True
        return False
