#!/usr/bin/python3

import logging
import random
from aws_lambda_powertools.utilities.typing import LambdaContext


logger = logging.getLogger()
logger.setLevel("INFO")


def handler(event: dict, context: LambdaContext) -> dict:
    json_data = [{"payload": f"{event.get('payload', '').upper()}"}]

    if random.random() > 0.5:
        return {
            "statusCode": "500",
            "body": "Internal server error",
            "headers": {
                "Content-Type": "application/json",
            }
        }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "content-type": "application/json"
        },
        "body": json_data
    }
