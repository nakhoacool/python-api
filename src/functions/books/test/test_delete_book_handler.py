import json
import unittest
from unittest.mock import patch

from aws_lambda_typing import events, responses

from ..delete_book_handler import handler


class TestDeleteBookHandler(unittest.TestCase):
    """
    Test cases for the delete_book_handler function.
    """

    def test_no_path_parameter(self):
        """
        Test that the handler returns a 400 status code when the event has no path parameters.
        """
        event: events.APIGatewayProxyEventV2 = {}
        context = {}
        response: responses.APIGatewayProxyResponseV2 = handler(
            event=event, context=context
        )
        self.assertEqual(response.get("statusCode"), 400)
        self.assertEqual(
            json.loads(response.get("body") or "{}")["message"],
            "path parameters is required",
        )
    
    def test_no_id_in_path_parameter(self):
        """
        Test that the handler returns a 400 status code when the event path parameters has no id.
        """
        event: events.APIGatewayProxyEventV2 = {"pathParameters": {}}
        context = {}
        response: responses.APIGatewayProxyResponseV2 = handler(
            event=event, context=context
        )
        self.assertEqual(response.get("statusCode"), 400)
        self.assertEqual(
            json.loads(response.get("body") or "{}")["message"],
            "id is required in path parameters",
        )

    @patch("src.functions.books.delete_book_handler.BooksMySQLRepository")
    @patch("src.functions.books.delete_book_handler.delete_book")
    def test_book_not_found(self, mock_delete_book, mock_repo):
        """
        Test that the handler returns a 404 status code when the book is not found.
        """
        mock_delete_book.return_value = False
        event: events.APIGatewayProxyEventV2 = {
            "pathParameters": {"bookId": "1"}
        }
        context = {}
        response: responses.APIGatewayProxyResponseV2 = handler(
            event=event, context=context
        )
        self.assertEqual(response.get("statusCode"), 404)
        self.assertEqual(
            json.loads(response.get("body") or "{}")["message"], "Book not found"
        )
    
    @patch("src.functions.books.delete_book_handler.BooksMySQLRepository")
    @patch("src.functions.books.delete_book_handler.delete_book")
    def test_exception_raised(self, mock_delete_book, mock_repo):
        """
        Test that the handler returns a 500 status code when an exception is raised.
        """
        mock_delete_book.side_effect = Exception("An error occurred")
        event: events.APIGatewayProxyEventV2 = {
            "pathParameters": {"bookId": "1"}
        }
        context = {}
        response: responses.APIGatewayProxyResponseV2 = handler(
            event=event, context=context
        )
        self.assertEqual(response.get("statusCode"), 500)
        self.assertEqual(
            json.loads(response.get("body") or "{}")["message"], "An error occurred"
        )

    @patch("src.functions.books.delete_book_handler.BooksMySQLRepository")
    @patch("src.functions.books.delete_book_handler.delete_book")
    def test_successfull_book_deletion(self, mock_delete_book, mock_repo):
        """
        Test that the handler returns a 200 status code when the book is deleted successfully.
        """
        mock_delete_book.return_value = True
        event: events.APIGatewayProxyEventV2 = {
            "pathParameters": {"bookId": "1"}
        }
        context = {}
        response: responses.APIGatewayProxyResponseV2 = handler(
            event=event, context=context
        )
        self.assertEqual(response.get("statusCode"), 200)
        self.assertEqual(
            json.loads(response.get("body") or "{}")["message"], "Book deleted"
        )


if __name__ == "__main__":
    unittest.main()
