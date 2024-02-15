#!/usr/bin/python3

import logging
from aws_lambda_powertools.utilities.typing import LambdaContext


logger = logging.getLogger()
logger.setLevel("INFO")


def handler(event: dict, context: LambdaContext) -> dict:
    json_data = [{"payload": f"{event.get('payload', '').upper()}"}]

    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": 'GET, POST, PUT, DELETE, OPTIONS',
            "content-type": "application/json"
        },
        'body': json_data
    }
