from abc import ABC, abstractmethod
from typing import List, Optional

from ..models.book import Book


class BookRepository(ABC):
    @abstractmethod
    def create(self, title: str, isbn: str) -> Optional[int]:
        pass

    @abstractmethod
    def get_by_id(self, book_id: str) -> Optional[Book]:
        pass

    @abstractmethod
    def list(self, page_num: int, page_size: int) -> List[Book]:
        pass

    @abstractmethod
    def update(self, book_id: str, fields: dict) -> int:
        pass

    @abstractmethod
    def delete(self, book_id: str) -> int:
        pass
