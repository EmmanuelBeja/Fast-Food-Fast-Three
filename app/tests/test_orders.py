"""app/tests_orders.py"""
import unittest
import json
from app import create_app
from app.database.conn import dbcon, create_admin


class TestOrders(unittest.TestCase):
    """ Tests for the Orders """
    def setUp(self):
        """setup"""
        app = create_app(config_name='testing')
        self.client = app.test_client()

        self.create_order = json.dumps(dict(
            client_adress='Likoni'))

        self.create_order2 = json.dumps(dict(
            client_adress='Kwale'))

        self.create_order3 = json.dumps(dict(
            client_adress='Mtwapa'))

        self.edit_order = json.dumps(dict(
            food_id=3,
            client_adress='Kwale',
            status='pending'))

        self.login_admin = json.dumps(dict(
            username="Person",
            password='Pass123'))

        create_admin()
        resource = self.client.post(
            '/v2/auth/login',
            data=self.login_admin,
            content_type='application/json')
        data = json.loads(resource.data.decode())
        self.headers = {'Authorization': 'Bearer ' +data['token']}

    def test_add_to_cart(self):
        resource = self.client.get(
            '/v2/users/pick_food/2',
            data=json.dumps(dict()), headers=self.headers)
        self.assertEqual(resource.status_code, 200)


    def test_order_creation(self):
        """ Test for order creation """
        resource = self.client.post(
            '/v2/users/orders',
            data=self.create_order,
            content_type='application/json', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Successful. Order created.')

        resource = self.client.post(
            '/v2/users/orders',
            data=self.create_order2,
            content_type='application/json', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Successful. Order created.')

        resource = self.client.post(
            '/v2/users/orders',
            data=self.create_order3,
            content_type='application/json', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Successful. Order created.')


    def test_get_all_orders(self):
        """ Test for getting all orders """
        self.client.post(
            '/v2/users/orders',
            data=self.create_order,
            content_type='application/json', headers=self.headers)
        self.client.post(
            '/v2/users/orders',
            data=self.create_order2,
            content_type='application/json', headers=self.headers)

        resource = self.client.get(
            '/v2/orders/',
            data=json.dumps(dict()), headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(resource.content_type, 'application/json')


    def test_get_order_by_order_id(self):
        """ Test for getting specific orders """
        resource = self.client.get('/v2/orders/1', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 200)


    def test_order_can_be_edited(self):
        """ test order can be edited """
        resource = self.client.get(
            '/v2/users/pick_food/2',
            data=json.dumps(dict()), headers=self.headers)
        self.assertEqual(resource.status_code, 200)

        self.client.post(
            '/v2/users/orders',
            data=self.create_order,
            content_type='application/json', headers=self.headers)
        self.client.post(
            '/v2/users/orders',
            data=self.create_order2,
            content_type='application/json', headers=self.headers)
        resource = self.client.put(
            '/v2/orders/1',
            data=self.edit_order,
            content_type='application/json', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Update Successful.')

if __name__ == '__main__':
    unittest.main()
