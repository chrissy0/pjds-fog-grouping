from eval_util import call_and_log


def handle(req):
    return call_and_log("evaluation-function-04", ["evaluation-function-05"], False, req)