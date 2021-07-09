import requests
import json
from member_utility import get_external_ip

port = "5000"

"""
Request body example:
{
    "requester" : <node-address that is requesting the alternative>
    "function" : <the function that needs to be looked up for alternatives>
    "address" : <address of the failed node>
}
"""


def handle(req):
    body = json.loads(req)
    requester = body["requester"]
    function = body["function"]
    address = body["address"]

    ip = get_external_ip()

    res = requests.get(f"http://{ip}:{port}/get-alternatives")
    addresses = res.text.split(",")
    alternative = ''

    # For now, simple approach: Take the first alternative address in the list
    # Later on, pick a node with minimal memory/cpu usage
    for alt in addresses:
        if alt != address:
            res = requests.post(f"http://{requester}:{port}/set-address", data=f"{function},{alt}")
            if res.status_code == 200:
                alternative = alt
                break

    return alternative
