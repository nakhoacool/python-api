import os
import sys
from mysql.connector import MySQLConnection, Error
sys.path.append(os.path.dirname(os.path.dirname(__file__)) + "/config")
from config import read_config

def connect(config):
    conn = None

    try:
        conn = MySQLConnection(**config)
        if conn.is_connected():
            print("Connected to MySQL database")
        else:
            print('Connection is failed')

    except Error as error:
        print(error)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
            print('Connection is closed')

if __name__ == '__main__':
    config = read_config()
    connect(config)