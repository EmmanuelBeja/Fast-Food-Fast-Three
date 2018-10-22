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

        self.no_address = json.dumps(dict(
            client_adress=''))

        self.edit_order = json.dumps(dict(
            status='accepted'))

        self.edit_order_wrong_status = json.dumps(dict(
            status='accept'))

        self.edit_order_empty_status = json.dumps(dict(
            status=''))

        self.edit_order_no_status = json.dumps(dict())

        self.login_admin = json.dumps(dict(
            username="Person",
            password='Pass123'))

        self.login_user = json.dumps(dict(
            username="Kamau",
            password='Pass123'))

        create_admin()
        resource = self.client.post(
            '/v2/auth/login',
            data=self.login_admin,
            content_type='application/json')
        data = json.loads(resource.data.decode())
        self.headers = {'Authorization': 'Bearer ' +data['token']}


    def test_add_to_cart(self):
        """adding items to cart"""
        resource = self.client.get(
            '/v2/users/pick_food/1',
            data=json.dumps(dict()), headers=self.headers)
        self.assertEqual(resource.status_code, 201)
        resource = self.client.get(
            '/v2/users/pick_food/2',
            data=json.dumps(dict()), headers=self.headers)
        self.assertEqual(resource.status_code, 201)
        resource = self.client.get(
            '/v2/users/pick_food/1',
            data=json.dumps(dict()), headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Added to cart.')

    def test_user_logged_in(self):
        """ Test user logged in """
        resource = self.client.post(
            '/v2/users/orders',
            data=self.create_order,
            content_type='application/json', headers={'Authorization': 'Bearer '})
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 401)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Invalid Token. Please login')

    def test_missing_auth_headers(self):
        """ Test missing auth headers """
        resource = self.client.post(
            '/v2/users/orders',
            data=self.create_order,
            content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 403)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Authorization header missing')

    def test_cart_details(self):
        """test cart details"""
        resource = self.client.get(
            '/v2/users/cart',
            data=json.dumps(dict()), headers=self.headers)
        self.assertEqual(resource.status_code, 200)

    def test_cart_quantity(self):
        """test cart quantity"""
        resource = self.client.get(
            '/v2/users/cart_quantity',
            data=json.dumps(dict()), headers=self.headers)
        self.assertEqual(resource.status_code, 200)

    def test_remove_from_cart(self):
        """remove all items in cart"""
        resource = self.client.get(
            '/v2/users/cart_cancel',
            data=json.dumps(dict()), headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Order Canceled.')

    def test_order_creation(self):
        """ Test for order creation """
        resource = self.client.get(
            '/v2/users/pick_food/2',
            data=json.dumps(dict()), headers=self.headers)
        self.assertEqual(resource.status_code, 201)
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



    def test_missing_address(self):
        """ Test for missing address """
        resource = self.client.get(
            '/v2/users/pick_food/2',
            data=json.dumps(dict()), headers=self.headers)
        self.assertEqual(resource.status_code, 201)
        resource = self.client.post(
            '/v2/users/orders',
            data=self.no_address,
            content_type='application/json', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'adress required')

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
        self.assertEqual(resource.status_code, 200)

    def test_get_user_orders(self):
        """ Test for getting user orders """
        self.client.post(
            '/v2/users/orders',
            data=self.create_order,
            content_type='application/json', headers=self.headers)
        self.client.post(
            '/v2/users/orders',
            data=self.create_order2,
            content_type='application/json', headers=self.headers)
        resource = self.client.get('/v2/users/orders/4', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Successful. User orders found.')

    def test_get_user_order_not_found(self):
        """ Test for getting user order not found """
        resource = self.client.get('/v2/users/orders/10', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'No Order.')


    def test_get_order_by_order_id(self):
        """ Test for getting specific orders """
        resource = self.client.get('/v2/orders/1', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Successful. Order found.')

    def test_get_order_not_found(self):
        """ Test for getting an order not found """
        resource = self.client.get('/v2/orders/10', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'No Order.')

    def test_order_edit(self):
        """ test order edit """
        resource = self.client.get(
            '/v2/users/pick_food/2',
            data=json.dumps(dict()), headers=self.headers)
        self.assertEqual(resource.status_code, 201)
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
        #self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Update Successful.')

    def test_order_edit_wrong_status(self):
        """ test order edit """
        resource = self.client.get(
            '/v2/users/pick_food/2',
            data=json.dumps(dict()), headers=self.headers)
        self.assertEqual(resource.status_code, 201)
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
            data=self.edit_order_wrong_status,
            content_type='application/json', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(),\
        'Wrong order status. Allowed statuses: accepted, declined, completed')

    def test_order_edit_empty_status(self):
        """ test order edit empty status"""
        resource = self.client.get(
            '/v2/users/pick_food/2',
            data=json.dumps(dict()), headers=self.headers)
        self.assertEqual(resource.status_code, 201)
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
            data=self.edit_order_empty_status,
            content_type='application/json', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'status required')

    def test_order_edit_no_status(self):
        """ test order edit no status"""
        resource = self.client.get(
            '/v2/users/pick_food/2',
            data=json.dumps(dict()), headers=self.headers)
        self.assertEqual(resource.status_code, 201)
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
            data=self.edit_order_no_status,
            content_type='application/json', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), "please provide all the fields, missing 'status'")

    def test_edit_order_not_found(self):
        """ test edit order not found """
        resource = self.client.put(
            '/v2/orders/10',
            data=self.edit_order,
            content_type='application/json', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'], 'No Order.')

    def test_delete_order(self):
        """ test delete order """
        resource = self.client.get(
            '/v2/users/pick_food/2',
            data=json.dumps(dict()), headers=self.headers)
        self.assertEqual(resource.status_code, 201)
        self.client.post(
            '/v2/users/orders',
            data=self.create_order,
            content_type='application/json', headers=self.headers)
        self.client.post(
            '/v2/users/orders',
            data=self.create_order2,
            content_type='application/json', headers=self.headers)
        resource = self.client.delete(
            '/v2/orders/2', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Delete Successful.')

    def test_delete_order_not_found(self):
        """ test delete order not found """
        resource = self.client.delete(
            '/v2/orders/10', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'No Order.')

    def test_user_not_admin(self):
        """ Test user not admin"""
        resource = self.client.post(
            '/v2/auth/login',
            data=self.login_user,
            content_type='application/json')
        data = json.loads(resource.data.decode())
        self.headers = {'Authorization': 'Bearer ' +data['token']}
        resource = self.client.get(
            '/v2/orders/',
            data=json.dumps(dict()), headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 401)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'You dont have admin priviledges.')

    def test_user_not_admin_edit_order(self):
        """ Test user not admin"""
        resource = self.client.post(
            '/v2/auth/login',
            data=self.login_user,
            content_type='application/json')
        data = json.loads(resource.data.decode())
        self.headers = {'Authorization': 'Bearer ' +data['token']}
        resource = self.client.get(
            '/v2/orders/1',
            data=json.dumps(dict()), headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 401)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'You dont have admin priviledges.')

if __name__ == '__main__':
    unittest.main()
