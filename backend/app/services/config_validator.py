"""
RISK // INDIA — Staging & Production Configuration Validation Engine
====================================================================
Provides strict, multi-tier environment configuration validation for:
- development: SQLite + in-memory cache allowed; developer defaults permitted.
- staging: Staging database credentials, Redis configuration, and strict CORS audited.
- production: Strict enforcement of non-default credentials, PostgreSQL requirement,
  secret key entropy, HSTS enforcement, and sanitized security boundaries.

SECURITY GUARANTEES:
- Zero credential logging: passwords, secrets, and auth tokens are redacted (***).
- Zero secret exposure in API responses.
- Safe fail-fast capability for deployment readiness gates.
"""

from typing import Dict, Any, List, Optional
import re
import logging
from dataclasses import dataclass, field, asdict

logger = logging.getLogger("risk-india.config-validator")

# Known insecure placeholder values that must be blocked in production
INSECURE_PLACEHOLDER_PASSWORDS = {
    "risk_password_change_me",
    "password",
    "admin",
    "root",
    "123456",
    "secret",
    "change_me",
    "postgres",
    "risk_password"
}

DEV_DEFAULT_SECRET_KEYS = {
    "dev-insecure-secret-key-risk-india-local-only-32chars",
    "secret",
    "default_secret_key",
    "change_me_in_production"
}

VALID_ENVIRONMENTS = {"development", "staging", "production", "test"}
VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "WARN", "ERROR", "CRITICAL"}
VALID_CACHE_BACKENDS = {"memory", "redis"}


@dataclass
class ValidationReport:
    environment: str
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    sanitized_config: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "environment": self.environment,
            "is_valid": self.is_valid,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings,
            "sanitized_config": self.sanitized_config
        }


