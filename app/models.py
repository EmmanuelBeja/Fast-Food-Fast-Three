"""app/v1/users/models.py"""
from flask import jsonify, session
import re
from .database.conn import dbcon


class User(object):
    """User Class"""
    def __init__(self):
        """ Initialize empty user list"""
        self.conn = dbcon()
        self.cur = self.conn.cursor()

    def create_user(self, username, userphone, password, userRole):
        """Create users"""
        self.users = {}
        if not self.valid_username(username):
            if not self.valid_phone(userphone):
                self.cur.execute("INSERT INTO  tbl_users(username, userphone, password, userrole) VALUES(%(username)s, %(userphone)s, %(password)s, %(userrole)s);",{
                'username': username, 'userphone': userphone, 'password': password, 'userrole': userRole})
                self.conn.commit()

                self.cur.execute("""SELECT * from tbl_users""")
                rows = self.cur.fetchall()
                #remove password from response
                userlistclone = {}
                for user in rows:
                    #remove password from response
                    userlistclone.update({
                        'user_id': user[0],
                        'username': user[1],
                        'userRole': user[4],
                        'userPhone': user[2]})
                    return jsonify({"message": "Successful", "user": userlistclone}), 201
            return jsonify({"message": "Userphone is taken."}), 400
        return jsonify({"message": "Username is taken."}), 400

    def login(self, username, password):
        """login users"""
        if not self.valid_username(username):
            return jsonify({"message": "Please register first."}), 401
        else:
            self.cur.execute("SELECT * FROM tbl_users WHERE username=%(username)s AND password=%(password)s", {'username': username, 'password': password})
            numrows = self.cur.rowcount
            if numrows > 0:
                rows = self.cur.fetchall()
                userlistclone = {}
                for user in rows:
                    session['userid'] = user[0]
                    session['username'] = user[1]
                    session['userrole'] = user[4]
                    #remove password from response
                    userlistclone.update({
                        'user_id': user[0],
                        'username': user[1],
                        'userRole': user[4],
                        'userPhone': user[2]})
                    return jsonify({
                        "message": "You are successfully logged in",
                        "user": userlistclone}), 200
            return jsonify({
                "message": "Wrong username or password"}), 403


    def get_specific_user(self, id):
        """get specific user """
        self.cur.execute("SELECT * FROM tbl_users WHERE userid=%(userid)s", {'userid': id})
        numrows = self.cur.rowcount
        if numrows > 0:
            rows = self.cur.fetchall()
            userlistclone = {}
            for user in rows:
                #remove password from response
                userlistclone.update({
                    'user_id': user[0],
                    'username': user[1],
                    'userRole': user[4],
                    'userPhone': user[2]})
                return jsonify({
                    "message": "Successful",
                    "user": userlistclone}), 200
        return jsonify({"message": "user does not exist"}), 400

    def get_users(self):
        """get all user """
        userlistclone = {}
        result = []
        self.cur.execute("SELECT * FROM tbl_users")
        numrows = self.cur.rowcount
        if numrows > 0:
            rows = self.cur.fetchall()
            for user in rows:
                #remove password from response
                userlistclone.update({
                    'user_id': user[0],
                    'username': user[1],
                    'userRole': user[4],
                    'userPhone': user[2]})
                result.append(dict(userlistclone))
            return jsonify({
                "message": "Successful.",
                "Users": result}), 200
        return jsonify({
            "message": "No user."}), 400

    def update_user(
            self,
            id,
            username,
            userphone,
            password,
            userRole):
        """ update User """
        userlistclone = {}
        self.cur.execute("SELECT * FROM tbl_users WHERE userid=%(userid)s", {'userid': id})
        numrows = self.cur.rowcount
        if numrows > 0:
            rows = self.cur.fetchall()
            #update this user details
            self.cur.execute("UPDATE tbl_users SET username=%s, userphone=%s, password=%s WHERE userid=%s", (username, userphone, password, id))
            self.conn.commit()
            userlistclone = {}
            for user in rows:
                #remove password from response
                userlistclone.update({
                    'user_id': user[0],
                    'username': user[1],
                    'userRole': user[4],
                    'userPhone': user[2]})
                return jsonify({
                    "message": "Successful",
                    "user": userlistclone}), 200
        return jsonify({"message": "No user."}), 400

    def delete_user(self, id):
        """ delete User """
        self.cur.execute("SELECT * FROM tbl_users WHERE userid=%(userid)s", {'userid': id})
        numrows = self.cur.rowcount
        if numrows > 0:
            #delete this user details
            self.cur.execute("DELETE FROM tbl_users WHERE userid=%(userid)s", {'userid': id})
            self.conn.commit()
            return jsonify({
                "message": "Delete Successful."}), 201
        return jsonify({"message": "No user."}), 400

    def valid_username(self, username):
        """check if username exist"""
        self.cur.execute("SELECT * FROM tbl_users WHERE username=%(username)s", {'username': username})
        numrows = self.cur.rowcount
        if numrows > 0:
            return True
        return False

    def valid_phone(self, userphone):
        """check if userphone exist"""
        self.cur.execute("SELECT * FROM tbl_users WHERE userphone=%(userphone)s", {'userphone': userphone})
        numrows = self.cur.rowcount
        if numrows > 0:
            return True
        return False

    def valid_password(self, password):
        """check password length and special characters"""
        if len(password) < 3 or not re.match("^[a-zA-Z0-9_ ]*$", password):
            return False
        else:
            return True
