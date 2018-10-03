"""app/tests_orders.py"""
import unittest
import json
from app import create_app, init_db
from app.database.conn import dbcon


class TestOrders(unittest.TestCase):
    """ Tests for the Orders """
    def setUp(self):
        """setup"""
        app = create_app(config_name='testing')
        self.client = app.test_client()

        self.register_user = json.dumps(dict(
            username="useer",
            userphone='0712991415',
            password='Pass123',
            userRole='admin',
            confirmpass='Pass123'))

        self.login = json.dumps(dict(username="useer", password='Pass123'))

        self.create_order = json.dumps(dict(
            food_id=1,
            client_id=1,
            client_adress='Likoni',
            status='pending'))

        self.signupuser = self.client.post(
            '/v2/auth/signup',
            data=self.register_user,
            content_type='application/json')

        self.client.post(
            '/v2/auth/login',
            data=self.login,
            content_type='application/json')

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


    def test_get_all_orders(self):
        """ Test for getting all orders """
        resource = self.client.get(
            '/v2/orders/',
            data=json.dumps(dict()),
            content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Successful.')


    def test_get_order_by_order_id(self):
        """ Test for getting specific orders """
        resource = self.client.get('/v2/orders/1')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(data['message'].strip(), 'Successful.')


    def test_order_can_be_edited(self):
        """ test order can be edited """
        resource = self.client.put(
            '/v2/orders/1',
            data=self.create_order,
            content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Successful')


    def test_order_deletion(self):
        """Test API can delete an existing order. (DELETE request)."""
        resource = self.client.delete('/v2/orders/1')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(data['message'].strip(), 'Delete Successful.')


    def tearDown(self):
        conn = dbcon()
        cur = conn.cursor()
        cur.execute("DELETE FROM tbl_users;")
        conn.commit()
        init_db()

if __name__ == '__main__':
    unittest.main()
