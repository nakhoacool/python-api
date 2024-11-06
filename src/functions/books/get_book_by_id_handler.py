import json

from aws_lambda_typing import events, responses

from src.domain.models.book import Book

from ...infrastructure.data_access.mysql.books.books_mysql_repo import (
    BooksMySQLRepository,
)
from ...use_cases.books.get_book_by_id import get_book_by_id


def handler(
    event: events.APIGatewayProxyEventV2, context
) -> responses.APIGatewayProxyResponseV2:
    if "pathParameters" not in event:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "path parameters is required"}),
        }

    if "bookId" not in event["pathParameters"]:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "id is required in path parameter"}),
        }
    bookId: str = event["pathParameters"]["bookId"]

    try:
        repo = BooksMySQLRepository()
        data: Book | None = get_book_by_id(repo, book_id=bookId)
        if data:
            return {"statusCode": 200, "body": json.dumps(data.to_dict())}
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": f"Book with id: {bookId} not found"}),
            }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}
