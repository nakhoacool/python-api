import json
import unittest
from unittest.mock import patch

from aws_lambda_typing import events, responses

from ..update_book_handler import handler


class TestUpdateBookHandler(unittest.TestCase):
    """
    Test case for update_book_handler
    """

    def test_no_path_parameter(self):
        """
        Should return 400 if path parameter not provided
        """
        event: events.APIGatewayProxyEventV2 = {}
        context = {}

        response: responses.APIGatewayProxyResponseV2 = handler(event, context)

        self.assertEqual(response.get("statusCode"), 400)
        self.assertEqual(
            json.loads(response.get("body") or "{}"),
            {"message": "path parameters is required"},
        )

    def test_no_bookId(self):
        """
        Should return 400 if id not provided
        """
        event: events.APIGatewayProxyEventV2 = {"pathParameters": {}}
        context = {}

        response: responses.APIGatewayProxyResponseV2 = handler(event, context)

        self.assertEqual(response.get("statusCode"), 400)
        self.assertEqual(
            json.loads(response.get("body") or "{}"),
            {"message": "id is required in path parameter"},
        )

    def test_no_body(self):
        """
        Should return 400 if body is missing
        """
        event: events.APIGatewayProxyEventV2 = {"pathParameters": {"bookId": "1"}}
        context = {}

        response: responses.APIGatewayProxyResponseV2 = handler(event, context)

        self.assertEqual(response.get("statusCode"), 400)
        self.assertEqual(
            json.loads(response.get("body") or "{}"), {"message": "body is required"}
        )

    def test_no_title_or_isbn_put_method(self):
        """
        Should return 400 if title or isbn is missing in body
        """
        event: events.APIGatewayProxyEventV2 = {
            "pathParameters": {"bookId": "1"},
            "body": "{}",
            "requestContext": {"http": {"method": "PUT"}},
        }  # type: ignore
        context = {}

        response: responses.APIGatewayProxyResponseV2 = handler(event, context)

        self.assertEqual(response.get("statusCode"), 400)
        self.assertEqual(
            json.loads(response.get("body") or "{}"),
            {"message": "title and isbn are required"},
        )

    def test_no_title_or_isbn_patch_method(self):
        """
        Should return 400 if title or isbn is missing in body
        """
        event: events.APIGatewayProxyEventV2 = {
            "pathParameters": {"bookId": "1"},
            "body": "{}",
            "requestContext": {"http": {"method": "PATCH"}},
        }  # type: ignore
        context = {}

        response: responses.APIGatewayProxyResponseV2 = handler(event, context)

        self.assertEqual(response.get("statusCode"), 400)
        self.assertEqual(
            json.loads(response.get("body") or "{}"),
            {"message": "title or isbn is required"},
        )

    @patch("src.functions.books.update_book_handler.update_book")
    @patch("src.functions.books.update_book_handler.BooksMySQLRepository")
    def test_exception(self, mock_repository, mock_update_book):
        """
        Should return 500 if exception is raised
        """
        mock_update_book.side_effect = Exception("error")
        event: events.APIGatewayProxyEventV2 = {
            "pathParameters": {"bookId": "1"},
            "body": '{"title": "new title"}',
            "requestContext": {"http": {"method": "PATCH"}},
        }  # type: ignore
        context = {}

        response: responses.APIGatewayProxyResponseV2 = handler(event, context)

        self.assertEqual(response.get("statusCode"), 500)
        self.assertEqual(json.loads(response.get("body") or "{}"), {"message": "error"})
        mock_update_book.assert_called_once()
        mock_repository.assert_called_once()

    @patch("src.functions.books.update_book_handler.update_book")
    @patch("src.functions.books.update_book_handler.BooksMySQLRepository")
    def test_book_not_found(self, mock_repository, mock_update_book):
        """
        Should return 404 if book is not found
        """
        mock_update_book.return_value = 0
        event: events.APIGatewayProxyEventV2 = {
            "pathParameters": {"bookId": "1"},
            "body": '{"title": "new title"}',
            "requestContext": {"http": {"method": "PATCH"}},
        }  # type: ignore
        context = {}

        response: responses.APIGatewayProxyResponseV2 = handler(event, context)

        self.assertEqual(response.get("statusCode"), 404)
        self.assertEqual(
            json.loads(response.get("body") or "{}"),
            {"message": "Book with id 1 not found"},
        )

    @patch("src.functions.books.update_book_handler.update_book")
    @patch("src.functions.books.update_book_handler.BooksMySQLRepository")
    def test_patch_title(self, mock_repository, mock_update_book):
        """
        Should return 200 if only title is provided in body
        """
        event: events.APIGatewayProxyEventV2 = {
            "pathParameters": {"bookId": "1"},
            "body": '{"title": "new title"}',
            "requestContext": {"http": {"method": "PATCH"}},
        }  # type: ignore
        context = {}

        response: responses.APIGatewayProxyResponseV2 = handler(event, context)

        self.assertEqual(response.get("statusCode"), 200)
        self.assertEqual(
            json.loads(response.get("body") or "{}"), {"message": "Book updated"}
        )
        mock_repository.assert_called_once()
        mock_update_book.assert_called_once()

    @patch("src.functions.books.update_book_handler.update_book")
    @patch("src.functions.books.update_book_handler.BooksMySQLRepository")
    def test_patch_isbn(self, mock_repository, mock_update_book):
        """
        Should return 200 if only isbn is provided in body
        """
        event: events.APIGatewayProxyEventV2 = {
            "pathParameters": {"bookId": "1"},
            "body": '{"isbn": "new isbn"}',
            "requestContext": {"http": {"method": "PATCH"}},
        }  # type: ignore
        context = {}

        response: responses.APIGatewayProxyResponseV2 = handler(event, context)

        self.assertEqual(response.get("statusCode"), 200)
        self.assertEqual(
            json.loads(response.get("body") or "{}"), {"message": "Book updated"}
        )
        mock_update_book.assert_called_once()
        mock_repository.assert_called_once()

    @patch("src.functions.books.update_book_handler.update_book")
    @patch("src.functions.books.update_book_handler.BooksMySQLRepository")
    def test_put_method(self, mock_repository, mock_update_book):
        """
        Should return 200 if method is PUT
        """
        event: events.APIGatewayProxyEventV2 = {
            "pathParameters": {"bookId": "1"},
            "body": '{"title": "new title", "isbn": "new isbn"}',
            "requestContext": {"http": {"method": "PUT"}},
        }  # type: ignore
        context = {}

        response: responses.APIGatewayProxyResponseV2 = handler(event, context)

        self.assertEqual(response.get("statusCode"), 200)
        self.assertEqual(
            json.loads(response.get("body") or "{}"), {"message": "Book updated"}
        )
        mock_repository.assert_called_once()
        mock_update_book.assert_called_once()


if __name__ == "__main__":
    unittest.main()
