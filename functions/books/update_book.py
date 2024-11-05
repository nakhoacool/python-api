import json

from aws_lambda_typing import events, responses

from database.update import update_book


def handler(
    event: events.APIGatewayProxyEventV2, context
) -> responses.APIGatewayProxyResponseV2:
    try:
        http_method = event["requestContext"]["http"]["method"]

        if "bookId" not in event["pathParameters"]:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "id is required in path parameter"}),
            }

        bookId = event["pathParameters"]["bookId"]

        body = json.loads(event["body"])

        if http_method == "PUT":
            if "title" not in body or "isbn" not in body:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"message": "title and isbn are required"}),
                }
            title = body["title"]
            isbn = body["isbn"]
            input = {"title": title, "isbn": isbn}

            update_book(bookId, input)

        elif http_method == "PATCH":
            # check if only title or isbn is provided and only update that field
            if "title" in body:
                update_book(bookId, {"title": body["title"]})
            elif "isbn" in body:
                update_book(bookId, {"isbn": body["isbn"]})
            else:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"message": "title or isbn is required"}),
                }

        return {"statusCode": 200, "body": json.dumps({"message": "Book updated"})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}
