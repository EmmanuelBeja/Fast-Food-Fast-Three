""" Database connection """
import os
import psycopg2


from .create_table import queries

def dbcon():
    """db connection"""
    url = os.getenv('DATABASE_URL')
    return psycopg2.connect(url)

def init_db():
    """Initialize db"""
    try:
        connection = dbcon()
        connection.autocommit = True

        #activate cursor
        cursor = connection.cursor()

        for query in queries:
            cursor.execute(query)
        connection.commit()

        create_admin()


    except (Exception, psycopg2.DatabaseError) as error:
        print("DB Error")
        print(error)

def create_admin():
    """creating an admin user"""
    conn = dbcon()
    cur = conn.cursor()
    #check if user exists
    username = "Person"
    password = 'Pass123'
    cur.execute("SELECT * FROM tbl_users WHERE username=%(username)s",\
    {'username': username})
    if cur.rowcount > 0:
        return False
    cur.execute("INSERT INTO tbl_users(username, userphone, password, userrole)\
    VALUES(%(username)s, %(userphone)s, %(password)s, %(userrole)s);",\
    {'username': 'Person', 'userphone': '0712991425', 'password': password, 'userrole': 'admin'})
    conn.commit()
