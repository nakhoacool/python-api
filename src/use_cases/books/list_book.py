from typing import List
from src.domain.models.book import Book
from ...domain.repositories.book_repo import BookRepository


def list_book(repo: BookRepository, page_num: int, page_size: int) -> List[Book]:
    data: List[Book] = repo.list(page_num=page_num, page_size=page_size)
    return data