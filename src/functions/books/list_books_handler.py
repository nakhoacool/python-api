import json

from aws_lambda_typing import events, responses

from ...infrastructure.data_access.mysql.books.books_mysql_repo import (
    BooksMySQLRepository,
)
from ...use_cases.books.list_book import list_book


def handler(
    event: events.APIGatewayProxyEventV2, context
) -> responses.APIGatewayProxyResponseV2:
    try:
        if "queryStringParameters" not in event:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "page_num and page_size are required"}),
            }

        if (
            "page_num" not in event["queryStringParameters"]
            or "page_size" not in event["queryStringParameters"]
        ):
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "page_num and page_size are required"}),
            }

        if (
            not event["queryStringParameters"]["page_num"].isdigit()
            or not event["queryStringParameters"]["page_size"].isdigit()
        ):
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {"message": "page_num and page_size must be integers"}
                ),
            }

        page_num = int(event["queryStringParameters"]["page_num"])
        page_size = int(event["queryStringParameters"]["page_size"])

        repo = BooksMySQLRepository()
        books = list_book(repo=repo, page_num=page_num, page_size=page_size)
        data = [book.to_dict() for book in books]
        body = {"data": data}

        return {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}
