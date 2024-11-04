import sys
import os
from mysql.connector import MySQLConnection, Error
sys.path.append(os.path.dirname(os.path.dirname(__file__)) + "/config")
from config import read_config

def delete_book(book_id):
    config = read_config()
    query = "DELETE FROM books WHERE id = %s"
    data = (book_id,)
    affected_row = 0

    try:
        with MySQLConnection(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, data)
                affected_row = cursor.rowcount
            conn.commit()
    except Error as e:
        print(e)
    
    return affected_row

if __name__ == '__main__':
    affected_rows = delete_book(37)
    print(f'Number of affected rows: {affected_rows}')