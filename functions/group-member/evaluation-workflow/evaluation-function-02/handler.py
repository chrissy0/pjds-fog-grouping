from eval_util import call_and_log


def handle(req):
    return call_and_log("evaluation-function-02", ["evaluation-function-03"], False, req)