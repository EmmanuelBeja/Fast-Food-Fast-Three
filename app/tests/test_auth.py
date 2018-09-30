"""app/tests_auth.py"""
import unittest
import os
import json
from flask import session
from app import create_app, init_db
from app.database.conn import dbcon


class TestAuth(unittest.TestCase):
    """ Tests for the Auth """
    def setUp(self):
        # pass in test configurations
        #config_name = os.getenv('APP_SETTINGS', 'testing')
        #DATABASE_URL="dbname=fastfoodfasttests user=emmanuelbeja password=#1Emmcodes host=localhost"
        app = create_app(config_name='testing')
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

        self.register_user3 = json.dumps(dict(
            username="userfour",
            userphone='0712991415',
            password='Pass123',
            userRole='client',
            confirmpass='Pass123'))

        self.client = app.test_client()
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


    def test_username_exist(self):
        """ Test if username exists """
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

    def test_login(self):
        """ Test login """
        self.register_user3 = json.dumps(dict(
            username="userfour",
            userphone='0712991480',
            password='Pass123',
            userRole='client',
            confirmpass='Pass123'))
        self.client.post(
            '/v2/auth/signup',
            data=self.register_user3, content_type='application/json')

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
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')

    def test_wrong_login_details(self):
        """ Test login validation """
        resource = self.client.post(
                '/v2/auth/login',
                data=json.dumps(dict(username="user1", password='')),
                content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 401)
        self.assertEqual(resource.content_type, 'application/json')

    def test_get_users(self):
        """ Test get users """
        resource = self.client.get('/v2/users')
        self.assertEqual(resource.status_code, 200)

    def test_edit_user_not_found(self):
        self.client.post(
            '/v2/auth/signup',
            data=self.register_user,
            content_type='application/json')


        self.client.post(
            '/v2/auth/signup',
            data=self.register_user2,
            content_type='application/json')
        resource = self.client.put(
                '/v2/users/2',
                data=json.dumps(dict(
                    username="user1 edit",
                    userphone='0712991415',
                    password='pass1234',
                    userRole='admin')), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)

    def test_delete_user(self):
        """Test delete specific user by id"""
        self.client.post(
            '/v2/auth/signup',
            data=self.register_user,
            content_type='application/json')


        self.client.post(
            '/v2/auth/signup',
            data=self.register_user2,
            content_type='application/json')

        resource = self.client.delete('/v2/users/1')
        self.assertEqual(resource.status_code, 201)


    def tearDown(self):
        conn = dbcon()
        cur = conn.cursor()

        cur.execute("DELETE FROM tbl_users;")
        conn.commit()
        init_db()



if __name__ == '__main__':
    unittest.main()
