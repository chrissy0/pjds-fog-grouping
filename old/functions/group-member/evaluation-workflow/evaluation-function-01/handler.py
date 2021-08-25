from eval_util import call_and_log


def handle(req):
    return call_and_log("evaluation-function-01", ["evaluation-function-02", "evaluation-function-11"], True, req)
