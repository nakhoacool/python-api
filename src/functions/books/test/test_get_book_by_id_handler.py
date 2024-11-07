import json
import unittest
from unittest.mock import patch

from aws_lambda_typing import events, responses

from ....domain.models.book import Book
from ..get_book_by_id_handler import handler


class TestGetBookByIdHandler(unittest.TestCase):
    """
    Test cases for the get_book_by_id_handler function.
    """

    def test_no_path_parameters_in_event(self):
        """
        Test that the handler returns a 400 status code when the event has no path parameters.
        """
        event: events.APIGatewayProxyEventV2 = {}
        context = {}
        response: responses.APIGatewayProxyResponseV2 = handler(event, context)
        self.assertEqual(response.get("statusCode"), 400)
        self.assertEqual(
            json.loads(response.get("body") or "{}")["message"],
            "path parameters is required",
        )

    def test_no_book_id_in_path_parameters(self):
        """
        Test that the handler returns a 400 status code when the event path parameters has no bookId.
        """
        event: events.APIGatewayProxyEventV2 = {"pathParameters": {}}
        context = {}
        response: responses.APIGatewayProxyResponseV2 = handler(
            event=event, context=context
        )
        self.assertEqual(response.get("statusCode"), 400)
        self.assertEqual(
            json.loads(response.get("body") or "{}")["message"],
            "id is required in path parameter",
        )

    @patch("src.functions.books.get_book_by_id_handler.BooksMySQLRepository")
    @patch("src.functions.books.get_book_by_id_handler.get_book_by_id")
    def test_exception_during_get_book(self, mock_get_book_by_id, mock_repo):
        """
        Test that the handler returns a 500 status code when an exception occurs during book retrieval.
        """
        mock_get_book_by_id.side_effect = Exception("Something went wrong")
        event: events.APIGatewayProxyEventV2 = {"pathParameters": {"bookId": "1"}}
        context = {}

        response: responses.APIGatewayProxyResponseV2 = handler(event, context)

        self.assertEqual(response.get("statusCode"), 500)
        self.assertEqual(
            json.loads(response.get("body") or "{}")["message"], "Something went wrong"
        )

    @patch("src.functions.books.get_book_by_id_handler.BooksMySQLRepository")
    @patch("src.functions.books.get_book_by_id_handler.get_book_by_id")
    def test_book_not_found(self, mock_get_book_by_id, mock_repo):
        """
        Test that the handler returns a 404 status code when the book is not found.
        """
        mock_get_book_by_id.return_value = None
        event: events.APIGatewayProxyEventV2 = {"pathParameters": {"bookId": "1"}}
        context = {}
        response: responses.APIGatewayProxyResponseV2 = handler(
            event=event, context=context
        )
        self.assertEqual(response.get("statusCode"), 404)
        self.assertEqual(
            json.loads(response.get("body") or "{}"),
            {"message": "Book with id: 1 not found"},
        )

    @patch("src.functions.books.get_book_by_id_handler.BooksMySQLRepository")
    @patch("src.functions.books.get_book_by_id_handler.get_book_by_id")
    def test_successfull_book_retrieval(self, mock_get_book_by_id, mock_repo):
        """
        Test that the handler returns a 200 status code when the book is retrieved successfully.
        """
        mock_get_book_by_id.return_value = Book(
            id=1, title="Test Book", isbn="1234567890"
        )
        event: events.APIGatewayProxyEventV2 = {"pathParameters": {"bookId": "1"}}
        context = {}
        response: responses.APIGatewayProxyResponseV2 = handler(
            event=event, context=context
        )
        self.assertEqual(response.get("statusCode"), 200)
        self.assertEqual(
            json.loads(response.get("body") or "{}"),
            {"id": 1, "title": "Test Book", "isbn": "1234567890"},
        )


if __name__ == "__main__":
    unittest.main()
