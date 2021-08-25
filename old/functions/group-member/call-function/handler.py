from member_utility import call_fn
import json


def handle(req):
    payload = json.loads(req)

    function_name = payload["function"]
    request_data = json.dumps(payload["request"])
    return call_fn(function_name, request_data)
