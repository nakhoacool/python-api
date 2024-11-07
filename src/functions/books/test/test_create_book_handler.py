import json
import unittest
from unittest.mock import patch

from aws_lambda_typing import events, responses

from ..create_book_handler import handler


class TestCreateBookHandler(unittest.TestCase):
    """
    Test cases for the create_book_handler function.
    """

    def test_no_body_in_event(self):
        """
        Test that the handler returns a 400 status code when the event has no body.
        """
        event: events.APIGatewayProxyEventV2 = {}
        context = {}
        response: responses.APIGatewayProxyResponseV2 = handler(event, context)
        self.assertEqual(response.get("statusCode"), 400)
        self.assertEqual(
            json.loads(response.get("body") or "{}")["message"], "body is required"
        )

    def test_no_title_or_isbn_in_body(self):
        """
        Test that the handler returns a 400 status code when the event body has no title or isbn.
        """
        event: events.APIGatewayProxyEventV2 = {"body": json.dumps({})}
        context = {}
        response: responses.APIGatewayProxyResponseV2 = handler(
            event=event, context=context
        )
        self.assertEqual(response.get("statusCode"), 400)
        self.assertEqual(
            json.loads(response.get("body") or "{}")["message"],
            "title and isbn are required",
        )

    @patch("src.functions.books.create_book_handler.BooksMySQLRepository")
    @patch("src.functions.books.create_book_handler.create_book")
    def test_successfull_book_creation(self, mock_create_book, mock_repo):
        """
        Test that the handler returns a 201 status code when the book is created successfully.
        """
        mock_create_book.return_value = 1
        event: events.APIGatewayProxyEventV2 = {
            "body": json.dumps({"title": "Test Book", "isbn": "1234567890"})
        }
        context = {}
        response: responses.APIGatewayProxyResponseV2 = handler(
            event=event, context=context
        )
        self.assertEqual(response.get("statusCode"), 201)
        self.assertEqual(
            json.loads(response.get("body") or "{}")["message"], "Book created"
        )

    @patch("src.functions.books.create_book_handler.BooksMySQLRepository")
    @patch("src.functions.books.create_book_handler.create_book")
    def test_exception_during_book_creation(self, mock_create_book, mock_repo):
        """
        Test that the handler returns a 500 status code when an exception occurs during book creation.
        """
        mock_create_book.side_effect = Exception("Database error")
        event: events.APIGatewayProxyEventV2 = {
            "body": json.dumps({"title": "Test Book", "isbn": "1234567890"})
        }
        context = {}
        response: responses.APIGatewayProxyResponseV2 = handler(
            event=event, context=context
        )
        self.assertEqual(response.get("statusCode"), 500)
        self.assertEqual(
            json.loads(response.get("body") or "{}")["message"], "Database error"
        )


if __name__ == "__main__":
    unittest.main()
