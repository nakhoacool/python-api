from mysql.connector import MySQLConnection, Error, cursor
from config import read_config

def query_with_fetchone(id):
    cursor = None
    conn = None

    params = (id,)

    try:
        config= read_config()
        conn = MySQLConnection(**config)
        # cursor to interact with the database
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM books WHERE id = %s", params=params)

        data = []
        #Fetch the first row
        row = cursor.fetchone()
        while row is not None:
            data.append({
                'id': row[0],
                'title': row[1],
                'isbn': row[2]
            })
            row= cursor.fetchone()
        
        return data
            
    except Error as e:
        return e
    
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

def query_with_fetchmany(page_number=1, page_size=10):
    try:
        config= read_config()
        conn = MySQLConnection(**config)
        cursor = conn.cursor()

        offset = (page_number - 1) * page_size

        cursor.execute('SELECT * FROM books LIMIT %s, %s', (offset, page_size))

        rows = []

        for row in iter_row(cursor, page_size):
            rows.append({
                'id': row[0],
                'title': row[1],
                'isbn': row[2]
            })
        
        return rows

    except Error as e:
        return e
    
    finally:
        conn.close()
        cursor.close()

if __name__ == '__main__':

    # query_with_fetchone()

    #query_with_fetchall()

    page_number = 1
    page_size = 10

    data = query_with_fetchmany(page_number=page_number, page_size=page_size)
    print(data)