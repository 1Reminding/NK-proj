# db_connection.py
import pymysql

def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='xqh20040327',
        database='shoppingplatform',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection
