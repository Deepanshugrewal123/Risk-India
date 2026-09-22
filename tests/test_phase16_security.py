"""
RISK // INDIA — Automated Test Suite: Phase 16 Production Security Hardening
=============================================================================
Covers 17 security test requirements:
1.  test_security_headers_present (nosniff, DENY, strict-origin, Permissions-Policy)
2.  test_csp_header_present_and_valid (script, style, font, img, connect, frame-ancestors)
3.  test_cors_rejection_for_unlisted_origin (unlisted origin gets no CORS allow)
4.  test_cors_acceptance_for_allowed_origin (allowed origin gets allow-origin & credentials)
5.  test_cors_no_wildcard_with_credentials (wildcard * never present with allow_credentials)
6.  test_rate_limiting_compute_route (11th request to /api/risk/analyze returns 429)
7.  test_rate_limiting_retry_after_header (429 has Retry-After header & retry_after payload)
8.  test_request_id_generated_when_absent (valid UUIDv4 generated)
9.  test_request_id_preserved_when_valid (valid alphanumeric/hyphen ID preserved)
10. test_request_id_sanitized_when_malformed (malformed/XSS-like ID replaced with UUID)
11. test_coordinate_validation_bounds (lat < 6 or > 38, lon < 68 or > 98 returns 422)
12. test_rainfall_validation_bounds (rainfall < 0 or > 2000 mm returns 422)
13. test_ssrf_protection_maintained (disaster provider endpoints are immutable)
14. test_500_error_sanitization (500 response contains no stack traces, paths, or secrets)
15. test_logging_no_credential_leak (authorization headers and secrets omitted from logs)
16. test_phase15_circuit_breaker_reliability_preserved (CircuitBreaker remains operational)
17. test_ml_prototype_integrity (Assam spatial guard and inference pipeline intact)
"""

import sys
from pathlib import Path
import unittest
import uuid
import io
import logging
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.middleware.rate_limit import rate_limiter
from app.services.disaster_provider import USGSSeismicProvider
from app.services.flood_model_service import flood_model_service


