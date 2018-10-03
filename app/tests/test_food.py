"""app/tests_food.py"""
import unittest
import json
from app import create_app, init_db
from app.database.conn import dbcon


class TestFood(unittest.TestCase):
    """ Tests for the Orders """
    def setUp(self):
        """setup"""
        app = create_app(config_name='testing')
        self.client = app.test_client()

        self.create_food = json.dumps(dict(
            food_name="mchele",
            food_price=200,
            food_image='mchele.jpg'))

        self.create_food2 = json.dumps(dict(
            food_name="pilau",
            food_price=200,
            food_image='pilau.jpg'))

        self.register_user = json.dumps(dict(
            username="useeer",
            userphone='0712991415',
            password='Pass123',
            userRole='admin',
            confirmpass='Pass123'))

        self.login = json.dumps(dict(username="useeer", password='Pass123'))

        self.signupuser = self.client.post(
            '/v2/auth/signup',
            data=self.register_user,
            content_type='application/json')

        self.client.post(
            '/v2/auth/login',
            data=self.login,
            content_type='application/json')

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
        self.assertEqual(data['message'].strip(), 'Successful. Food Created')


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

    def test_get_food_by_food_id(self):
        """ Test for getting specific foods """
        resource = self.client.get('/v2/food/2')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Successful. Food Found')

    def test_food_can_be_edited(self):
        """ test food can be edited """
        resource = self.client.put(
            '/v2/food/2',
            data=self.create_food,
            content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Update Successful')

    def test_food_deletion(self):
        """Test API can delete an existing order. (DELETE request)."""
        res = self.client.delete('/v2/food/1')
        self.assertEqual(res.status_code, 201)

    def tearDown(self):
        conn = dbcon()
        cur = conn.cursor()

        cur.execute("DELETE FROM tbl_users;")
        conn.commit()
        init_db()

if __name__ == '__main__':
    unittest.main()
