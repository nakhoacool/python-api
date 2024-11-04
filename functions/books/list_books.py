import json
import os
import sys
from aws_lambda_typing import events

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + "/database")
from database.query import query_with_fetchmany

def handler(event: events.APIGatewayProxyEventV2, context):
    page_num = int(event['queryStringParameters']['page_num'])
    page_size = int(event['queryStringParameters']['page_size'])

    data = query_with_fetchmany(page_num, page_size)

    body = {
        'data': data
    }

    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }