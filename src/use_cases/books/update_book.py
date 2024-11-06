from ...domain.repositories.book_repo import BookRepository


def update_book(repo: BookRepository, book_id: str, fields: dict):
    return repo.update(book_id=book_id, fields=fields)