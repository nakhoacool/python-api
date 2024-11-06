from src.domain.models.book import Book
from ...domain.repositories.book_repo import BookRepository


def get_book_by_id(repo: BookRepository, book_id: str) -> Book | None:
    data: Book | None = repo.get_by_id(book_id=book_id)
    return data