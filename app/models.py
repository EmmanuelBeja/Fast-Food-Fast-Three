"""app/v1/users/models.py"""
import re
from datetime import datetime, timedelta
import jwt
from flask import jsonify, session, request, make_response
from .database.conn import dbcon
from app.jwt import Auth

jwt_object = Auth()


class User(object):
    """User Class"""

    def __init__(self):
        """ Initialize empty user list"""
        self.conn = dbcon()
        self.cur = self.conn.cursor()
        self.users = {}
        self.userlist = {}
        self.result = []

    def create_user(self, username, userphone, password):
        """Create users"""
        userRole = "client"
        if not self.valid_username(username):
            if not self.valid_phone(userphone):
                self.cur.execute(
                    "INSERT INTO tbl_users(username, userphone, password, userrole)\
                VALUES(%(username)s, %(userphone)s, %(password)s, %(userrole)s);",\
                {'username': username, 'userphone': userphone, 'password': password, 'userrole': userRole})
                self.conn.commit()
                return jsonify({"message": "Signup Successful"}), 201
            return jsonify({"message": "Userphone is taken."}), 400
        return jsonify({"message": "Username is taken."}), 400

    def login(self, username, password):
        """login users"""
        if not self.valid_username(username):
            return jsonify({"message": "Please register first."}), 401
        self.cur.execute("SELECT * FROM tbl_users WHERE username=%(username)s\
        AND password=%(password)s", {'username': username, 'password': password})
        if self.cur.rowcount > 0:
            rows = self.cur.fetchall()
            for user in rows:
                userid = user[0]
                username = user[1]
                userrole = user[4]
                token = jwt.encode({'userid': userid,
                                        'username': username, 'userrole': userrole,
                                        'exp': datetime.utcnow() + timedelta(minutes=30)},
                                        'SECRET_KEY', algorithm='HS256')
                #save token in tbl_auth_tokens
                self.cur.execute("INSERT INTO tbl_auth_tokens(token)\
                VALUES(%(token)s);", {'token': token})
                self.conn.commit()
                mssg = {"message": "You are successfully logged in",
                "token": token.decode()}
                return jsonify(mssg), 200
        return jsonify({
            "message": "Wrong username or password"}), 403

    def get_specific_user(self, id):
        """get specific user """
        self.cur.execute(
            "SELECT * FROM tbl_users WHERE userid=%(userid)s", {'userid': id})
        if self.cur.rowcount > 0:
            rows = self.cur.fetchall()
            for user in rows:
                self.userlist.update({
                    'user_id': user[0],
                    'username': user[1],
                    'userRole': user[4],
                    'userPhone': user[2]})
                return jsonify({
                    "message": "Successful. User Found.",
                    "user": self.userlist}), 200
        return jsonify({"message": "user does not exist"}), 400

    def get_users(self):
        """get all user """
        self.cur.execute("SELECT * FROM tbl_users")
        if self.cur.rowcount > 0:
            rows = self.cur.fetchall()
            for user in rows:
                self.userlist.update({
                    'user_id': user[0],
                    'username': user[1],
                    'userRole': user[4],
                    'userPhone': user[2]})
                self.result.append(dict(self.userlist))
            return jsonify({
                "message": "Successful. Users Found",
                "Users": self.result}), 200
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
        self.cur.execute(
            "SELECT * FROM tbl_users WHERE userid=%(userid)s", {'userid': id})
        if self.cur.rowcount > 0:
            self.cur.execute(
                "UPDATE tbl_users SET username=%s, userphone=%s, password=%s\
            WHERE userid=%s", (username, userphone, password, id))
            self.conn.commit()
            return jsonify({"message": "Update Successful"}), 200
        return jsonify({"message": "No user."}), 400

    def delete_user(self, id):
        """ delete User """
        self.cur.execute(
            "SELECT * FROM tbl_users WHERE userid=%(userid)s", {'userid': id})
        if self.cur.rowcount > 0:
            # delete this user details
            self.cur.execute(
                "DELETE FROM tbl_users WHERE userid=%(userid)s", {
                    'userid': id})
            self.conn.commit()
            return jsonify({"message": "Delete Successful."}), 201
        return jsonify({"message": "No user."}), 400

    def valid_username(self, username):
        """check if username exist"""
        self.cur.execute("SELECT * FROM tbl_users WHERE username=%(username)s",
                         {'username': username})
        if self.cur.rowcount > 0:
            return True
        return False

    def valid_phone(self, userphone):
        """check if userphone exist"""
        self.cur.execute("SELECT * FROM tbl_users WHERE userphone=%(userphone)s",
                         {'userphone': userphone})
        if self.cur.rowcount > 0:
            return True
        return False

    def valid_password(self, password):
        """check password length and special characters"""
        if len(password) < 3 or not re.match("^[a-zA-Z0-9_ ]*$", password):
            return False
        return True


