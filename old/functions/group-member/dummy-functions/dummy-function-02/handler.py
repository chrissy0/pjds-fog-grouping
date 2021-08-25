import requests
import json
import os
import sys


def handle(req):
    payload = json.loads(req)
    data = payload["data"]
    return json.dumps({
        "status-code": 200,
        "message": f"Hello world! I have received this data: {data}."
    })
