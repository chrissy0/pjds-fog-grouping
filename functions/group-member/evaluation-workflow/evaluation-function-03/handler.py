from member_utility import call_fn


def handle(req):
    # passes data to next function
    # TODO do something with data and pass to other function
    call_fn("evaluation-function-04", req)
    return call_fn("evaluation-function-08", req)
