import json

from aws_lambda_typing import events, responses

from ...infrastructure.data_access.mysql.books.books_mysql_repo import (
    BooksMySQLRepository,
)
from ...use_cases.books.create_book import create_book


def handler(
    event: events.APIGatewayProxyEventV2, context
) -> responses.APIGatewayProxyResponseV2:
    if "body" not in event:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "body is required"}),
        }
    
    body = json.loads(event["body"])
    if "title" not in body or "isbn" not in body:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "title and isbn are required"}),
        }
    
    title = body["title"]
    isbn = body["isbn"]

    try:
        repo = BooksMySQLRepository()
        book_id = create_book(repo=repo, title=title, isbn=isbn)
        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Book created", "book_id": book_id}),
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}
