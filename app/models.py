"""app/v1/users/models.py"""
from flask import jsonify, session
import re
from .database.conn import dbcon


class Food(object):
    def __init__(self):
        """ Initialize empty Order list"""
        self.conn = dbcon()
        self.cur = self.conn.cursor()

    def create_food(self, food_name, food_price, food_image):
        """Create food_item"""
        foodlist = {}
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

    def update_food(self, food_id, food_name, food_price, food_image):
        """ update Food """
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
