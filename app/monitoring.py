
import logging
import time

from fastapi import Request

logger = logging.getLogger("owaspshield")


def log_request_metrics(
    method: str,
    path: str,
    status_code: int,
    latency_ms: float,
):
    logger.info(
        "request_metrics method=%s path=%s status=%s latency_ms=%.2f",
        method,
        path,
        status_code,
        latency_ms,
    )


async def request_monitoring_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response

    finally:
        latency_ms = (time.perf_counter() - start_time) * 1000

        log_request_metrics(
            method=request.method,
            path=request.url.path,
            status_code=status_code,
            latency_ms=latency_ms,
        )
