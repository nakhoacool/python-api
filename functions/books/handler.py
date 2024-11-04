import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + "/database")
from database.query import query_with_fetchmany
def list_books(event, context):
    data = query_with_fetchmany()

    body = {
        'data': data
    }

    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }