import json
import unittest
from unittest.mock import patch

from aws_lambda_typing import events, responses

from ....domain.models.book import Book
from ..list_books_handler import handler


class TestListBooksHandler(unittest.TestCase):
    """
    Test cases for the list_books_handler function.
    """

    def test_no_path_parameter(self):
        """
        Test that the handler return 400 if no query string.
        """
        event: events.APIGatewayProxyEventV2 = {}
        context = {}

        response: responses.APIGatewayProxyResponseV2 = handler(
            event=event, context=context
        )

        self.assertEqual(response.get("statusCode"), 400)
        self.assertEqual(
            json.loads(response.get("body") or "{}"),
            {"message": "page_num and page_size are required"},
        )

    def test_no_page_num_or_page_size(self):
        """
        Test that the handler return 400 if no page num or page size in query string parameter
        """
        event: events.APIGatewayProxyEventV2 = {
            "queryStringParameters": {"page_num": "1"}
        }
        context = {}

        response: responses.APIGatewayProxyResponseV2 = handler(event, context)

        self.assertEqual(response.get("statusCode"), 400)
        self.assertEqual(
            json.loads(response.get("body") or "{}"),
            {"message": "page_num and page_size are required"},
        )

    def test_page_num_or_page_size_not_integer(self):
        """
        Test that the handler return 400 if page num or page size is not integer
        """
        event: events.APIGatewayProxyEventV2 = {
            "queryStringParameters": {"page_num": "a", "page_size": "b"}
        }
        context = {}

        response: responses.APIGatewayProxyResponseV2 = handler(event, context)

        self.assertEqual(response.get("statusCode"), 400)
        self.assertEqual(
            json.loads(response.get("body") or "{}"),
            {"message": "page_num and page_size must be integers"},
        )

    @patch("src.functions.books.list_books_handler.BooksMySQLRepository")
    @patch("src.functions.books.list_books_handler.list_book")
    def test_exception_during_list_books(self, mock_list_book, mock_repo):
        """
        Test that the handler returns a 500 status code when an exception occurs during book retrieval.
        """
        mock_list_book.side_effect = Exception("Something went wrong")
        event: events.APIGatewayProxyEventV2 = {
            "queryStringParameters": {"page_num": "1", "page_size": "10"}
        }
        context = {}

        response: responses.APIGatewayProxyResponseV2 = handler(event, context)

        self.assertEqual(response.get("statusCode"), 500)
        self.assertEqual(
            json.loads(response.get("body") or "{}")["message"], "Something went wrong"
        )

    @patch("src.functions.books.list_books_handler.BooksMySQLRepository")
    @patch("src.functions.books.list_books_handler.list_book")
    def test_list_books(self, mock_list_book, mock_repo):
        """
        Test that the handler returns a 200 status code and list of books.
        """
        mock_list_book.return_value = [
            Book(id=1, title="Book 1", isbn="1234"),
            Book(id=2, title="Book 2", isbn="5678"),
        ]
        event: events.APIGatewayProxyEventV2 = {
            "queryStringParameters": {"page_num": "1", "page_size": "10"}
        }
        context = {}

        response: responses.APIGatewayProxyResponseV2 = handler(event, context)

        self.assertEqual(response.get("statusCode"), 200)
        self.assertEqual(
            json.loads(response.get("body") or "{}"),
            {
                "data": [
                    {"id": 1, "title": "Book 1", "isbn": "1234"},
                    {"id": 2, "title": "Book 2", "isbn": "5678"},
                ]
            },
        )


if __name__ == "__main__":
    unittest.main()
