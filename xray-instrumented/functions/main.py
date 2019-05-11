"""
Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import decimal
import json
import os
import random
import boto3


from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all


patch_all()


TABLE_NAME = os.environ["TABLE_NAME"]


table = boto3.resource("dynamodb").Table(TABLE_NAME)


def dec_encode(o):
    """
    Decimal encoder for JSON

    This converts Decimal into floats, as DynamoDB returns Decimal numbers.
    """
    if isinstance(o, decimal.Decimal):
        return float(o)
    raise TypeError(repr(o) + " is not JSON serializable")


def error(status, message):
    """
    Return an error message
    """

    return {
        "statusCode": status,
        "body": json.dumps({"message": message})
    }


@xray_recorder.capture("get_item")
def get_item(id):
    """
    Returns item from the table
    """

    # Fake error
    if random.randrange(5) == 0:
        raise Exception("Fake error")

    item = table.get_item(Key={"id": id})
    if "Item" not in item:
        raise ValueError("Item not found")
    return item["Item"]["content"]


@xray_recorder.capture("put_item")
def put_item(id, item):
    """
    Add a new item to the table
    """

    table.put_item(Item={
        "id": id,
        "content": item
    })


@xray_recorder.capture("get")
def get_handler(event, _):
    """
    Handler for GetItem
    """

    try:
        name = event["pathParameters"]["name"]
    except KeyError:
        return error(400, "missing 'name' parameter")

    if not name:
        return error(400, "missing 'name' parameter")

    # When using sam local, current_subsegment() returns None
    subsegment = xray_recorder.current_subsegment()
    if subsegment:
        subsegment.put_annotation("name", name)

    try:
        item = get_item(name)
        return {
            "statusCode": 200,
            "body": json.dumps(item, default=dec_encode)
        }
    except ValueError as exc:
        return error(404, str(exc))
    except Exception as exc:
        return error(500, str(exc))


@xray_recorder.capture("put")
def put_handler(event, _):
    """
    Handler for PutItem
    """

    try:
        name = event["pathParameters"]["name"]
    except KeyError:
        return error(400, "missing 'name' parameter")

    if not name:
        return error(400, "missing 'name' parameter")

    # When using sam local, current_subsegment() returns None
    subsegment = xray_recorder.current_subsegment()
    if subsegment:
        subsegment.put_annotation("name", name)

    item = json.loads(event["body"])

    try:
        put_item(name, item)
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Success"})
        }
    except Exception as exc:
        return error(500, str(exc))
