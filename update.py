from mysql.connector import MySQLConnection, Error
from config import read_config

def update_book(book_id, title):
    config = read_config()
    query = "UPDATE books SET title = %s WHERE id = %s"
    data = (title, book_id)

    affected_rows = 0

    try:
        with MySQLConnection(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query,data)
                affected_rows = cursor.rowcount
            conn.commit()
    except Error as e:
        print(e)
    
    return affected_rows

if __name__ == '__main__':
    affected_rows = update_book(37, 'The Giant on the Hill *** TEST ***')
    print(f'Number of affected rows: {affected_rows}')