class TestPhase16Security(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        rate_limiter.reset()

    def tearDown(self):
        rate_limiter.reset()

    # -------------------------------------------------------------------------
    # 1. Security Headers Tests
    # -------------------------------------------------------------------------
    def test_security_headers_present(self):
        """Verify baseline defense-in-depth headers on API responses."""
        resp = self.client.get("/api/health")
        self.assertEqual(resp.status_code, 200)

        # nosniff
        self.assertEqual(resp.headers.get("x-content-type-options"), "nosniff")
        # Clickjacking defense
        self.assertEqual(resp.headers.get("x-frame-options"), "DENY")
        # Referrer privacy
        self.assertEqual(resp.headers.get("referrer-policy"), "strict-origin-when-cross-origin")
        # Device permissions
        perm_policy = resp.headers.get("permissions-policy")
        self.assertIsNotNone(perm_policy)
        self.assertIn("camera=()", perm_policy)
        self.assertIn("microphone=()", perm_policy)

    # -------------------------------------------------------------------------
    # 2. Content Security Policy (CSP)
    # -------------------------------------------------------------------------
    def test_csp_header_present_and_valid(self):
        """Verify Content-Security-Policy restricts origins and protects against XSS/framing."""
        resp = self.client.get("/api/health")
        csp = resp.headers.get("content-security-policy")
        self.assertIsNotNone(csp)

        self.assertIn("default-src 'self'", csp)
        self.assertIn("script-src", csp)
        self.assertIn("style-src", csp)
        self.assertIn("fonts.googleapis.com", csp)
        self.assertIn("fonts.gstatic.com", csp)
        self.assertIn("tile.openstreetmap.org", csp)
        self.assertIn("earthquake.usgs.gov", csp)
        self.assertIn("frame-ancestors 'none'", csp)

    # -------------------------------------------------------------------------
    # 3. CORS: Rejection of Unlisted Origin
    # -------------------------------------------------------------------------
    def test_cors_rejection_for_unlisted_origin(self):
        """Unlisted origin should not receive CORS approval."""
        untrusted = "https://malicious-phishing-site.example.com"
        resp = self.client.get(
            "/api/health",
            headers={"Origin": untrusted}
        )
        self.assertEqual(resp.status_code, 200)
        allowed_origin = resp.headers.get("access-control-allow-origin")
        self.assertNotEqual(allowed_origin, untrusted)
        self.assertNotEqual(allowed_origin, "*")

    # -------------------------------------------------------------------------
    # 4. CORS: Acceptance for Allowed Origin
    # -------------------------------------------------------------------------
    def test_cors_acceptance_for_allowed_origin(self):
        """Allowed frontend origin receives Access-Control-Allow-Origin & Credentials."""
        allowed = "http://localhost:5173"
        resp = self.client.get(
            "/api/health",
            headers={"Origin": allowed}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("access-control-allow-origin"), allowed)
        self.assertEqual(resp.headers.get("access-control-allow-credentials"), "true")

    # -------------------------------------------------------------------------
    # 5. CORS: No Wildcard '*' with Credentials
    # -------------------------------------------------------------------------
    def test_cors_no_wildcard_with_credentials(self):
        """Verify that wildcard '*' is strictly removed from cors_origin_list."""
        origins = settings.cors_origin_list
        self.assertNotIn("*", origins, "Wildcard '*' must never be combined with allow_credentials=True")
        for orig in origins:
            self.assertTrue(orig.startswith("http://") or orig.startswith("https://"))

    # -------------------------------------------------------------------------
    # 6. Rate Limiting: Compute Route Abuse Trigger
    # -------------------------------------------------------------------------
    def test_rate_limiting_compute_route(self):
        """Exceeding 10 requests to /api/risk/analyze triggers HTTP 429."""
        rate_limiter.reset()
        payload = {
            "location_id": "kamrup_rural",
            "district": "Kamrup Rural",
            "disaster_type": "flood",
            "features": {"rainfall_24h": 120.0, "river_level_relative": 2.5}
        }

        # Make 10 permitted requests
        for i in range(10):
            res = self.client.post("/api/risk/analyze", json=payload)
            self.assertEqual(res.status_code, 200, f"Request {i+1} should succeed within limit")

        # 11th request must be rejected with 429
        rejected = self.client.post("/api/risk/analyze", json=payload)
        self.assertEqual(rejected.status_code, 429)
        body = rejected.json()
        self.assertEqual(body.get("error"), "Too Many Requests")
        self.assertIn("Rate limit exceeded", body.get("detail", ""))

    # -------------------------------------------------------------------------
    # 7. Rate Limiting: Retry-After Header
    # -------------------------------------------------------------------------
    def test_rate_limiting_retry_after_header(self):
        """HTTP 429 response contains a positive integer Retry-After header."""
        rate_limiter.reset()
        payload = {
            "location_id": "kamrup_rural",
            "district": "Kamrup Rural",
            "disaster_type": "flood"
        }
        for _ in range(10):
            self.client.post("/api/risk/analyze", json=payload)

        rejected = self.client.post("/api/risk/analyze", json=payload)
        self.assertEqual(rejected.status_code, 429)

        retry_after = rejected.headers.get("retry-after")
        self.assertIsNotNone(retry_after)
        self.assertTrue(retry_after.isdigit())
        self.assertGreater(int(retry_after), 0)
        self.assertEqual(rejected.json().get("retry_after"), int(retry_after))

    # -------------------------------------------------------------------------
    # 8. Request ID: Generated when Absent
    # -------------------------------------------------------------------------
    def test_request_id_generated_when_absent(self):
        """Every response must return an X-Request-ID even if client sends none."""
        resp = self.client.get("/api/health")
        req_id = resp.headers.get("x-request-id")
        self.assertIsNotNone(req_id)
        # Should be a valid UUID
        parsed = uuid.UUID(req_id)
        self.assertEqual(str(parsed), req_id)

    # -------------------------------------------------------------------------
    # 9. Request ID: Preserved when Valid
    # -------------------------------------------------------------------------
    def test_request_id_preserved_when_valid(self):
        """Valid client-supplied X-Request-ID is preserved and returned."""
        valid_id = "req-india-2026-audit-001"
        resp = self.client.get("/api/health", headers={"X-Request-ID": valid_id})
        self.assertEqual(resp.headers.get("x-request-id"), valid_id)

    # -------------------------------------------------------------------------
    # 10. Request ID: Sanitized when Malformed
    # -------------------------------------------------------------------------
    def test_request_id_sanitized_when_malformed(self):
        """Malformed or injection-payload X-Request-ID is discarded and replaced with a valid UUID."""
        malformed_id = "<script>alert('xss')</script>"
        resp = self.client.get("/api/health", headers={"X-Request-ID": malformed_id})
        returned_id = resp.headers.get("x-request-id")
        self.assertNotEqual(returned_id, malformed_id)
        self.assertNotIn("<script>", returned_id)
        # Should be replaced by a clean UUID
        parsed = uuid.UUID(returned_id)
        self.assertEqual(str(parsed), returned_id)

    # -------------------------------------------------------------------------
    # 11. Coordinate Validation Bounds
    # -------------------------------------------------------------------------
    def test_coordinate_validation_bounds(self):
        """Coordinates outside Indian bounding limits (6-38 N, 68-98 E) return HTTP 422."""
        # Latitude too high (> 38)
        resp1 = self.client.post("/api/risk/analyze", json={
            "location_id": "kamrup_rural",
            "features": {"latitude": 60.5, "longitude": 91.0}
        })
        self.assertEqual(resp1.status_code, 422)

        # Latitude too low (< 6)
        resp2 = self.client.post("/api/risk/analyze", json={
            "location_id": "kamrup_rural",
            "features": {"latitude": 2.0, "longitude": 91.0}
        })
        self.assertEqual(resp2.status_code, 422)

        # Longitude too high (> 98)
        resp3 = self.client.post("/api/risk/analyze", json={
            "location_id": "kamrup_rural",
            "features": {"latitude": 26.0, "longitude": 115.0}
        })
        self.assertEqual(resp3.status_code, 422)

        # Longitude too low (< 68)
        resp4 = self.client.post("/api/risk/analyze", json={
            "location_id": "kamrup_rural",
            "features": {"latitude": 26.0, "longitude": 50.0}
        })
        self.assertEqual(resp4.status_code, 422)

    # -------------------------------------------------------------------------
    # 12. Rainfall Validation Bounds
    # -------------------------------------------------------------------------
    def test_rainfall_validation_bounds(self):
        """Rainfall values outside physical bounds (0.0 to 2000.0 mm) return HTTP 422."""
        # Unrealistic extreme rainfall (> 2000 mm)
        resp1 = self.client.post("/api/risk/analyze", json={
            "location_id": "kamrup_rural",
            "features": {"rainfall_24h": 5000.0}
        })
        self.assertEqual(resp1.status_code, 422)

        # Negative rainfall (< 0)
        resp2 = self.client.post("/api/risk/analyze", json={
            "location_id": "kamrup_rural",
            "features": {"rainfall_24h": -25.0}
        })
        self.assertEqual(resp2.status_code, 422)

    # -------------------------------------------------------------------------
    # 13. SSRF Protection Maintained
    # -------------------------------------------------------------------------
    def test_ssrf_protection_maintained(self):
        """Verify upstream disaster providers use static, immutable endpoints with no user-controlled URL inputs."""
        provider = USGSSeismicProvider()
        self.assertTrue(provider.ENDPOINT.startswith("https://earthquake.usgs.gov/"))
        self.assertIn("minlatitude=6&maxlatitude=38", provider.ENDPOINT)
        # Verify endpoint cannot be altered by query parameter
        self.assertFalse(hasattr(provider, "user_endpoint"))

    # -------------------------------------------------------------------------
    # 14. 500 Error Sanitization
    # -------------------------------------------------------------------------
    def test_500_error_sanitization(self):
        """Internal 500 errors must return sanitized JSON with request_id and zero stack trace leakage."""
        client = TestClient(app, raise_server_exceptions=False)
        with patch("app.services.risk_service.risk_service.get_location_risk") as mock_service:
            mock_service.side_effect = RuntimeError("Sensitive DB Connection String: postgres://user:secret@10.0.0.1:5432/db")
            resp = client.get("/api/risk/assam")

            self.assertEqual(resp.status_code, 500)
            data = resp.json()
            self.assertEqual(data.get("error"), "Internal Server Error")
            self.assertIn("detail", data)
            # Must NOT leak exception details, credentials, or file paths
            raw_text = resp.text
            self.assertNotIn("postgres://", raw_text)
            self.assertNotIn("secret@", raw_text)
            self.assertNotIn("Traceback", raw_text)
            self.assertNotIn("C:\\Users", raw_text)
            # Must include request_id
            self.assertIsNotNone(data.get("request_id"))
            self.assertIsNotNone(resp.headers.get("x-request-id"))

    # -------------------------------------------------------------------------
    # 15. Logging: Zero Credential / Token Leakage
    # -------------------------------------------------------------------------
    def test_logging_no_credential_leak(self):
        """Structured logs must never record Authorization tokens, cookies, or secrets."""
        log_capture = io.StringIO()
        handler = logging.StreamHandler(log_capture)
        access_logger = logging.getLogger("risk-india.access")
        access_logger.addHandler(handler)

        secret_token = "Bearer secret-super-confidential-token-98765"
        resp = self.client.get(
            "/api/health",
            headers={"Authorization": secret_token, "Cookie": "session=sensitive_cookie_value"}
        )
        self.assertEqual(resp.status_code, 200)

        logs = log_capture.getvalue()
        self.assertNotIn(secret_token, logs)
        self.assertNotIn("sensitive_cookie_value", logs)
        access_logger.removeHandler(handler)

    # -------------------------------------------------------------------------
    # 16. Phase 15 Reliability Features Preserved
    # -------------------------------------------------------------------------
    def test_phase15_circuit_breaker_reliability_preserved(self):
        """Phase 15 CircuitBreaker integration remains functional."""
        provider = USGSSeismicProvider()
        self.assertIsNotNone(provider.circuit_breaker)
        health = provider.get_health()
        self.assertIn("circuit_breaker", health)
        self.assertEqual(health["circuit_breaker"]["state"], "CLOSED")

    # -------------------------------------------------------------------------
    # 17. ML Prototype Integrity Preserved
    # -------------------------------------------------------------------------
    def test_ml_prototype_integrity(self):
        """Assam flood ML prototype (assam_flood_prototype_v1) retains spatial bounds and inference contract."""
        self.assertTrue(flood_model_service.is_ready)
        self.assertEqual(flood_model_service.model_version, "assam_flood_prototype_v1")

        # Valid Assam location inference
        result = flood_model_service.predict(
            location_id="kamrup_rural",
            district="Kamrup Rural",
            features={"rainfall_24h": 95.0, "river_level_relative": 1.2}
        )
        self.assertEqual(result.get("status"), "success")
        self.assertIn("flood_probability", result)
        self.assertIn("risk_score", result)

        # Geographic guard: non-Assam location rejected
        out_of_scope = flood_model_service.predict(
            location_id="mumbai",
            district="Mumbai City",
            features={"rainfall_24h": 120.0}
        )
        self.assertEqual(out_of_scope.get("status"), "model_scope_limited")


if __name__ == "__main__":
    unittest.main()
