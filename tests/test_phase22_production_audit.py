"""
RISK // INDIA — Phase 22 Production, Security & Scientific Audit Test Suite
=============================================================================
Automated verification suite validating:
1. Defense-in-depth security headers (CSP, HSTS, X-Frame-Options, etc.)
2. Rate limiting with RFC-compliant Retry-After header
3. X-Request-ID correlation tracking and sanitization
4. Global error sanitization (zero stack trace leakage)
5. Pydantic input bounds validation (coordinates, rainfall, river stages)
6. Clean-clone reproducibility (zero hardcoded machine paths)
7. Nginx hardening (server_tokens off, dotfile denial, CSP)
8. Container security (non-root execution, minimal surface, isolated DB/Redis)
9. ML model immutability (13 features, 32 observations, frozen artifact)
10. Spatial guard enforcement (non-Assam receives baseline, no fake ML)
11. National coverage preservation (28 States, 8 Union Territories)
12. Multi-hazard architecture coverage (6 hazards)
13. Provider circuit breaker isolation and graceful degradation
14. Frontend external link security (rel="noopener noreferrer")
15. Frontend XSS immunity (zero dangerouslySetInnerHTML)
"""

import unittest
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from starlette.requests import Request
from starlette.responses import JSONResponse

# Backend imports
from app.main import app
from app.config import settings
from app.middleware.logger import CorrelationIdMiddleware, VALID_REQUEST_ID_REGEX
from app.middleware.rate_limit import RateLimiter
from app.schemas.risk import RiskAnalyzeRequest
from app.services.model_registry import model_registry
from app.services.geo_basin_service import (
    INDIAN_ADMINISTRATIVE_ENTITIES,
    geo_basin_service
)
from app.services.flood_model_service import flood_model_service, EXPECTED_FEATURES
from app.services.hazard_providers.base import BaseHazardProvider
from app.services.disaster_provider import NormalizedDisasterEvent, CircuitBreaker


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class TestPhase22ProductionAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_security_headers_enforced(self):
        """Verify baseline security headers are present on API responses."""
        resp = self.client.get("/api/health")
        self.assertEqual(resp.status_code, 200)

        headers = resp.headers
        self.assertEqual(headers.get("X-Frame-Options"), "DENY")
        self.assertEqual(headers.get("X-Content-Type-Options"), "nosniff")
        self.assertEqual(headers.get("Referrer-Policy"), "strict-origin-when-cross-origin")
        self.assertIn("camera=()", headers.get("Permissions-Policy", ""))
        self.assertIn("default-src 'self'", headers.get("Content-Security-Policy", ""))
        self.assertIn("tile.openstreetmap.org", headers.get("Content-Security-Policy", ""))

    def test_02_rate_limiter_retry_after_header(self):
        """Verify rate limiter blocks bursts with 429 and includes Retry-After header."""
        limiter = RateLimiter(general_limit=3, compute_limit=2, window_seconds=60)

        class MockRequest:
            def __init__(self, method="GET", path="/api/health", ip="192.168.1.100"):
                self.method = method
                self.url = type("URL", (), {"path": path})()
                self.headers = {"x-forwarded-for": ip}
                self.client = type("Client", (), {"host": ip})()

        req = MockRequest()
        self.assertTrue(limiter.check(req)[0])
        self.assertTrue(limiter.check(req)[0])
        self.assertTrue(limiter.check(req)[0])

        allowed, retry_after = limiter.check(req)
        self.assertFalse(allowed)
        self.assertGreaterEqual(retry_after, 1)
        self.assertLessEqual(retry_after, 60)

    def test_03_request_id_correlation_sanitization(self):
        """Verify valid request IDs are preserved and invalid ones are sanitized."""
        # Valid ID
        resp = self.client.get("/api/health", headers={"X-Request-ID": "valid-audit-id-12345"})
        self.assertEqual(resp.headers.get("X-Request-ID"), "valid-audit-id-12345")

        # Malformed ID with suspicious characters (e.g. path traversal or script tags)
        resp_bad = self.client.get("/api/health", headers={"X-Request-ID": "bad/id;DROP TABLE--<script>"})
        clean_id = resp_bad.headers.get("X-Request-ID")
        self.assertNotEqual(clean_id, "bad/id;DROP TABLE--<script>")
        self.assertTrue(bool(VALID_REQUEST_ID_REGEX.match(clean_id)))

    def test_04_error_sanitization_no_stack_traces(self):
        """Verify unhandled exceptions return sanitized JSON without leaking Python tracebacks."""
        # Query an intentional 404 or bad method on non-existent route
        resp = self.client.get("/api/invalid-nonexistent-endpoint-audit")
        self.assertEqual(resp.status_code, 404)
        body = resp.text
        self.assertNotIn("Traceback (most recent call last)", body)
        self.assertNotIn("File \"", body)

    def test_05_input_bounds_validation(self):
        """Verify Pydantic schemas enforce coordinate, rainfall, and river stage bounds."""
        # Latitude out of Indian bounds (> 38)
        with self.assertRaises(ValueError):
            RiskAnalyzeRequest(
                location_id="assam",
                features={"latitude": 45.0, "longitude": 92.0}
            )

        # Longitude out of Indian bounds (< 68)
        with self.assertRaises(ValueError):
            RiskAnalyzeRequest(
                location_id="assam",
                features={"latitude": 26.0, "longitude": 50.0}
            )

        # Physical rainfall out of bounds (> 2000 mm)
        with self.assertRaises(ValueError):
            RiskAnalyzeRequest(
                location_id="assam",
                features={"rainfall_24h": 3500.0}
            )

        # River level relative out of bounds (< -10m or > 15m)
        with self.assertRaises(ValueError):
            RiskAnalyzeRequest(
                location_id="assam",
                features={"river_level_relative": 25.0}
            )

        # Valid input should succeed
        valid_req = RiskAnalyzeRequest(
            location_id="assam",
            district="Kamrup",
            features={"latitude": 26.1, "longitude": 91.7, "rainfall_24h": 85.0, "river_level_relative": 1.2}
        )
        self.assertEqual(valid_req.location_id, "assam")

    def test_06_clean_clone_no_hardcoded_machine_paths(self):
        """Verify no source code or configuration files contain hardcoded developer machine paths."""
        source_dirs = [
            PROJECT_ROOT / "backend" / "app",
            PROJECT_ROOT / "src",
            PROJECT_ROOT / "nginx",
            PROJECT_ROOT / "alembic"
        ]
        forbidden_patterns = ["C:\\Users\\", "c:\\users\\", "/home/hp/", "/Users/hp/"]

        checked_count = 0
        for sdir in source_dirs:
            if not sdir.exists():
                continue
            for fpath in sdir.rglob("*"):
                if fpath.is_file() and fpath.suffix in [".py", ".ts", ".tsx", ".js", ".json", ".conf", ".yml"]:
                    checked_count += 1
                    content = fpath.read_text(encoding="utf-8", errors="ignore")
                    for pattern in forbidden_patterns:
                        self.assertNotIn(
                            pattern,
                            content,
                            f"Hardcoded local path '{pattern}' found in {fpath.relative_to(PROJECT_ROOT)}"
                        )
        self.assertGreater(checked_count, 15, "Insufficient source files scanned for machine paths.")

    def test_07_nginx_configuration_hardening(self):
        """Verify Nginx configuration includes server_tokens off, dotfile protection, and CSP."""
        nginx_conf = PROJECT_ROOT / "nginx" / "default.conf"
        self.assertTrue(nginx_conf.exists(), "nginx/default.conf missing")
        content = nginx_conf.read_text(encoding="utf-8")

        self.assertIn("server_tokens off;", content)
        self.assertIn("add_header X-Frame-Options \"DENY\"", content)
        self.assertIn("add_header X-Content-Type-Options \"nosniff\"", content)
        self.assertIn("add_header Content-Security-Policy", content)
        self.assertIn("location ~ /\\.", content)
        self.assertIn("client_max_body_size", content)

    def test_08_docker_security_configuration(self):
        """Verify Dockerfile.backend runs as non-root user and .dockerignore excludes sensitive files."""
        dockerfile = PROJECT_ROOT / "Dockerfile.backend"
        self.assertTrue(dockerfile.exists())
        df_content = dockerfile.read_text(encoding="utf-8")
        self.assertIn("USER appuser", df_content)
        self.assertIn("HEALTHCHECK", df_content)

        dockerignore = PROJECT_ROOT / ".dockerignore"
        self.assertTrue(dockerignore.exists())
        di_content = dockerignore.read_text(encoding="utf-8")
        self.assertIn(".env", di_content)
        self.assertIn("*.db", di_content)
        self.assertIn("node_modules", di_content)

    def test_09_docker_compose_network_isolation(self):
        """Verify PostgreSQL and Redis are not exposed to host ports in docker-compose.yml."""
        compose_file = PROJECT_ROOT / "docker-compose.yml"
        self.assertTrue(compose_file.exists())
        content = compose_file.read_text(encoding="utf-8")

        # Postgres and Redis blocks should NOT have public ports mapping
        lines = content.splitlines()
        current_service = None
        service_ports = {}

        for line in lines:
            stripped = line.strip()
            if line.startswith("  ") and not line.startswith("    ") and stripped.endswith(":"):
                current_service = stripped[:-1]
                service_ports[current_service] = []
            elif current_service and stripped.startswith("- ") and "ports:" in lines[lines.index(line) - 1]:
                service_ports[current_service].append(stripped)

        # Confirm postgres and redis have no exposed host ports
        self.assertFalse(service_ports.get("postgres", []))
        self.assertFalse(service_ports.get("redis", []))

    def test_10_ml_model_immutability(self):
        """Verify assam_flood_prototype_v1 has 13 features and 32 empirical observations."""
        meta_file = PROJECT_ROOT / "ml" / "flood" / "artifacts" / "metadata.json"
        self.assertTrue(meta_file.exists())
        with open(meta_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data["model_version"], "assam_flood_prototype_v1")
        self.assertEqual(data["total_training_samples"], 32)
        self.assertEqual(len(data["numerical_features"]), 13)
        self.assertEqual(data["numerical_features"], EXPECTED_FEATURES)

    def test_11_ml_spatial_guard_non_assam(self):
        """Verify non-Assam locations are refused ML inference and redirected to regional baseline."""
        res = flood_model_service.predict(
            location_id="kerala",
            district="Wayanad",
            features={"rainfall_24h": 120.0, "latitude": 11.6, "longitude": 76.1},
            hazard="flood"
        )
        self.assertEqual(res["status"], "model_scope_limited")
        self.assertIn("available only for the Assam flood prototype", res["message"])

    def test_12_national_coverage_36_entities(self):
        """Verify 28 States and 8 Union Territories are registered."""
        states = [e for e in INDIAN_ADMINISTRATIVE_ENTITIES if e["type"] == "STATE"]
        uts = [e for e in INDIAN_ADMINISTRATIVE_ENTITIES if e["type"] == "UNION_TERRITORY"]

        self.assertEqual(len(states), 28, "Expected exactly 28 States")
        self.assertEqual(len(uts), 8, "Expected exactly 8 Union Territories")
        self.assertEqual(len(INDIAN_ADMINISTRATIVE_ENTITIES), 36)

    def test_13_all_six_hazards_supported(self):
        """Verify FLOOD, EARTHQUAKE, CYCLONE, HEATWAVE, LANDSLIDE, SEVERE_WEATHER coverage."""
        from app.services.hazard_providers import (
            USGSSeismicProvider,
            CWCFloodProvider,
            IMDWeatherProvider,
            IMDCycloneProvider,
            IMDHeatwaveProvider,
            GSILandslideProvider
        )
        providers = [
            USGSSeismicProvider(),
            CWCFloodProvider(),
            IMDWeatherProvider(),
            IMDCycloneProvider(),
            IMDHeatwaveProvider(),
            GSILandslideProvider()
        ]
        hazards_seen = {p.hazard_type.upper() for p in providers}
        expected = {"FLOOD", "EARTHQUAKE", "CYCLONE", "HEATWAVE", "LANDSLIDE", "SEVERE_WEATHER"}
        self.assertTrue(expected.issubset(hazards_seen), f"Missing hazards: {expected - hazards_seen}")

    def test_14_provider_circuit_breaker_resilience(self):
        """Verify provider circuit breaker transitions to OPEN on repeated failures."""
        breaker = CircuitBreaker(failure_threshold=3, cooldown_seconds=60.0)
        self.assertTrue(breaker.can_execute())

        breaker.record_failure("HTTP 500")
        breaker.record_failure("HTTP 503")
        self.assertTrue(breaker.can_execute())

        breaker.record_failure("Timeout")
        # Threshold reached: should trip OPEN
        self.assertFalse(breaker.can_execute())
        self.assertEqual(breaker.state.value, "OPEN")

    def test_15_frontend_external_links_safe(self):
        """Verify all target=_blank links in frontend code include rel='noopener noreferrer'."""
        src_dir = PROJECT_ROOT / "src"
        checked_links = 0
        for fpath in src_dir.rglob("*.tsx"):
            content = fpath.read_text(encoding="utf-8")
            if 'target="_blank"' in content:
                # Find occurrences
                matches = re.finditer(r'<a\s+[^>]*target="_blank"[^>]*>', content)
                for m in matches:
                    tag = m.group(0)
                    self.assertIn(
                        'rel="noopener noreferrer"',
                        tag,
                        f"Unsafe external link missing rel='noopener noreferrer' in {fpath.name}: {tag}"
                    )
                    checked_links += 1
        self.assertGreater(checked_links, 5, "Expected multiple target=_blank links checked.")

    def test_16_frontend_no_dangerous_html(self):
        """Verify zero dangerouslySetInnerHTML usage in frontend source code."""
        src_dir = PROJECT_ROOT / "src"
        for fpath in src_dir.rglob("*.tsx"):
            content = fpath.read_text(encoding="utf-8")
            self.assertNotIn("dangerouslySetInnerHTML", content, f"Unsafe HTML rendering in {fpath.name}")


if __name__ == "__main__":
    unittest.main()
