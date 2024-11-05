import json

from aws_lambda_typing import events, responses

from database.insert import insert_book


def handler(
    event: events.APIGatewayProxyEventV2, context
) -> responses.APIGatewayProxyResponseV2:
    body = json.loads(event["body"])
    if "title" not in body or "isbn" not in body:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "title and isbn are required"}),
        }
    title = body["title"]
    isbn = body["isbn"]

    try:
        book_id = insert_book(title, isbn)
        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Book created", "book_id": book_id}),
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}
