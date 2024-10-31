from mysql.connector import MySQLConnection, Error, cursor
from config import read_config

def query_with_fetchone(config):
    cursor = None
    conn = None

    try:
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

def query_with_fetchall(config):
    try:
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

def query_with_fetchmany(config):
    try:
        conn = MySQLConnection(**config)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM books')

        for row in iter_row(cursor, 10):
            print(row)

    except Error as e:
        print(e)
    
    finally:
        conn.close()
        cursor.close()

if __name__ == '__main__':
    config= read_config()

    # query_with_fetchone(config)

    #query_with_fetchall(config=config)

    query_with_fetchmany(config)