class Order(object):
    """order class"""

    def __init__(self):
        """ Initialize empty Order list"""
        self.conn = dbcon()
        self.cur = self.conn.cursor()
        self.orderlist = {}
        self.result = []

    def create_order(self, food_id, client_id, client_adress):
        """Create order_item"""
        status = 'pending'
        self.cur.execute("INSERT INTO  tbl_orders(food_id, client_id, client_adress, status)\
        VALUES(%(food_id)s, %(client_id)s, %(client_adress)s, %(status)s);",
                         {'food_id': food_id, 'client_id': client_id,\
                         'client_adress': client_adress,\
                          'status': status})
        self.conn.commit()
        return jsonify({"message": "Successful. Order created."}), 201

    def get_orders(self):
        """ get all Orders """
        self.cur.execute("SELECT * FROM tbl_orders")
        if self.cur.rowcount > 0:
            rows = self.cur.fetchall()
            for order in rows:
                self.orderlist.update({
                    'order_id': order[0],
                    'food_id': order[1],
                    'client_id': order[2],
                    'client_adress': order[3]})
                self.result.append(dict(self.orderlist))
            return jsonify({
                "message": "Successful. Orders Found.",
                "Orders": self.result}), 200
        return jsonify({
            "message": "No Order."}), 400

    def get_order(self, order_id):
        """ get Order """
        self.cur.execute("SELECT * FROM tbl_orders WHERE order_id=%(order_id)s",
                         {'order_id': order_id})
        if self.cur.rowcount > 0:
            rows = self.cur.fetchall()
            for order in rows:
                self.orderlist.update({
                    'order_id': order[0],
                    'food_id': order[1],
                    'client_id': order[2],
                    'client_adress': order[3]})
                self.result.append(dict(self.orderlist))
            return jsonify({
                "message": "Successful. Order found.",
                "Orders": self.result}), 200
        return jsonify({
            "message": "No Order."}), 400

    def get_user_orders(self, client_id):
        self.cur.execute("SELECT * FROM tbl_orders WHERE client_id=%(client_id)s",
                         {'client_id': client_id})
        if self.cur.rowcount > 0:
            rows = self.cur.fetchall()
            for order in rows:
                self.orderlist.update({
                    'order_id': order[0],
                    'food_id': order[1],
                    'client_id': order[2],
                    'client_adress': order[3]})
                self.result.append(dict(self.orderlist))
            return jsonify({
                "message": "Successful. User orders found.",
                "Orders": self.result}), 200
        return jsonify({
            "message": "No Order."}), 400

    def update_order(
            self,
            order_id,
            food_id,
            client_id,
            client_adress,
            status):
        """ update Order """
        self.cur.execute("SELECT * FROM tbl_orders WHERE order_id=%(order_id)s",
                         {'order_id': order_id})
        rows = self.cur.fetchall()
        if self.cur.rowcount > 0:
            # update this order details
            self.cur.execute(
                "UPDATE tbl_orders SET food_id=%s, client_id=%s,\
            client_adress=%s, status=%s WHERE order_id=%s",
                (food_id,
                 client_id,
                 client_adress,
                 status,
                 order_id))
            self.conn.commit()

            for order in rows:
                self.orderlist.update({
                    'order_id': order[0],
                    'food_id': order[1],
                    'client_id': order[2],
                    'client_adress': order[3]})
                return jsonify({
                    "message": "Update Successful.",
                    "Order": self.orderlist}), 201
        return jsonify({"message": "No Order."}), 400

    def delete_order(self, order_id):
        """ delete Order """
        self.cur.execute("SELECT * FROM tbl_orders WHERE order_id=%(order_id)s",
                         {'order_id': order_id})
        if self.cur.rowcount > 0:
            # delete this order details
            self.cur.execute(
                "DELETE FROM tbl_orders WHERE order_id=%(order_id)s", {
                    'order_id': order_id})
            self.conn.commit()
            return jsonify({"message": "Delete Successful."}), 201
        return jsonify({"message": "No Order."}), 400


