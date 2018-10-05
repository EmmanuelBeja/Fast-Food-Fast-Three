"""app/tests_auth.py"""
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

class TestAuth(unittest.TestCase):
    """ Tests for the Auth """
    def setUp(self):
        """setup"""
        app = create_app(config_name='testing')
        self.client = app.test_client()

        self.register_user = json.dumps(dict(
            username="Kamau",
            userphone='0712991415',
            password='Pass123',
            confirmpass='Pass123'))

        self.login_user = json.dumps(dict(
            username="Kamau",
            password='Pass123'))

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


    def test_registration(self):
        """Test for user registration"""
        resource = self.client.post(
            '/v2/auth/signup',
            data=self.register_user, content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Signup Successful')


    def test_username_already_taken(self):
        """ Test if username already taken """
        resource = self.client.post(
            '/v2/auth/signup',
            data=self.register_user, content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Username is taken.')

    def test_login(self):
        """ Test login """
        resource = self.client.post(
            '/v2/auth/login',
            data=self.login_admin,
            content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(
            data['message'].strip(),
            'You are successfully logged in')


    def test_wrong_login_username(self):
        """ Test login validation """
        resource = self.client.post(
            '/v2/auth/login',
            data=json.dumps(dict(username="user5", password='Pass123')),
            content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 401)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Please register first.')


    def test_wrong_login_password(self):
        """ Test wrong login password """
        resource = self.client.post(
            '/v2/auth/login',
            data=json.dumps(dict(username="Person", password='12')),
            content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 403)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Wrong username or password')


    def test_get_users(self):
        """ Test get users """
        resource = self.client.get('/v2/users', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Successful. Users Found')


    def test_get_specific_user(self):
        """Test get specific user by id"""
        resource = self.client.get('/v2/users/2', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Successful. User Found.')


    def test_delete_user(self):
        """Test delete specific user by id"""
        resource = self.client.delete('/v2/users/1', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Delete Successful.')


if __name__ == '__main__':
    unittest.main()
