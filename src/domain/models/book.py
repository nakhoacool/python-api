class Book:
    def __init__(self, id: int, title: str, isbn: str) -> None:
        self._id = id
        self._title = title
        self._isbn = isbn

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def isbn(self):
        return self._isbn

    def to_dict(self):
        return {"id": self.id, "title": self.title, "isbn": self.isbn}
