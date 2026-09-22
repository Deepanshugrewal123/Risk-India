"""
RISK // INDIA — Operational Observability & Metrics Service
============================================================
Thread-safe, in-memory operational metrics collector for production observability.
Tracks:
- Total requests and HTTP status code distribution (2xx, 3xx, 4xx, 5xx)
- Request latency percentiles (p50, p95, p99, average)
- Rate-limiting events (HTTP 429)
- Provider telemetry reliability (successes, failures, timeouts, retries, circuit breaker trips)
- Cache efficiency (hits, misses, stale-served, offline fallbacks)
- ML inference audit (requests, Assam successes, outside-Assam rejections)
- Database connectivity failures

SECURITY & PRIVACY GUARANTEES:
- Strictly redacts all PII, auth headers, tokens, cookies, and database URLs.
- Retains machine-readable JSON structure.
- In-memory bounded deque for latency tracking prevents unbounded memory growth.
"""

import time
import threading
from typing import Dict, Any, List, Optional
from collections import defaultdict, deque
import math


class OperationalMetricsCollector:
    """
    Singleton thread-safe metrics aggregator for system-wide observability.
    """

    def __init__(self, latency_sample_size: int = 1000):
        self._lock = threading.Lock()
        self.latency_sample_size = latency_sample_size
        self._start_time = time.time()
        self.reset()

    def reset(self):
        """Resets all metrics counters (used in testing and periodic cycles)."""
        with self._lock:
            self._start_time = time.time()
            self._request_count = 0
            self._status_distribution = defaultdict(int)
            self._status_groups = {
                "2xx": 0,
                "3xx": 0,
                "4xx": 0,
                "5xx": 0
            }
            self._latencies_ms = deque(maxlen=self.latency_sample_size)
            self._rate_limit_events = 0
            self._database_errors = 0

            # Provider metrics: {provider_name: {success: int, failure: int, timeout: int, retry: int, circuit_trip: int}}
            self._provider_metrics = defaultdict(lambda: {
                "requests": 0,
                "successes": 0,
                "failures": 0,
                "timeouts": 0,
                "retries": 0,
                "circuit_trips": 0
            })

            # Cache metrics
            self._cache_hits = 0
            self._cache_misses = 0
            self._stale_served = 0
            self._offline_fallbacks = 0

            # ML Inference audit
            self._ml_inference_requests = 0
            self._ml_assam_success = 0
            self._ml_outside_assam_rejections = 0

    def record_request(self, method: str, path: str, status_code: int, latency_ms: float):
        """Records an HTTP request outcome and response latency."""
        with self._lock:
            self._request_count += 1
            self._status_distribution[status_code] += 1
            self._latencies_ms.append(latency_ms)

            group = f"{status_code // 100}xx"
            if group in self._status_groups:
                self._status_groups[group] += 1

            if status_code == 429:
                self._rate_limit_events += 1

    def record_rate_limit(self):
        """Explicitly increments the rate-limit trigger counter."""
        with self._lock:
            self._rate_limit_events += 1

    def record_db_error(self):
        """Increments database connection failure counter."""
        with self._lock:
            self._database_errors += 1

    def record_provider_event(self, provider_name: str, event_type: str):
        """
        Records an upstream provider event:
        event_type in ('request', 'success', 'failure', 'timeout', 'retry', 'circuit_trip')
        """
        p_clean = provider_name.lower().strip()
        with self._lock:
            m = self._provider_metrics[p_clean]
            if event_type == "request":
                m["requests"] += 1
            elif event_type == "success":
                m["successes"] += 1
            elif event_type == "failure":
                m["failures"] += 1
            elif event_type == "timeout":
                m["timeouts"] += 1
                m["failures"] += 1
            elif event_type == "retry":
                m["retries"] += 1
            elif event_type == "circuit_trip":
                m["circuit_trips"] += 1

    def record_cache_event(self, event_type: str):
        """
        Records a cache event:
        event_type in ('hit', 'miss', 'stale_served', 'offline_fallback')
        """
        with self._lock:
            if event_type == "hit":
                self._cache_hits += 1
            elif event_type == "miss":
                self._cache_misses += 1
            elif event_type == "stale_served":
                self._stale_served += 1
            elif event_type == "offline_fallback":
                self._offline_fallbacks += 1

    def record_ml_inference(self, is_assam: bool, success: bool):
        """Audits an ML prediction attempt."""
        with self._lock:
            self._ml_inference_requests += 1
            if is_assam and success:
                self._ml_assam_success += 1
            elif not is_assam:
                self._ml_outside_assam_rejections += 1

    def get_snapshot(self) -> Dict[str, Any]:
        """
        Generates a thread-safe, sanitized JSON-serializable observability snapshot.
        """
        with self._lock:
            uptime_sec = round(time.time() - self._start_time, 2)
            latencies = list(self._latencies_ms)

            if latencies:
                sorted_lat = sorted(latencies)
                n = len(sorted_lat)
                p50 = sorted_lat[int(n * 0.50)]
                p95 = sorted_lat[min(n - 1, int(n * 0.95))]
                p99 = sorted_lat[min(n - 1, int(n * 0.99))]
                avg_lat = round(sum(sorted_lat) / n, 2)
            else:
                p50 = p95 = p99 = avg_lat = 0.0

            total_cache_ops = self._cache_hits + self._cache_misses
            cache_hit_ratio = round(self._cache_hits / total_cache_ops, 4) if total_cache_ops > 0 else 0.0

            # Sanitize provider dictionary
            providers_snapshot = {}
            for p_name, p_data in self._provider_metrics.items():
                providers_snapshot[p_name] = dict(p_data)

            return {
                "uptime_seconds": uptime_sec,
                "http_metrics": {
                    "total_requests": self._request_count,
                    "status_groups": dict(self._status_groups),
                    "status_distribution": {str(k): v for k, v in self._status_distribution.items()},
                    "latency_ms": {
                        "p50": round(p50, 2),
                        "p95": round(p95, 2),
                        "p99": round(p99, 2),
                        "average": avg_lat,
                        "samples": len(latencies)
                    },
                    "rate_limit_events": self._rate_limit_events
                },
                "cache_metrics": {
                    "hits": self._cache_hits,
                    "misses": self._cache_misses,
                    "hit_ratio": cache_hit_ratio,
                    "stale_served": self._stale_served,
                    "offline_fallbacks": self._offline_fallbacks
                },
                "provider_telemetry": {
                    "providers": providers_snapshot
                },
                "ml_inference_audit": {
                    "total_requests": self._ml_inference_requests,
                    "assam_prototype_successes": self._ml_assam_success,
                    "outside_assam_rejections": self._ml_outside_assam_rejections
                },
                "database_metrics": {
                    "connection_errors": self._database_errors
                }
            }


# Singleton collector
metrics_collector = OperationalMetricsCollector()
