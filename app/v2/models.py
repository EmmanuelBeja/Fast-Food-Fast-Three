"""app/v1/users/models.py"""
import re
from datetime import datetime, timedelta
from flask import jsonify
import jwt
from app.database.conn import dbcon
from app.jwt_file import Auth

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
                {'username': username, 'userphone': userphone, 'password': password,\
                'userrole': userRole})
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
            rows = self.cur.fetchone()
            userid = rows[0]
            username = rows[1]
            userrole = rows[4]
            token = jwt.encode({'userid': userid,
                                'username': username, 'userrole': userrole,
                                'exp': datetime.utcnow() + timedelta(minutes=30)},
                               'SECRET_KEY', algorithm='HS256')
            #save token in tbl_auth_tokens
            self.cur.execute("INSERT INTO tbl_auth_tokens(token)\
            VALUES(%(token)s);", {'token': token})
            self.conn.commit()
            mssg = {"message": "You are successfully logged in",
                    "token": token.decode(), 'userrole': userrole}
            return jsonify(mssg), 200
        return jsonify({
            "message": "Wrong username or password"}), 403

    def get_specific_user(self, id):
        """get specific user """
        self.cur.execute(
            "SELECT * FROM tbl_users WHERE userid=%(userid)s", {'userid': id})
        if self.cur.rowcount > 0:
            rows = self.cur.fetchone()
            self.userlist.update({
                'user_id': rows[0],
                'username': rows[1],
                'userRole': rows[4],
                'userPhone': rows[2]})
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
            userid,
            username,
            userphone,
            password):
        """ update User """
        self.cur.execute("SELECT * FROM tbl_users WHERE userid=%(userid)s",\
            {'userid': userid})
        if self.cur.rowcount > 0:
            self.cur.execute(
                "UPDATE tbl_users SET username=%s, userphone=%s, password=%s\
            WHERE userid=%s", (username, userphone, password, userid))
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
        self.pick_food_list = []

    def create_order(self, client_id, client_adress):
        """Create order_item"""
        status = 'pending'
        self.cur.execute(
            "SELECT * FROM tbl_order_cache WHERE client_id=%(client_id)s",\
            {'client_id': client_id})
        if self.cur.rowcount > 0:
            #loop through to get total price
            row_cache = self.cur.fetchall()
            for order in row_cache:
                food_id = order[1]
                quantity = order[5]
                #Check if user had ordered this food earlier
                self.cur.execute("SELECT * FROM tbl_orders WHERE food_id=%(food_id)s\
                and client_id=%(client_id)s and status=%(status)s",
                                 {'food_id': food_id, 'client_id': client_id, 'status': status})
                if self.cur.rowcount > 0:
                    rows = self.cur.fetchone()
                    order_id = rows[0]
                    quantity = int(rows[4]) + int(quantity)
                    self.cur.execute(
                        "UPDATE tbl_orders SET client_adress=%s, quantity=%s WHERE order_id=%s",
                        (client_adress, quantity, order_id))
                    self.conn.commit()
                else:
                    self.cur.execute("INSERT INTO  tbl_orders(food_id, client_id, client_adress,\
                    quantity, status)\
                    VALUES(%(food_id)s, %(client_id)s, %(client_adress)s, %(quantity)s,\
                    %(status)s);",
                                     {'food_id': food_id, 'client_id': client_id,\
                    'client_adress': client_adress, 'quantity': quantity, 'status': status})
                    self.conn.commit()

                #delete all orders in cache for this user
                self.cur.execute(
                    "DELETE FROM tbl_order_cache WHERE client_id=%(client_id)s", {
                        'client_id': client_id})
                self.conn.commit()

        return jsonify({"message": "Successful. Order created."}), 201


    def get_orders(self):
        """ get all Orders """
        self.cur.execute("SELECT * FROM tbl_orders")
        if self.cur.rowcount > 0:
            rows = self.cur.fetchall()
            self.orderlist = {}
            self.result = []
            for order in rows:
                food_id = order[1]
                userid = order[2]
                self.cur.execute("SELECT * FROM tbl_foods WHERE food_id=%(food_id)s",
                                 {'food_id': food_id})
                rowfood = self.cur.fetchone()

                self.cur.execute("SELECT * FROM tbl_users WHERE userid=%(userid)s",
                                 {'userid': userid})
                rowuser = self.cur.fetchone()

                self.orderlist.update({
                    'order_id': order[0],
                    'food_name': rowfood[1],
                    'food_price': rowfood[2],
                    'client_adress': order[3],
                    'client_name': rowuser[1],
                    'client_phone': rowuser[2],
                    'quantity': order[4],
                    'status': order[5],
                    'createddate': order[6]})
                self.result.append(dict(self.orderlist))
            return jsonify({
                "message": "Successful. Orders Found.",
                "Orders": self.result}), 200
        return jsonify({
            "message": "No Order."}), 200

    def get_order(self, order_id):
        """ get Order """
        self.cur.execute("SELECT * FROM tbl_orders WHERE order_id=%(order_id)s",
                         {'order_id': order_id})
        if self.cur.rowcount > 0:
            rows = self.cur.fetchone()
            self.orderlist.update({
                'order_id': rows[0],
                'food_id': rows[1],
                'client_id': rows[2],
                'client_adress': rows[3]})
            self.result.append(dict(self.orderlist))
            return jsonify({
                "message": "Successful. Order found.",
                "Orders": self.result}), 200
        return jsonify({
            "message": "No Order."}), 400

    def get_user_orders(self, client_id):
        """get orders for specific user"""
        self.cur.execute("SELECT * FROM tbl_orders WHERE client_id=%(client_id)s",
                         {'client_id': client_id})
        if self.cur.rowcount > 0:
            rows = self.cur.fetchall()
            self.result = []
            for order in rows:
                # get food details
                food_id = order[1]
                self.cur.execute("SELECT * FROM tbl_foods WHERE food_id=%(food_id)s",
                                 {'food_id': food_id})
                rowfood = self.cur.fetchone()

                self.orderlist.update({
                    'order_id': order[0],
                    'food_id': food_id,
                    'food_name': rowfood[1],
                    'food_price': rowfood[2],
                    'client_id': order[2],
                    'client_adress': order[3],
                    'quantity': order[4],
                    'status': order[5],
                    'createddate': order[6]
                    })
                self.result.append(dict(self.orderlist))
            return jsonify({
                "message": "Successful. User orders found.",
                "Orders": self.result}), 200

        return jsonify({
            "message": "No Order."}), 400


    def add_to_cart(self, food_id, client_id):
        """add food to cart"""
        #get food price
        self.cur.execute(
            "SELECT * FROM tbl_foods WHERE food_id=%(food_id)s", {'food_id': food_id})
        rows = self.cur.fetchone()
        price = rows[2]
        food_name = rows[1]

        #check if food ordered before
        self.cur.execute(
            "SELECT * FROM tbl_order_cache WHERE food_id=%(food_id)s and client_id=%(client_id)s",\
            {'food_id': food_id, 'client_id': client_id})
        if self.cur.rowcount > 0:
            #update order
            rows = self.cur.fetchone()
            quantity = int(rows[5]) + 1
            total = int(quantity)*int(price)
            self.cur.execute(
                "UPDATE tbl_order_cache SET quantity=%s, total=%s\
            WHERE food_id=%s AND client_id=%s",
                (quantity,
                 total,
                 food_id,
                 client_id))
            self.conn.commit()
        else:
            #insert new order
            quantity = 1
            self.cur.execute("INSERT INTO tbl_order_cache(food_id, food_name, client_id, price,\
            quantity, total)\
            VALUES(%(food_id)s, %(food_name)s, %(client_id)s, %(price)s, %(quantity)s, %(total)s);",
                             {'food_id': food_id, 'food_name': food_name, 'client_id': client_id,\
                             'price': price, 'quantity': quantity, 'total': price})
            self.conn.commit()

        return jsonify({"message": "Added to cart."}), 201

    def cart_cancel(self, client_id):
        """cancel order"""
        self.cur.execute(
            "DELETE FROM tbl_order_cache WHERE client_id=%(client_id)s", {
                'client_id': client_id})
        self.conn.commit()
        return jsonify({"message": "Order Canceled."}), 200

    def cart_quantity(self, client_id):
        """get quantity added to cart"""
        total = 0
        totalprice = 0
        self.cur.execute(
            "SELECT * FROM tbl_order_cache WHERE client_id=%(client_id)s", {'client_id': client_id})
        if self.cur.rowcount > 0:
            #loop through to get total and total price
            rows = self.cur.fetchall()
            for order in rows:
                total = int(total)+int(order[5])
                totalprice = int(totalprice)+int(order[6])

        return jsonify({'Cart': total, 'totalprice': totalprice}), 200


    def cart_details(self, client_id):
        """get cart details"""
        totalprice = 0
        cartlist = {}
        cart = []
        self.cur.execute(
            "SELECT * FROM tbl_order_cache WHERE client_id=%(client_id)s",\
            {'client_id': client_id})
        if self.cur.rowcount > 0:
            #loop through to get total price
            rows = self.cur.fetchall()
            for order in rows:
                totalprice = int(totalprice)+int(order[6])
                cartlist.update({
                    'food_id': order[1],
                    'food_name': order[2],
                    'price': order[4],
                    'quantity': order[5],
                    'total': order[6]
                    })
                cart.append(dict(cartlist))

        return jsonify({'Cart': cart, 'totalprice': totalprice}), 200


    def update_order(
            self,
            order_id,
            status):
        """ update Order """
        self.cur.execute("SELECT * FROM tbl_orders WHERE order_id=%(order_id)s",
                         {'order_id': order_id})
        rows = self.cur.fetchone()
        if self.cur.rowcount > 0:
            # update this order details
            self.cur.execute(
                "UPDATE tbl_orders SET status=%s WHERE order_id=%s",
                (status,
                 order_id))
            self.conn.commit()
            self.orderlist.update({
                'order_id': rows[0],
                'order_status': rows[5]})
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
        else:
            return jsonify({"message": "No Order."}), 400

    def check_food_availability(self, food_id):
        """check if food is available in menu"""
        self.cur.execute("SELECT * FROM tbl_foods WHERE food_id=%(food_id)s",\
        {'food_id': food_id})
        if self.cur.rowcount > 0:
            return True
        return False

class Food(object):
    """ food class """
    def __init__(self):
        """ Initialize empty Order list"""
        self.conn = dbcon()
        self.cur = self.conn.cursor()
        self.foodlist = {}
        self.result = []

    def create_food(self, food_name, food_price, food_image):
        """Create food_item"""
        #check if food is created before
        self.cur.execute("SELECT * FROM tbl_foods WHERE food_name=%(food_name)s",
                         {'food_name': food_name})
        if self.cur.rowcount > 0:
            return jsonify({"message": "Ooops! Food already exists."}), 400
        else:
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
            self.result = []
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
            "message": "No Food."}), 200

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
            rows = self.cur.fetchone()
            self.foodlist.update({
                'food_id': rows[0],
                'food_name': rows[1],
                'food_price': rows[2],
                'food_image': rows[3]})
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
