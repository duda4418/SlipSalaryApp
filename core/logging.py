"""Application logging utilities and request logging middleware.

Provides:
1. configure_logging() – sets root logging level & format based on settings.LOG_LEVEL
2. RequestLoggingMiddleware – logs each HTTP request with method, path, status, duration, client IP, and a request ID.

Adds an 'X-Request-ID' header to responses for correlation.
"""

from __future__ import annotations

import logging, time, uuid
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from core.settings import settings

_LOGGER_NAME = "slipsalaryapp"

def configure_logging() -> None:
	"""Configure application-wide logging.

	Format includes timestamp, level, logger, message. Level derives from LOG_LEVEL or defaults to INFO.
	Safe to call multiple times (subsequent calls won't duplicate handlers).
	"""
	level_name = (settings.LOG_LEVEL or "INFO").upper()
	level = getattr(logging, level_name, logging.INFO)
	logger = logging.getLogger()
	if not logger.handlers:
		logging.basicConfig(
			level=level,
			format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
		)
	else:
		logger.setLevel(level)
	# Reduce noise from uvicorn/access if desired (keep info)
	logging.getLogger("uvicorn.access").setLevel(logging.INFO)
	logging.getLogger("uvicorn.error").setLevel(logging.INFO)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
	"""Log each incoming HTTP request and response.

	Data points:
	- method path status duration_ms client_ip request_id
	- For errors, duration still recorded (status >=400)
	"""

	def __init__(self, app, logger: logging.Logger | None = None):
		super().__init__(app)
		self.logger = logger or logging.getLogger(_LOGGER_NAME)

	async def dispatch(self, request: Request, call_next: Callable) -> Response:  # type: ignore[override]
		req_id = str(uuid.uuid4())
		start = time.time()
		try:
			response = await call_next(request)
		except Exception as exc:  # Log unhandled exceptions
			duration_ms = (time.time() - start) * 1000
			self.logger.exception(
				f"EXCEPTION method={request.method} path={request.url.path} duration_ms={duration_ms:.1f} req_id={req_id} "
			)
			raise
		duration_ms = (time.time() - start) * 1000
		self.logger.info(
			f"{request.method} {request.url.path} status={response.status_code} duration_ms={duration_ms:.1f} req_id={req_id} "
		)
		# Correlate response
		response.headers["X-Request-ID"] = req_id
		return response

__all__ = ["configure_logging", "RequestLoggingMiddleware"]
