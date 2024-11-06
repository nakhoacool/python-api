from ...domain.repositories.book_repo import BookRepository


def delete_book(repo: BookRepository, book_id: str) -> int:
    res: int = repo.delete(book_id=book_id)
    return res
