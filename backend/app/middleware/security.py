"""
RISK // INDIA — Security Headers Middleware
============================================
Injects defense-in-depth security headers into all HTTP responses:
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY (clickjacking protection)
- Referrer-Policy: strict-origin-when-cross-origin
- Permissions-Policy: camera=(), microphone=(), geolocation=(self)
- Content-Security-Policy (application-specific for React/Vite, OSM tiles, USGS endpoints)
- Strict-Transport-Security (conditional on HTTPS or production environment)
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.config import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware applying production-grade HTTP security headers.
    """

    CSP_POLICY = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com data:; "
        "img-src 'self' data: blob: https://*.tile.openstreetmap.org https://tile.openstreetmap.org; "
        "connect-src 'self' https://earthquake.usgs.gov; "
        "frame-ancestors 'none'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    )

    def __init__(self, app, enable_hsts: bool = False):
        super().__init__(app)
        self.enable_hsts = enable_hsts

    async def dispatch(self, request: Request, call_next) -> Response:
        response: Response = await call_next(request)

        # Baseline Security Headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=(self)"
        response.headers["Content-Security-Policy"] = self.CSP_POLICY

        # Conditional HSTS (avoid breaking local development over HTTP)
        is_production = getattr(settings, "APP_ENV", "development").lower() == "production"
        is_https = request.url.scheme == "https" or request.headers.get("x-forwarded-proto") == "https"
        hsts_configured = self.enable_hsts or getattr(settings, "ENABLE_HSTS", False)

        if hsts_configured or is_production or is_https:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response
