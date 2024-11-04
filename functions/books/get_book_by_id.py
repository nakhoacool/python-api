import json
from aws_lambda_typing import events, responses
from database.query import query_with_fetchone

def handler(event: events.APIGatewayProxyEventV2, context) -> responses.APIGatewayProxyResponseV2:
    if 'bookId' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "message": "id is required in path parameter"
            })
        }
    bookId = event['pathParameters']['bookId']

    try:
        data = query_with_fetchone(bookId)
        return {
            'statusCode': 200,
            'body': json.dumps(data)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": str(e)
            })
        }
