"""
RISK // INDIA — Request Correlation & Structured Safe Logging Middleware
========================================================================
Implements:
1. X-Request-ID correlation tracking:
   - Sanitizes and validates incoming client X-Request-ID headers (alphanumeric, hyphens, max 64 chars).
   - Generates cryptographically random UUIDv4 if missing or invalid.
   - Attaches `request.state.request_id` and adds `X-Request-ID` to all HTTP responses.
2. Structured JSON Access Logging:
   - Records timestamp, log level, correlation ID, method, path, HTTP status, and latency (ms).
   - Zero Credential Leakage: explicitly suppresses authorization headers, cookie values,
     API tokens, passwords, and sensitive PII from log output.
"""

import time
import uuid
import re
import json
import logging
from datetime import datetime, timezone
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.services.metrics_service import metrics_collector

# Strict correlation ID regex: alphanumeric, hyphen, underscore, 1-64 chars
VALID_REQUEST_ID_REGEX = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")

# Dedicated structured logger
logger = logging.getLogger("risk-india.access")


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    Ensures every request has a validated correlation ID (X-Request-ID).
    """
    async def dispatch(self, request: Request, call_next) -> Response:
        incoming_id = request.headers.get("x-request-id")

        if incoming_id and VALID_REQUEST_ID_REGEX.match(incoming_id):
            request_id = incoming_id
        else:
            request_id = str(uuid.uuid4())

        request.state.request_id = request_id

        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    """
    Emits structured JSON access logs with request correlation and latency tracking.
    Guarantees no credentials, authorization tokens, or sensitive cookies are logged.
    """
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.perf_counter()
        request_id = getattr(request.state, "request_id", None) or request.headers.get("x-request-id") or "untracked"

        try:
            response: Response = await call_next(request)
            status_code = response.status_code
        except Exception as exc:
            status_code = 500
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            log_record = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": "ERROR",
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": 500,
                "latency_ms": latency_ms,
                "error_type": exc.__class__.__name__
            }
            logger.error(json.dumps(log_record))
            metrics_collector.record_request(request.method, request.url.path, 500, latency_ms)
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal Server Error",
                    "detail": "An unexpected error occurred in the risk intelligence service.",
                    "request_id": request_id
                },
                headers={"X-Request-ID": request_id}
            )

        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

        log_level = logging.INFO
        if status_code >= 500:
            log_level = logging.ERROR
        elif status_code >= 400:
            log_level = logging.WARNING

        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": logging.getLevelName(log_level),
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": status_code,
            "latency_ms": latency_ms
        }

        # Safe structured logging (no auth, cookies, or body tokens)
        logger.log(log_level, json.dumps(log_record))
        metrics_collector.record_request(request.method, request.url.path, status_code, latency_ms)
        return response
