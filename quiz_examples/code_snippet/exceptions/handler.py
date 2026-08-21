import logging

import litestar


def handle_all_errors(_log, message, trace):
    requester = message["client"]
    route = message["path"]
    logging.error(
        {
            "message": "Api method error",
            "requester_ip": str(requester),
            "level": "ERROR",
            "route": route,
            "exc_info": trace,
        }
    )


def handle_timeout(request: litestar.Request, exc: TimeoutError):
    raise RuntimeError("Request timed out")

EXCEPTION_HANDLERS = {
    TimeoutError: handle_timeout
}