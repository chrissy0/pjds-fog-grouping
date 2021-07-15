from member_utility import call_fn


def handle(req):
    # TODO change what this function does
    payload = json.loads(req)
    data = payload["data"]
    return json.dumps({
        "status-code": 200,
        "message": f"Hello world! I have received this data: {data}."
    })
