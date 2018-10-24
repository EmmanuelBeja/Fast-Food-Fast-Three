"""app/tests_food.py"""
import unittest
import json
from app import create_app
from app.database.conn import dbcon, create_admin


class TestFood(unittest.TestCase):
    """ Tests for the Orders """
    def setUp(self):
        """setup"""
        app = create_app(config_name='testing')
        self.client = app.test_client()

        self.create_food = json.dumps(dict(
            food_name="mchele",
            food_price='200',
            food_image='mchele.jpg'))

        self.create_food2 = json.dumps(dict(
            food_name="pilau",
            food_price='200',
            food_image='pilau.jpg'))

        self.create_food3 = json.dumps(dict(
            food_name="burger",
            food_price='200',
            food_image='burger.jpg'))

        self.edit_food = json.dumps(dict(
            food_name="pizza",
            food_price='1000',
            food_image='pizza.jpg'))

        self.create_food_empty_food_name = json.dumps(dict(
            food_name="",
            food_price='200',
            food_image='burger.jpg'))

        self.create_food_spaced_food_name = json.dumps(dict(
            food_name="burg er",
            food_price='200',
            food_image='burger.jpg'))

        self.create_food_empty_food_price = json.dumps(dict(
            food_name="wali",
            food_price='',
            food_image='burger.jpg'))

        self.create_food_spaced_food_price = json.dumps(dict(
            food_name="wali",
            food_price='20 0',
            food_image='burger.jpg'))

        self.create_food_no_food_price = json.dumps(dict(
            food_name="wali",
            food_image='burger.jpg'))

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


    def test_food_creation(self):
        """ Test for food creation """
        resource = self.client.post(
            '/v2/menu',
            data=self.create_food3,
            content_type='application/json', headers=self.headers)
        resource = self.client.post(
            '/v2/menu',
            data=self.create_food2,
            content_type='application/json', headers=self.headers)
        data = json.loads(resource.data.decode())
        #self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Successful. Food Created')

    def test_empty_food_name(self):
        """food name empty"""
        resource = self.client.post(
            '/v2/menu',
            data=self.create_food_empty_food_name,
            content_type='application/json', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Food name required')

    def test_spaced_food_name(self):
        """food name spaced"""
        resource = self.client.post(
            '/v2/menu',
            data=self.create_food_spaced_food_name,
            content_type='application/json', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(),\
        'Food Name should be one word, no spaces')

    def test_empty_food_price(self):
        """food price empty"""
        resource = self.client.post(
            '/v2/menu',
            data=self.create_food_empty_food_price,
            content_type='application/json', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Food Price required')

    def test_spaced_food_price(self):
        """food price spaced"""
        resource = self.client.post(
            '/v2/menu',
            data=self.create_food_spaced_food_price,
            content_type='application/json', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'food price should be one word, no spaces')

    def test_no_food_price(self):
        """no food price"""
        resource = self.client.post(
            '/v2/menu',
            data=self.create_food_no_food_price,
            content_type='application/json', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(),\
        "please provide all the fields, missing 'food_price'")

    def test_auth_headers_missing(self):
        """ Test authorization headers missing """
        resource = self.client.post(
            '/v2/menu',
            data=self.create_food3,
            content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 403)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Authorization header missing')

    def test_user_not_admin(self):
        """ Test user not admin """
        resource = self.client.post(
            '/v2/auth/login',
            data=self.login_user,
            content_type='application/json')
        data = json.loads(resource.data.decode())
        self.headers = {'Authorization': 'Bearer ' +data['token']}
        resource = self.client.post(
            '/v2/menu',
            data=self.create_food3,
            content_type='application/json', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 401)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'You dont have admin priviledges.')

    def test_get_all_foods(self):
        """ Test for getting all foods """
        resource = self.client.get(
            '/v2/menu',
            data=json.dumps(dict()),
            content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Successful. Food Found')

    def test_user_not_admin_get_food(self):
        """ Test user not admin geting food"""
        resource = self.client.post(
            '/v2/auth/login',
            data=self.login_user,
            content_type='application/json')
        data = json.loads(resource.data.decode())
        self.headers = {'Authorization': 'Bearer ' +data['token']}
        resource = self.client.get('/v2/food/2', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 401)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'You dont have admin priviledges.')

    def test_get_food_by_food_id(self):
        """ Test for getting specific foods """
        resource = self.client.get('/v2/food/2', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Successful. Food Found')

    def test_get_food_not_found(self):
        """ Test for getting specific food not found """
        resource = self.client.get('/v2/food/10', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'No Food.')

    def test_create_existing_food(self):
        """ Test for creating existing food """
        resource = self.client.post(
            '/v2/menu',
            data=self.create_food,
            content_type='application/json', headers=self.headers)
        resource = self.client.post(
            '/v2/menu',
            data=self.create_food,
            content_type='application/json', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Ooops! Food already exists.')

    def test_food_deletion(self):
        """Test API can delete an existing order. (DEL request)."""
        resource = self.client.delete('/v2/food/3', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Delete Successful.')

    def test_food_deleted_not_found(self):
        """Test delete food not found"""
        resource = self.client.delete('/v2/food/10', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'No Food.')

    def test_food_edit(self):
        """ test food can be edited """
        self.test_food_creation()
        resource = self.client.put(
            '/v2/food/2',
            data=self.edit_food,
            content_type='application/json', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Update Successful')

    def test_food_edited_not_found(self):
        """ test food can be edited """
        resource = self.client.put(
            '/v2/food/10',
            data=self.edit_food,
            content_type='application/json', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'No Food.')


if __name__ == '__main__':
    unittest.main()
