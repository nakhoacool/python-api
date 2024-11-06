import json

from aws_lambda_typing import events, responses

from ...infrastructure.data_access.mysql.books.books_mysql_repo import (
    BooksMySQLRepository,
)
from ...use_cases.books.update_book import update_book


def handler(
    event: events.APIGatewayProxyEventV2, context
) -> responses.APIGatewayProxyResponseV2:
    try:
        http_method = event.get("requestContext", {}).get("http", {}).get("method", "")

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

        bookId = event["pathParameters"]["bookId"]

        if "body" not in event:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "body is required"}),
            }
        body = json.loads(event["body"])

        repo = BooksMySQLRepository()
        res = 0

        if http_method == "PUT":
            if "title" not in body or "isbn" not in body:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"message": "title and isbn are required"}),
                }
            title = body["title"]
            isbn = body["isbn"]
            input = {"title": title, "isbn": isbn}
            res = update_book(repo=repo, book_id=bookId, fields=input)

        elif http_method == "PATCH":
            # check if only title or isbn is provided and only update that field
            if "title" in body:
                res = update_book(
                    repo=repo, book_id=bookId, fields={"title": body["title"]}
                )
            elif "isbn" in body:
                res = update_book(
                    repo=repo, book_id=bookId, fields={"isbn": body["isbn"]}
                )
            else:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"message": "title or isbn is required"}),
                }
        if res:
            return {"statusCode": 200, "body": json.dumps({"message": "Book updated"})}
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": f"Book with id {bookId} not found"}),
            }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}
