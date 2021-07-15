from member_utility import call_fn


def handle(req):
    # passes data to next function
    return call_fn("evaluation-function-3", req)
