import json

from aws_lambda_typing import events, responses

from database.delete import delete_book


def handler(
    event: events.APIGatewayProxyEventV2, context
) -> responses.APIGatewayProxyResponseV2:
    try:
        if "bookId" not in event["pathParameters"]:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "id is required in path parameters"}),
            }
        bookId = event["pathParameters"]["bookId"]
        delete_book(book_id=bookId)
        return {"statusCode": 200, "body": json.dumps({"message": "Book deleted"})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}
