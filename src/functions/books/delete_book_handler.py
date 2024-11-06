import json

from aws_lambda_typing import events, responses

from ...infrastructure.data_access.mysql.books.books_mysql_repo import (
    BooksMySQLRepository,
)
from ...use_cases.books.delete_book import delete_book


def handler(
    event: events.APIGatewayProxyEventV2, context
) -> responses.APIGatewayProxyResponseV2:
    try:
        if "pathParameters" not in event:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "path parameters is required"}),
            }
        
        if "bookId" not in event["pathParameters"]:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "id is required in path parameters"}),
            }
        
        bookId = event["pathParameters"]["bookId"]
        repo = BooksMySQLRepository()
        res = delete_book(repo=repo, book_id=bookId)
        if res:
            return {"statusCode": 200, "body": json.dumps({"message": "Book deleted"})}
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Book not found"}),
            }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}
