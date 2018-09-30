""" Database connection """
import psycopg2
import os

from .create_table import queries

def dbcon():
    """db connection"""
    url = os.getenv('DATABASE_URL')
    return psycopg2.connect(url)

def init_db():
    try:
        connection = dbcon()
        connection.autocommit = True

        #activate cursor
        cursor = connection.cursor()

        for query in queries:
            cursor.execute(query)
        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("DB Error")
        print(error)
