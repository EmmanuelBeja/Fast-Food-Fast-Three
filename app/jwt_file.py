"""jwt auth"""
from datetime import datetime
from flask import request
import jwt
from .database.conn import dbcon

class Auth(object):
    """jwt auth"""
    def __init__(self):
        self.conn = dbcon()
        self.cur = self.conn.cursor()

    def blacklist(self, token):
        """Blacklist"""
        try:
            blacklist_dy = datetime.now()
            status = 'blacklisted'
            self.cur.execute(
                "UPDATE tbl_auth_tokens SET status =%s, blacklist_dy=%s WHERE token=%s",
                (status, blacklist_dy, token))
            self.conn.commit()
            return True
        except Exception as e:
            return e

    def in_blacklist(self, token):
        """if in blacklist """
        try:
            status = 'blacklisted'
            self.cur.execute(
                "SELECT * FROM tbl_auth_tokens WHERE token = %s AND status = %s;",
                (token, status))
            if self.cur.fetchone():
                return True
            return False
        except Exception:
            return False

def is_admin_loggedin():
    """ check if a user is an admin logged in"""
    header = request.headers.get('authorization')
    token = header.split(" ")[1]
    token = jwt.decode(token, 'SECRET_KEY', algorithms=['HS256'])
    user_id = token['userid']
    conn = dbcon()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tbl_users WHERE userid=%(userid)s AND userRole=%(userrole)s",\
    {'userid': user_id, 'userrole': 'admin'})
    if cur.rowcount > 0:
        return True
    return False

def get_logged_in_user_id():
    """get logged in user id"""
    header = request.headers.get('authorization')
    token = header.split(" ")[1]
    token = jwt.decode(token, 'SECRET_KEY', algorithms=['HS256'])
    user_id = token['userid']
    return user_id    