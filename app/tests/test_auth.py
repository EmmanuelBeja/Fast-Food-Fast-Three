"""app/tests_auth.py"""
import unittest
import json
from app import create_app
from app.database.conn import dbcon
from app.database.conn import init_db

class TestAuth(unittest.TestCase):
    """ Tests for the Auth """
    def setUp(self):
        """setup"""

        app = create_app(config_name='testing')
        self.client = app.test_client()

        self.conn = dbcon()
        self.cur = self.conn.cursor()

        self.register_user = json.dumps(dict(
            username="user6",
            userphone='0712991415',
            password='Pass123',
            userRole='client',
            confirmpass='Pass123'))

        self.register_user2 = json.dumps(dict(
            username="usertwo",
            userphone='0712991415',
            password='Pass123',
            userRole='client',
            confirmpass='Pass123'))

        self.register_user4 = json.dumps(dict(
            username="userfour",
            userphone='0712991415',
            password='Pass123',
            userRole='client',
            confirmpass='Pass123'))

        self.client.post(
            '/v2/auth/signup',
            data=self.register_user,
            content_type='application/json')

        self.client.post(
            '/v2/auth/signup',
            data=self.register_user2,
            content_type='application/json')


    def test_registration(self):
        """Test for user registration"""
        resource = self.client.post(
            '/v2/auth/signup',
            data=json.dumps(dict(
                username="userkamau",
                userphone='0712991460',
                password='pass1234',
                userRole='client',
                confirmpass='pass1234')), content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Successful')


    def test_username_already_taken(self):
        """ Test if username already taken """
        resource = self.client.post(
            '/v2/auth/signup',
            data=json.dumps(dict(
                username="user6",
                userphone='0712991440',
                password='pass1234',
                userRole='client',
                confirmpass='pass1234')), content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Username is taken.')


    def test_login(self):
        """ Test login """
        self.client.post(
            '/v2/auth/signup',
            data=json.dumps(dict(
                username="userfour",
                userphone='0712991480',
                password='Pass123',
                userRole='client',
                confirmpass='Pass123')), content_type='application/json')
        resource = self.client.post(
            '/v2/auth/login',
            data=json.dumps(dict(username="userfour", password='Pass123')),
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
        self.client.post(
            '/v2/auth/signup',
            data=json.dumps(dict(
                username="user1",
                userphone='0712991490',
                password='Pass123',
                userRole='client',
                confirmpass='Pass123')), content_type='application/json')
        resource = self.client.post(
            '/v2/auth/login',
            data=json.dumps(dict(username="user1", password='12')),
            content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 403)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Wrong username or password')


    def test_get_users(self):
        """ Test get users """
        self.client.post(
            '/v2/auth/signup',
            data=json.dumps(dict(
                username="userfour",
                userphone='0712991480',
                password='Pass123',
                userRole='client',
                confirmpass='Pass123')), content_type='application/json')
        resource = self.client.post(
            '/v2/auth/login',
            data=json.dumps(dict(username="userfour", password='Pass123')),
            content_type='application/json')
        data = json.loads(resource.data.decode())
        resource = self.client.get('/v2/users')
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'You are successfully logged in')


    def test_get_specific_user(self):
        """Test get specific user by id"""
        self.client.post(
            '/v2/auth/signup',
            data=json.dumps(dict(
                username="userfour",
                userphone='0712991480',
                password='Pass123',
                userRole='client',
                confirmpass='Pass123')), content_type='application/json')
        resource = self.client.post(
            '/v2/auth/login',
            data=json.dumps(dict(username="userfour", password='Pass123')),
            content_type='application/json')
        resource = self.client.get('/v2/users')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Successful.')


    def test_edit_user_not_found(self):
        """test if user exists"""
        self.client.post(
            '/v2/auth/signup',
            data=json.dumps(dict(
                username="userfour",
                userphone='0712991480',
                password='Pass123',
                userRole='client',
                confirmpass='Pass123')), content_type='application/json')

        resource = self.client.post(
            '/v2/auth/login',
            data=json.dumps(dict(username="userfo", password='Pass123')),
            content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 401)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Please register first.')


    def test_delete_user(self):
        """Test delete specific user by id"""
        self.client.post(
            '/v2/auth/signup',
            data=json.dumps(dict(
                username="userfour",
                userphone='0712991480',
                password='Pass123',
                userRole='client',
                confirmpass='Pass123')), content_type='application/json')
        resource = self.client.post(
            '/v2/auth/login',
            data=json.dumps(dict(username="userfour", password='Pass123')),
            content_type='application/json')
        resource = self.client.delete('/v2/users/1')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Delete Successful.')



    def tearDown(self):
        conn = dbcon()
        cur = conn.cursor()

        cur.execute("DELETE FROM tbl_users;")
        conn.commit()
        init_db()

if __name__ == '__main__':
    unittest.main()
