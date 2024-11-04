import sys
import os
from mysql.connector import MySQLConnection, Error, cursor
sys.path.append(os.path.dirname(os.path.dirname(__file__)) + "/config")
from config import read_config

def query_with_fetchone():
    cursor = None
    conn = None

    try:
        config= read_config()
        conn = MySQLConnection(**config)
        # cursor to interact with the database
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM books")

        #Fetch the first row
        row = cursor.fetchone()
        while row is not None:
            print(row)
            row= cursor.fetchone()
            
    except Error as e:
        print (e)
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def query_with_fetchall():
    try:
        config= read_config()
        conn = MySQLConnection(**config)
        
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM books")

        rows= cursor.fetchall()

        print('Total Row(s):', cursor.rowcount)

        for row in rows:
            print(row)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

def iter_row(cursor: cursor.MySQLCursor, size):
    while True:
        rows = cursor.fetchmany(size)

        if not rows:
            break

        for row in rows:
            yield row

def query_with_fetchmany():
    try:
        config= read_config()
        conn = MySQLConnection(**config)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM books')

        rows = []

        for row in iter_row(cursor, 10):
            rows.append(row)
        
        return rows

    except Error as e:
        print(e)
    
    finally:
        conn.close()
        cursor.close()

if __name__ == '__main__':

    # query_with_fetchone()

    #query_with_fetchall()

    data = query_with_fetchmany()
    print(data)