"""app/v1/users/models.py"""
from flask import jsonify, session
import re
from .database.conn import dbcon


class User(object):
    """User Class"""
    def __init__(self):
        """ Initialize empty user list"""
        self.conn = dbcon()
        self.cur = self.conn.cursor()

    def create_user(self, username, userphone, password, userRole):
        """Create users"""
        self.users = {}
        if not self.valid_username(username):
            if not self.valid_phone(userphone):
                self.cur.execute("INSERT INTO  tbl_users(username, userphone, password, userrole) VALUES(%(username)s, %(userphone)s, %(password)s, %(userrole)s);",{
                'username': username, 'userphone': userphone, 'password': password, 'userrole': userRole})
                self.conn.commit()

                self.cur.execute("""SELECT * from tbl_users""")
                rows = self.cur.fetchall()
                #remove password from response
                userlistclone = {}
                for user in rows:
                    #remove password from response
                    userlistclone.update({
                        'user_id': user[0],
                        'username': user[1],
                        'userRole': user[4],
                        'userPhone': user[2]})
                    return jsonify({"message": "Successful", "user": userlistclone}), 201
            return jsonify({"message": "Userphone is taken."}), 400
        return jsonify({"message": "Username is taken."}), 400

    def login(self, username, password):
        """login users"""
        if not self.valid_username(username):
            return jsonify({"message": "Please register first."}), 401
        else:
            self.cur.execute("SELECT * FROM tbl_users WHERE username=%(username)s AND password=%(password)s", {'username': username, 'password': password})
            numrows = self.cur.rowcount
            if numrows > 0:
                rows = self.cur.fetchall()
                userlistclone = {}
                for user in rows:
                    session['userid'] = user[0]
                    session['username'] = user[1]
                    session['userrole'] = user[4]
                    #remove password from response
                    userlistclone.update({
                        'user_id': user[0],
                        'username': user[1],
                        'userRole': user[4],
                        'userPhone': user[2]})
                    return jsonify({
                        "message": "You are successfully logged in",
                        "user": userlistclone}), 200
            return jsonify({
                "message": "Wrong username or password"}), 403


    def get_specific_user(self, id):
        """get specific user """
        self.cur.execute("SELECT * FROM tbl_users WHERE userid=%(userid)s", {'userid': id})
        numrows = self.cur.rowcount
        if numrows > 0:
            rows = self.cur.fetchall()
            userlistclone = {}
            for user in rows:
                #remove password from response
                userlistclone.update({
                    'user_id': user[0],
                    'username': user[1],
                    'userRole': user[4],
                    'userPhone': user[2]})
                return jsonify({
                    "message": "Successful",
                    "user": userlistclone}), 200
        return jsonify({"message": "user does not exist"}), 400

    def get_users(self):
        """get all user """
        userlistclone = {}
        result = []
        self.cur.execute("SELECT * FROM tbl_users")
        numrows = self.cur.rowcount
        if numrows > 0:
            rows = self.cur.fetchall()
            for user in rows:
                #remove password from response
                userlistclone.update({
                    'user_id': user[0],
                    'username': user[1],
                    'userRole': user[4],
                    'userPhone': user[2]})
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
        self.cur.execute("SELECT * FROM tbl_users WHERE userid=%(userid)s", {'userid': id})
        numrows = self.cur.rowcount
        if numrows > 0:
            rows = self.cur.fetchall()
            #update this user details
            self.cur.execute("UPDATE tbl_users SET username=%s, userphone=%s, password=%s WHERE userid=%s", (username, userphone, password, id))
            self.conn.commit()
            userlistclone = {}
            for user in rows:
                #remove password from response
                userlistclone.update({
                    'user_id': user[0],
                    'username': user[1],
                    'userRole': user[4],
                    'userPhone': user[2]})
                return jsonify({
                    "message": "Successful",
                    "user": userlistclone}), 200
        return jsonify({"message": "No user."}), 400

    def delete_user(self, id):
        """ delete User """
        self.cur.execute("SELECT * FROM tbl_users WHERE userid=%(userid)s", {'userid': id})
        numrows = self.cur.rowcount
        if numrows > 0:
            #delete this user details
            self.cur.execute("DELETE FROM tbl_users WHERE userid=%(userid)s", {'userid': id})
            self.conn.commit()
            return jsonify({
                "message": "Delete Successful."}), 201
        return jsonify({"message": "No user."}), 400

    def valid_username(self, username):
        """check if username exist"""
        self.cur.execute("SELECT * FROM tbl_users WHERE username=%(username)s", {'username': username})
        numrows = self.cur.rowcount
        if numrows > 0:
            return True
        return False

    def valid_phone(self, userphone):
        """check if userphone exist"""
        self.cur.execute("SELECT * FROM tbl_users WHERE userphone=%(userphone)s", {'userphone': userphone})
        numrows = self.cur.rowcount
        if numrows > 0:
            return True
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
        self.conn = dbcon()
        self.cur = self.conn.cursor()

    def create_order(self, food_id, client_id, client_adress, status):
        """Create order_item"""
        orderlist = {}
        if self.is_loggedin() is True:
            self.cur.execute("INSERT INTO  tbl_orders(food_id, client_id, client_adress, status) VALUES(%(food_id)s, %(client_id)s, %(client_adress)s, %(status)s);",{
            'food_id': food_id, 'client_id': client_id, 'client_adress': client_adress, 'status': status})
            self.conn.commit()

            self.cur.execute("""SELECT * from tbl_orders""")
            rows = self.cur.fetchall()
            for order in rows:
                orderlist.update({
                    'order_id': order[0],
                    'food_id': order[1],
                    'client_id': order[2],
                    'client_adress': order[3]})
            return jsonify({"message": "Successful", "Order": orderlist}), 201
        return jsonify({
            "message": "Please login first."}), 401

    def get_orders(self):
        """ get all Orders """
        orderlist = {}
        result = []
        if self.is_loggedin() is True:
            if self.is_admin() is True:
                self.cur.execute("SELECT * FROM tbl_orders")
                numrows = self.cur.rowcount
                if numrows > 0:
                    rows = self.cur.fetchall()
                    for order in rows:
                        orderlist.update({
                            'order_id': order[0],
                            'food_id': order[1],
                            'client_id': order[2],
                            'client_adress': order[3]})
                        result.append(dict(orderlist))
                    return jsonify({
                        "message": "Successful.",
                        "Orders": result}), 200
                return jsonify({
                    "message": "No Order."}), 400
            return jsonify({
                "message": "You dont have admin priviledges."}), 401
        return jsonify({
            "message": "Please login first."}), 401

    def get_order(self, order_id):
        """ get Order """
        orderlist = {}
        result = []
        if self.is_loggedin() is True:
            if self.is_admin() is True:

                self.cur.execute("SELECT * FROM tbl_orders WHERE order_id=%(order_id)s", {'order_id': order_id})
                numrows = self.cur.rowcount
                if numrows > 0:
                    rows = self.cur.fetchall()
                    for order in rows:
                        orderlist.update({
                            'order_id': order[0],
                            'food_id': order[1],
                            'client_id': order[2],
                            'client_adress': order[3]})
                        result.append(dict(orderlist))
                    return jsonify({
                        "message": "Successful.",
                        "Orders": result}), 200
                return jsonify({
                    "message": "No Order."}), 400
            return jsonify({
                "message": "You dont have admin priviledges."}), 401
        return jsonify({
            "message": "Please login first."}), 401

    def get_user_orders(self, client_id):
        orderlist = {}
        result = []
        if self.is_loggedin() is True:
            if self.is_admin() is True:
                self.cur.execute("SELECT * FROM tbl_orders WHERE client_id=%(client_id)s", {'client_id': client_id})
                numrows = self.cur.rowcount
                if numrows > 0:
                    rows = self.cur.fetchall()
                    for order in rows:
                        orderlist.update({
                            'order_id': order[0],
                            'food_id': order[1],
                            'client_id': order[2],
                            'client_adress': order[3]})
                        result.append(dict(orderlist))
                    return jsonify({
                        "message": "Successful.",
                        "Orders": result}), 200
                return jsonify({
                    "message": "No Order."}), 400
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
                orderlist = {}
                self.cur.execute("SELECT * FROM tbl_orders WHERE order_id=%(order_id)s", {'order_id': order_id})
                numrows = self.cur.rowcount
                rows = self.cur.fetchall()
                if numrows > 0:
                    #update this order details
                    self.cur.execute("UPDATE tbl_orders SET food_id=%s, client_id=%s, client_adress=%s, status=%s WHERE order_id=%s", (food_id, client_id, client_adress, status, order_id))
                    self.conn.commit()

                    for order in rows:
                        orderlist.update({
                            'order_id': order[0],
                            'food_id': order[1],
                            'client_id': order[2],
                            'client_adress': order[3]})
                        return jsonify({
                            "message": "Successful",
                            "Order": orderlist}), 201
                return jsonify({"message": "No Order."}), 400
            return jsonify({
                "message": "You dont have admin priviledges."}), 401
        return jsonify({
            "message": "Please login first."}), 401

    def delete_order(self, order_id):
        """ delete Order """
        if self.is_loggedin() is True:
            if self.is_admin() is True:

                self.cur.execute("SELECT * FROM tbl_orders WHERE order_id=%(order_id)s", {'order_id': order_id})
                numrows = self.cur.rowcount
                if numrows > 0:
                    #delete this order details
                    self.cur.execute("DELETE FROM tbl_orders WHERE order_id=%(order_id)s", {'order_id': order_id})
                    self.conn.commit()
                    return jsonify({
                        "message": "Delete Successful."}), 201
                return jsonify({"message": "No Order."}), 400
            return jsonify({
                "message": "You dont have admin priviledges."}), 401
        return jsonify({
            "message": "Please login first."}), 401

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
        self.conn = dbcon()
        self.cur = self.conn.cursor()

    def create_food(self, food_name, food_price, food_image):
        """Create food_item"""
        foodlist = {}
        if self.is_loggedin() is True:
            if self.is_admin() is True:
                self.cur.execute("INSERT INTO  tbl_foods(food_name, food_price, food_image) VALUES(%(food_name)s, %(food_price)s, %(food_image)s);",{
                'food_name': food_name, 'food_price': food_price, 'food_image': food_image})
                self.conn.commit()
                self.cur.execute("""SELECT * from tbl_foods""")
                rows = self.cur.fetchall()
                for food in rows:
                    foodlist.update({
                        'food_id': food[0],
                        'food_name': food[1],
                        'food_price': food[2],
                        'food_image': food[3]})
                return jsonify({"message": "Successful", "Food": foodlist}), 201
            return jsonify({
                "message": "You dont have admin priviledges."}), 401
        return jsonify({
            "message": "Please login first."}), 401

    def get_foods(self):
        """ get all Foods """
        foodlist = {}
        result = []
        self.cur.execute("SELECT * FROM tbl_foods")
        numrows = self.cur.rowcount
        if numrows > 0:
            rows = self.cur.fetchall()
            for food in rows:
                foodlist.update({
                    'food_id': food[0],
                    'food_name': food[1],
                    'food_price': food[2],
                    'food_image': food[3]})
                result.append(dict(foodlist))
            return jsonify({
                "message": "Successful.",
                "Foods": result}), 200
        return jsonify({
            "message": "No Food."}), 400

    def update_food(self, food_id, food_name, food_price, food_image):
        """ update Food """
        if self.is_loggedin() is True:
            if self.is_admin() is True:

                foodlist = {}
                self.cur.execute("SELECT * FROM tbl_foods WHERE food_id=%(food_id)s", {'food_id': food_id})
                numrows = self.cur.rowcount
                rows = self.cur.fetchall()
                if numrows > 0:
                    #update this order details
                    self.cur.execute("UPDATE tbl_foods SET food_name=%s, food_price=%s, food_image=%s WHERE food_id=%s", (food_name, food_price, food_image, food_id))
                    self.conn.commit()

                    for food in rows:
                        foodlist.update({
                            'food_id': food[0],
                            'food_name': food[1],
                            'food_price': food[2],
                            'food_image': food[3]})
                        return jsonify({
                            "message": "Successful",
                            "Food": foodlist}), 201
                return jsonify({"message": "No Food."}), 400

            return jsonify({
                "message": "You dont have admin priviledges."}), 401
        return jsonify({
            "message": "Please login first."}), 401

    def get_food(self, food_id):
        """ get Food """
        foodlist = {}
        self.cur.execute("SELECT * FROM tbl_foods WHERE food_id=%(food_id)s", {'food_id': food_id})
        numrows = self.cur.rowcount
        if numrows > 0:
            rows = self.cur.fetchall()
            for food in rows:
                foodlist.update({
                    'food_id': food[0],
                    'food_name': food[1],
                    'food_price': food[2],
                    'food_image': food[3]})
            return jsonify({
                "message": "Successful.",
                "Foods": foodlist}), 200
        return jsonify({
            "message": "No Food."}), 400

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
