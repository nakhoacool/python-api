from ...domain.repositories.book_repo import BookRepository


def create_book(repo: BookRepository, title: str, isbn: str) -> int:
    res: int = repo.create(title=title, isbn=isbn)
    return res