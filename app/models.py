"""app/v1/users/models.py"""
from flask import jsonify, session
import re
from .database.conn import dbcon


class Order(object):
    def __init__(self):
        """ Initialize empty Order list"""
        self.conn = dbcon()
        self.cur = self.conn.cursor()

    def create_order(self, food_id, client_id, client_adress, status):
        """Create order_item"""
        orderlist = {}
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

    def get_user_orders(self, client_id):
        orderlist = {}
        result = []
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
