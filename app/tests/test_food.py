"""app/tests_food.py"""
import unittest
import os
import json
from flask import session
from app import create_app, init_db
from app.database.conn import dbcon


class TestFood(unittest.TestCase):
    """ Tests for the Orders """
    def setUp(self):
        # pass in test configurations
        app = create_app(config_name='testing')
        self.create_food = json.dumps(dict(
                food_name="mchele",
                food_price=200,
                food_image='mchele.jpg'))

        self.create_food2 = json.dumps(dict(
                food_name="pilau",
                food_price=200,
                food_image='pilau.jpg'))

        self.client = app.test_client()

        self.client.post(
            '/v2/menu',
            data=self.create_food,
            content_type='application/json')

        self.client.post(
            '/v2/menu',
            data=self.create_food2,
            content_type='application/json')

    def test_food_creation(self):
        """ Test for food creation """
        resource = self.client.post(
                '/v2/menu',
                data=self.create_food,
                content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Successful')

    def test_food_can_be_updated(self):
        """ test food can be updated """
        resource = self.client.put(
                '/v2/food/2',
                data=self.create_food,
                content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Successful')

if __name__ == '__main__':
    unittest.main()
