import json
from aws_lambda_typing import events, responses
from database.query import query_with_fetchmany

def handler(event: events.APIGatewayProxyEventV2, context) -> responses.APIGatewayProxyResponseV2:
    if 'queryStringParameters' not in event:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'page_num and page_size are required'})
        }
    
    if 'page_num' not in event['queryStringParameters'] or 'page_size' not in event['queryStringParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'page_num and page_size are required'})
        }
    
    if not event['queryStringParameters']['page_num'].isdigit() or not event['queryStringParameters']['page_size'].isdigit():
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'page_num and page_size must be integers'})
        }

    page_num = int(event['queryStringParameters']['page_num'])
    page_size = int(event['queryStringParameters']['page_size'])

    try:
        data = query_with_fetchmany(page_num, page_size)

        body = {
            'data': data
        }

        return {
            'statusCode': 200,
            'body': json.dumps(body)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }