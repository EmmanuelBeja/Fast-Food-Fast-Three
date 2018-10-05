"""app/tests_food.py"""
import unittest
import json
from app import create_app
from app.database.conn import dbcon
from app.database.conn import init_db


def create_admin():
    """creating an admin user"""
    conn = dbcon()
    cur = conn.cursor()
    #check if user exists
    username = "Person"
    cur.execute("SELECT * FROM tbl_users WHERE username=%(username)s",\
    {'username': username})
    if cur.rowcount > 0:
        return False
    cur.execute("INSERT INTO tbl_users(username, userphone, password, userrole)\
    VALUES(%(username)s, %(userphone)s, %(password)s, %(userrole)s);",\
    {'username': 'Person', 'userphone': '0712991425', 'password': "Pass123", 'userrole': 'admin'})
    conn.commit()

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

        self.create_food3 = json.dumps(dict(
            food_name="burger",
            food_price=200,
            food_image='burger.jpg'))

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


    def test_food_creation(self):
        """ Test for food creation """
        resource = self.client.post(
            '/v2/menu',
            data=self.create_food,
            content_type='application/json', headers=self.headers)

        resource = self.client.post(
            '/v2/menu',
            data=self.create_food2,
            content_type='application/json', headers=self.headers)

        resource = self.client.post(
            '/v2/menu',
            data=self.create_food3,
            content_type='application/json', headers=self.headers)

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
        resource = self.client.get('/v2/food/2', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Successful. Food Found')

    def test_food_deletion(self):
        """Test API can delete an existing order. (DEL request)."""
        res = self.client.delete('/v2/food/1', headers=self.headers)
        self.assertEqual(res.status_code, 201)

    def test_food_can_be_edited(self):
        """ test food can be edited """
        self.test_food_creation()
        resource = self.client.put(
            '/v2/food/2',
            data=self.create_food,
            content_type='application/json', headers=self.headers)

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Update Successful')


if __name__ == '__main__':
    unittest.main()
