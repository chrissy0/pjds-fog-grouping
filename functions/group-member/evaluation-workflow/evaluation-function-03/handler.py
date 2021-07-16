from eval_util import call_and_log


def handle(req):
    return call_and_log("evaluation-function-03", ["evaluation-function-04"], False, req)