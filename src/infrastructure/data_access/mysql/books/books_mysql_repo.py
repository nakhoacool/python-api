from typing import List, Optional

from mysql.connector import Error, MySQLConnection

from .book_mapper import map_row_to_book

from .....domain.models.book import Book
from .....domain.repositories.book_repo import BookRepository
from ..config.config import read_config


class BooksMySQLRepository(BookRepository):
    def __init__(self):
        self.config = read_config()

    def create(self, title: str, isbn: str) -> Optional[int]:
        query = "INSERT INTO books(title, isbn) VALUES(%s, %s)"
        args = (title, isbn)
        book_id = None

        try:
            with MySQLConnection(**self.config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, args)
                    book_id = cursor.lastrowid
                conn.commit()
            return book_id
        except Error as e:
            raise e

    def get_by_id(self, book_id: str) -> Optional[Book]:
        query = "SELECT * FROM books WHERE id = %s"
        params = (book_id,)
        try:
            with MySQLConnection(**self.config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    row = cursor.fetchone()
                    if row:
                        return map_row_to_book(row)
                    return None
        except Error as e:
            raise e

    def list(self, page_num: int, page_size: int) -> List[Book]:
        offset = (page_num - 1) * page_size
        query = "SELECT * FROM books LIMIT %s, %s"
        params = (offset, page_size)
        books = []

        try:
            with MySQLConnection(**self.config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    rows = cursor.fetchall()
                    for row in rows:
                        books.append(map_row_to_book(row))
            return books
        except Error as e:
            raise e

    def update(self, book_id: str, fields: dict) -> int:
        set_clause = ", ".join([f"{key} = %s" for key in fields.keys()])
        query = f"UPDATE books SET {set_clause} WHERE id = %s"
        data = tuple(fields.values()) + (book_id,)

        try:
            with MySQLConnection(**self.config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, data)
                    affected_rows = cursor.rowcount
                conn.commit()
            return affected_rows
        except Error as e:
            raise e

    def delete(self, book_id: str) -> int:
        query = "DELETE FROM books WHERE id = %s"
        data = (book_id,)

        try:
            with MySQLConnection(**self.config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, data)
                    affected_rows = cursor.rowcount
                conn.commit()
            return affected_rows
        except Error as e:
            raise e