class Food(object):
    def __init__(self):
        """ Initialize empty Order list"""
        self.conn = dbcon()
        self.cur = self.conn.cursor()
        self.foodlist = {}
        self.result = []

    def create_food(self, food_name, food_price, food_image):
        """Create food_item"""
        self.cur.execute(
            "INSERT INTO  tbl_foods(food_name, food_price, food_image)\
        VALUES(%(food_name)s, %(food_price)s, %(food_image)s);", {
            'food_name': food_name, 'food_price': food_price,\
                'food_image': food_image})
        self.conn.commit()
        return jsonify({"message": "Successful. Food Created"}), 201

    def get_foods(self):
        """ get all Foods """
        self.cur.execute("SELECT * FROM tbl_foods")
        if self.cur.rowcount > 0:
            rows = self.cur.fetchall()
            for food in rows:
                self.foodlist.update({
                    'food_id': food[0],
                    'food_name': food[1],
                    'food_price': food[2],
                    'food_image': food[3]})
                self.result.append(dict(self.foodlist))
            return jsonify({
                "message": "Successful. Food Found",
                "Foods": self.result}), 200
        return jsonify({
            "message": "No Food."}), 400

    def update_food(self, food_id, food_name, food_price, food_image):
        """ update Food """
        self.cur.execute("SELECT * FROM tbl_foods WHERE food_id=%(food_id)s",
                         {'food_id': food_id})
        if self.cur.rowcount > 0:
            # update this order details
            self.cur.execute(
                "UPDATE tbl_foods SET food_name=%s, food_price=%s, food_image=%s\
            WHERE food_id=%s", (food_name, food_price, food_image, food_id))
            self.conn.commit()
            return jsonify({"message": "Update Successful"}), 201
        return jsonify({"message": "No Food."}), 400

    def get_food(self, food_id):
        """ get specific Food """
        self.cur.execute(
            "SELECT * FROM tbl_foods WHERE food_id=%(food_id)s", {'food_id': food_id})
        if self.cur.rowcount > 0:
            rows = self.cur.fetchall()
            for food in rows:
                self.foodlist.update({
                    'food_id': food[0],
                    'food_name': food[1],
                    'food_price': food[2],
                    'food_image': food[3]})
            return jsonify({
                "message": "Successful. Food Found",
                "Foods": self.foodlist}), 200
        return jsonify({
            "message": "No Food."}), 400

    def delete_food(self, food_id):
        """ delete Food """
        self.cur.execute("SELECT * FROM tbl_foods WHERE food_id=%(food_id)s",
                         {'food_id': food_id})
        if self.cur.rowcount > 0:
            # delete this food details
            self.cur.execute(
                "DELETE FROM tbl_foods WHERE food_id=%(food_id)s", {
                    'food_id': food_id})
            self.conn.commit()
            return jsonify({
                "message": "Delete Successful."}), 201
        return jsonify({"message": "No Food."}), 400
