"""app/v1/users/models.py"""
from flask import jsonify, session
import re
from .database.conn import dbcon



class Order(object):
    def __init__(self):
        """ Initialize empty Order list"""
        self.conn = dbcon()
        self.cur = self.conn.cursor()

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
