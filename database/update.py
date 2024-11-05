from mysql.connector import Error, MySQLConnection

from config import read_config


def update_book(book_id, fields: dict):
    config = read_config()
    set_clause = ", ".join([f"{key} = %s" for key in fields.keys()])
    query = f"UPDATE books SET {set_clause} WHERE id = %s"
    data = tuple(fields.values()) +  (book_id,)

    affected_rows = 0

    try:
        with MySQLConnection(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, data)
                affected_rows = cursor.rowcount
            conn.commit()
    except Error as e:
        return e

    return affected_rows


if __name__ == "__main__":
    affected_rows = update_book(37, "The Giant on the Hill *** TEST ***")
    print(f"Number of affected rows: {affected_rows}")
