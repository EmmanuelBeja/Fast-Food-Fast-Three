"""app/tests_orders.py"""
import unittest
import os
import json
from flask import session
from app import create_app, init_db
from app.database.conn import dbcon


class TestOrders(unittest.TestCase):
    """ Tests for the Orders """
    def setUp(self):
        app = create_app(config_name='testing')
        self.client = app.test_client()

        self.create_order = json.dumps(dict(
                food_id=1,
                client_id=1,
                client_adress='Likoni',
                status='pending'))

        self.client.post(
            '/v2/users/orders',
            data=self.create_order,
            content_type='application/json')


    def test_order_creation(self):
        """ Test for order creation """
        resource = self.client.post(
                '/v2/users/orders',
                data=self.create_order,
                content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Successful')

    def test_order_deletion(self):
        """Test API can delete an existing order. (DELETE request)."""
        self.create_order = json.dumps(dict(
                food_id=1,
                client_id=1,
                client_adress='Likoni',
                status='pending'))

        self.client.post(
            '/v2/users/orders',
            data=self.create_order,
            content_type='application/json')
        res = self.client.delete('/v2/orders/2')
        self.assertEqual(res.status_code, 201)

if __name__ == '__main__':
    unittest.main()
