from typing import Literal

RiskLevelType = Literal["LOW", "MODERATE", "HIGH", "CRITICAL"]

# Provisional prototype thresholds
RISK_THRESHOLDS = {
    "LOW": (0, 25),
    "MODERATE": (26, 50),
    "HIGH": (51, 75),
    "CRITICAL": (76, 100),
}

def classify_risk_score(score: float | int) -> RiskLevelType:
    """
    Centralized risk-level classification.
    Provisional Prototype Bands:
      0 - 25:   LOW
      26 - 50:  MODERATE
      51 - 75:  HIGH
      76 - 100: CRITICAL
    """
    bounded_score = max(0, min(100, round(float(score))))
    if bounded_score <= 25:
        return "LOW"
    elif bounded_score <= 50:
        return "MODERATE"
    elif bounded_score <= 75:
        return "HIGH"
    else:
        return "CRITICAL"
