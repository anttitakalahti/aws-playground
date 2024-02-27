import random


def handler(event, context):
    if random.random() > 0.75:
        raise Exception("Internal error")

    json_data = {"payload": f"{event.get('payload', '').upper()}"}

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "content-type": "application/json"
        },
        "body": json_data
    }
