import sys
import os
from mysql.connector import MySQLConnection, Error
sys.path.append(os.path.dirname(os.path.dirname(__file__)) + "/config")
from config import read_config

def insert_book(title, isbn):
    query = "INSERT INTO books(title,isbn) " \
            "VALUES(%s,%s)"
    args = (title, isbn)
    book_id = None

    try:
        config = read_config()
        with MySQLConnection(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query,args)
                book_id = cursor.lastrowid
            conn.commit()
        return book_id
    except Error as e:
        print(e)

def insert_books(books):
    query = "INSERT INTO books(title,isbn) VALUES(%s,%s)"

    try:
        config = read_config()
        with MySQLConnection(**config) as conn:
            with conn.cursor() as cursor:
                cursor.executemany(query, books)
            conn.commit()
    except Error as e:
        print(e)

if __name__ == '__main__':
    insert_book('A Sudden Light', '9712374172147')
    books = [('The Martian', '9780804139021'), ('Ready Player One', '9780307887443')]
    insert_books(books)