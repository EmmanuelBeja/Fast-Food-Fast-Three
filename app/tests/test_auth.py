"""app/tests_auth.py"""
import unittest
import json
from app import create_app
from app.database.conn import dbcon, create_admin


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

        self.register_user_missing_input = json.dumps(dict(
            username="Kamau",
            userphone='0712991415',
            password='Pass123'))

        self.register_user_empty_confirmpass = json.dumps(dict(
            username="Mwilu",
            userphone='0712991415',
            password='Pass123',
            confirmpass=''))

        self.register_user_empty_input = json.dumps(dict(
            username="Mwilu",
            userphone='',
            password='Pass123',
            confirmpass='Pass123'))

        self.register_user_empty_field = json.dumps(dict(
            username="Mwilu",
            password='Pass123',
            confirmpass='Pass123'))

        self.register_user_duplicate_phone = json.dumps(dict(
            username="Mwilu",
            userphone='0712991415',
            password='Pass123',
            confirmpass='Pass123'))

        self.register_short_username = json.dumps(dict(
            username="Mw",
            userphone='0712991415',
            password='Pass123',
            confirmpass='Pass123'))

        self.register_spaced_password = json.dumps(dict(
            username="Mwangi",
            userphone='0712991416',
            password='Pass 123',
            confirmpass='Pass 123'))

        self.register_spaced_username = json.dumps(dict(
            username="Mwa ngangi",
            userphone='0712991416',
            password='Pass123',
            confirmpass='Pass123'))

        self.register_empty_username = json.dumps(dict(
            username='',
            userphone='0712991416',
            password='Pass123',
            confirmpass='Pass123'))

        self.register_short_password = json.dumps(dict(
            username="Mwangangi",
            userphone='0712991416',
            password='Pass',
            confirmpass='Pass'))

        self.register_spaced_userphone = json.dumps(dict(
            username="Mwangangi",
            userphone='0712 991416',
            password='Pass123',
            confirmpass='Pass123'))

        self.edit_user = json.dumps(dict(
            username="Njogu",
            userphone='0712991415',
            password='Pass123',
            confirmpass='Pass123'))

        self.login_user = json.dumps(dict(
            username="Kamau",
            password='Pass123'))

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

    def test_userphone_already_taken(self):
        """ Test if userphone already taken """
        resource = self.client.post(
            '/v2/auth/signup',
            data=self.register_user_duplicate_phone, content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Userphone is taken.')

    def test_register_spaced_password(self):
        """ Test spaced_password """
        resource = self.client.post(
            '/v2/auth/signup',
            data=self.register_spaced_password, content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'password should be one word, no spaces')

    def test_register_spaced_username(self):
        """ Test spaced_username """
        resource = self.client.post(
            '/v2/auth/signup',
            data=self.register_spaced_username, content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'username should be one word, no spaces')

    def test_register_spaced_userphone(self):
        """ Test spaced_userphone """
        resource = self.client.post(
            '/v2/auth/signup',
            data=self.register_spaced_userphone, content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'userphone should be one word, no spaces')

    def test_register_empty_username(self):
        """ Test empty_username """
        resource = self.client.post(
            '/v2/auth/signup',
            data=self.register_empty_username, content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'username must be more than 3 characters')

    def test_register_empty_field(self):
        """ Test empty_field """
        resource = self.client.post(
            '/v2/auth/signup',
            data=self.register_user_empty_field, content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(),\
        "please provide all the fields, missing 'userphone'")

    def test_register_short_password(self):
        """ Test short_password """
        resource = self.client.post(
            '/v2/auth/signup',
            data=self.register_short_password, content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Password should have atleast 5 characters')

    def test_signup_form_field_missing(self):
        """ Test signup form field missing """
        resource = self.client.post(
            '/v2/auth/signup',
            data=self.register_user_missing_input, content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(),\
        "please provide all the fields, missing 'confirmpass'")

    def test_signup_form_field_empty(self):
        """ Test signup form field empty """
        resource = self.client.post(
            '/v2/auth/signup',
            data=self.register_user_empty_input, content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), "userphone required")

    def test_short_signup_username(self):
        """ Test sort signup username"""
        resource = self.client.post(
            '/v2/auth/signup',
            data=self.register_short_username, content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), "username must be more than 3 characters")

    def test_passwords_not_match(self):
        """ Test signup form passwords dont match """
        resource = self.client.post(
            '/v2/auth/signup',
            data=self.register_user_empty_confirmpass, content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), "passwords do not match")

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

    def test_empty_login_password(self):
        """ Test empty password """
        resource = self.client.post(
            '/v2/auth/login',
            data=json.dumps(dict(username="Person", password='')),
            content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 403)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'password required')

    def test_empty_login_field(self):
        """ Test empty field """
        resource = self.client.post(
            '/v2/auth/login',
            data=json.dumps(dict(username="Person")),
            content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 403)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(),\
        "please provide all the fields, missing 'password'")

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

    def test_user_not_admin(self):
        """ Test user not admin """
        resource = self.client.post(
            '/v2/auth/login',
            data=self.login_user,
            content_type='application/json')
        data = json.loads(resource.data.decode())
        self.headers = {'Authorization': 'Bearer ' +data['token']}
        resource = self.client.get('/v2/users', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 401)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'You dont have admin priviledges.')

    def test_auth_headers_missing(self):
        """ Test auth headers missing """
        resource = self.client.get('/v2/users')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 403)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Authorization header missing')

    def test_user_logged_in(self):
        """ Test user logged in """
        resource = self.client.get(
            '/v2/users',
            content_type='application/json', headers={'Authorization': 'Bearer '})
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 401)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Invalid Token. Please login')

    def test_get_specific_user(self):
        """Test get specific user by id"""
        resource = self.client.get('/v2/users/2', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Successful. User Found.')

    def test_get_user_not_found(self):
        """Test get user not found"""
        resource = self.client.get('/v2/users/10', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'user does not exist')

    def test_update_user(self):
        """Test update user"""
        resource = self.client.post(
            '/v2/auth/login',
            data=self.login_admin,
            content_type='application/json')
        data = json.loads(resource.data.decode())
        self.headers = {'Authorization': 'Bearer ' +data['token']}
        resource = self.client.put(
            '/v2/users',
            data=self.edit_user,
            content_type='application/json',
            headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Update Successful')

    def test_delete_user(self):
        """Test delete specific user by id"""
        resource = self.client.delete('/v2/users/1', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Delete Successful.')

    def test_logout_user_not_loggedin(self):
        """Test logout user_not_loggedin"""
        resource = self.client.get('/v2/auth/logout')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 403)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Authorization header missing')

    def test_logout_user(self):
        """Test logout user"""
        resource = self.client.get('/v2/auth/logout', headers=self.headers)
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 200)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Succefuly logout.')


if __name__ == '__main__':
    unittest.main()