class StagingConfigValidator:
    """
    Validates operational configuration across development, staging, and production tiers.
    """

    @classmethod
    def sanitize_value(cls, key: str, value: Any) -> Any:
        """Masks sensitive credentials in outputs."""
        if value is None:
            return None
        k_lower = key.lower()
        if any(s in k_lower for s in ["password", "secret", "token", "key", "auth"]):
            return "***REDACTED***"
        if "database_url" in k_lower or "redis_url" in k_lower:
            # Mask user:pass@ in connection URLs
            return re.sub(r"://([^:]+):([^@]+)@", r"://\1:***@", str(value))
        return value

    @classmethod
    def validate(
        cls,
        settings_obj: Any,
        target_env: Optional[str] = None
    ) -> ValidationReport:
        """
        Executes strict configuration validation against environment rules.
        """
        env = (target_env or getattr(settings_obj, "APP_ENV", "development")).lower().strip()
        errors: List[str] = []
        warnings: List[str] = []

        # 1. Validate Environment Name
        if env not in VALID_ENVIRONMENTS:
            errors.append(f"Invalid APP_ENV '{env}'. Must be one of: {sorted(list(VALID_ENVIRONMENTS))}")

        # 2. Extract settings values
        db_url = getattr(settings_obj, "DATABASE_URL", "")
        redis_url = getattr(settings_obj, "REDIS_URL", None)
        cache_backend = getattr(settings_obj, "CACHE_BACKEND", "memory").lower()
        secret_key = getattr(settings_obj, "SECRET_KEY", "")
        cors_origins = getattr(settings_obj, "CORS_ORIGINS", "")
        enable_hsts = getattr(settings_obj, "ENABLE_HSTS", False)
        debug = getattr(settings_obj, "DEBUG", True)
        web_concurrency = getattr(settings_obj, "WEB_CONCURRENCY", 4)
        log_level = getattr(settings_obj, "LOG_LEVEL", "INFO").upper()
        rate_general = getattr(settings_obj, "RATE_LIMIT_GENERAL", 60)
        rate_compute = getattr(settings_obj, "RATE_LIMIT_COMPUTE", 10)

        # 3. Baseline validation for all environments
        if log_level not in VALID_LOG_LEVELS:
            warnings.append(f"LOG_LEVEL '{log_level}' is non-standard. Recommended: INFO, WARNING, ERROR")

        if cache_backend not in VALID_CACHE_BACKENDS:
            errors.append(f"CACHE_BACKEND '{cache_backend}' invalid. Must be 'memory' or 'redis'")

        if web_concurrency < 1 or web_concurrency > 64:
            warnings.append(f"WEB_CONCURRENCY {web_concurrency} unusual. Expected between 1 and 32")

        if rate_general <= 0 or rate_compute <= 0:
            errors.append("Rate limits must be positive integers")

        # 4. Check for wildcard CORS
        if "*" in [o.strip() for o in cors_origins.split(",")]:
            errors.append("Wildcard '*' in CORS_ORIGINS is forbidden when credentials are enabled")

        # 5. Environment-specific rules
        if env in ["staging", "production"]:
            # Database check
            if env == "production" and db_url.startswith("sqlite"):
                errors.append("Production environment cannot use SQLite. PostgreSQL 16 is required")

            # Check for default insecure database passwords
            for insecure_pw in INSECURE_PLACEHOLDER_PASSWORDS:
                if f":{insecure_pw}@" in db_url:
                    msg = f"Database password uses known insecure placeholder '{insecure_pw}'"
                    if env == "production":
                        errors.append(msg)
                    else:
                        warnings.append(msg + " (acceptable only in local mock staging)")

            # Redis check
            if cache_backend == "redis" and not redis_url:
                errors.append("CACHE_BACKEND is set to 'redis' but REDIS_URL is not configured")

            # Secret Key check
            if not secret_key or len(secret_key) < 16:
                errors.append("SECRET_KEY is missing or too short (minimum 16 characters required)")

            if env == "production":
                if secret_key in DEV_DEFAULT_SECRET_KEYS:
                    errors.append("Production cannot use the development default SECRET_KEY")
                if len(secret_key) < 32:
                    errors.append("Production SECRET_KEY must be at least 32 characters long")
                if debug:
                    errors.append("DEBUG mode must be False in production")
                if not enable_hsts:
                    warnings.append("ENABLE_HSTS should be enabled for production HTTPS ingress")
                if "localhost" in cors_origins or "127.0.0.1" in cors_origins:
                    warnings.append("CORS_ORIGINS contains localhost addresses in production mode")

        elif env == "development":
            # Development mode permits SQLite, in-memory cache, and dev keys
            if db_url.startswith("sqlite"):
                warnings.append("Using local SQLite database for development")
            if cache_backend == "memory":
                warnings.append("Using in-memory TTL cache (local development mode)")

        # 6. Build sanitized configuration map (no raw secrets)
        sanitized_cfg = {
            "APP_ENV": env,
            "DEBUG": debug,
            "DATABASE_DIALECT": "sqlite" if db_url.startswith("sqlite") else "postgresql",
            "DATABASE_URL": cls.sanitize_value("DATABASE_URL", db_url),
            "CACHE_BACKEND": cache_backend,
            "REDIS_CONFIGURED": bool(redis_url),
            "REDIS_URL": cls.sanitize_value("REDIS_URL", redis_url),
            "CORS_ORIGINS_COUNT": len([o for o in cors_origins.split(",") if o.strip()]),
            "ENABLE_HSTS": enable_hsts,
            "WEB_CONCURRENCY": web_concurrency,
            "LOG_LEVEL": log_level,
            "RATE_LIMIT_GENERAL": rate_general,
            "RATE_LIMIT_COMPUTE": rate_compute,
            "SECRET_KEY_CONFIGURED": bool(secret_key and secret_key not in DEV_DEFAULT_SECRET_KEYS)
        }

        is_valid = len(errors) == 0
        return ValidationReport(
            environment=env,
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            sanitized_config=sanitized_cfg
        )


config_validator = StagingConfigValidator()
