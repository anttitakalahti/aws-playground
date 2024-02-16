import random


def lambda_handler(event, context):
    json_data = [{"payload": f"{event.get('payload', '').upper()}"}]

    if random.random() > 0.5:
        raise Exception("moomoo")

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "content-type": "application/json"
        },
        "body": json_data
    }