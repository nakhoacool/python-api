from mysql.connector import MySQLConnection, Error
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
        return e
    
    return affected_row

if __name__ == '__main__':
    affected_rows = delete_book(37)
    print(f'Number of affected rows: {affected_rows}')