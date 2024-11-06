from .....domain.models.book import Book


def map_row_to_book(row) -> Book:
    return Book(id=row[0], title=row[1], isbn=row[2])
