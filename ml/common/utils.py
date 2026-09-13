"""
RISK // INDIA — ML Common Utilities & Risk Mapping Contracts
Centralizes mathematical conversions from predicted probabilities to standardized risk scores and tiers.
"""

from typing import Literal

RiskLevel = Literal["LOW", "MODERATE", "HIGH", "CRITICAL"]

def probability_to_risk_score(probability: float) -> int:
    """
    Converts a continuous calibrated probability P(Event=1 | X) in [0.0, 1.0]
    to an integer risk score in [0, 100].
    """
    clamped = max(0.0, min(1.0, float(probability)))
    return int(round(clamped * 100))

def probability_to_risk_level(probability: float) -> RiskLevel:
    """
    Standardized provisional probability-to-risk-level mapping across RISK // INDIA.
    
    Bands:
      [0.00, 0.25] -> LOW
      (0.25, 0.50] -> MODERATE
      (0.50, 0.75] -> HIGH
      (0.75, 1.00] -> CRITICAL
    """
    prob = max(0.0, min(1.0, float(probability)))
    if prob <= 0.25:
        return "LOW"
    elif prob <= 0.50:
        return "MODERATE"
    elif prob <= 0.75:
        return "HIGH"
    else:
        return "CRITICAL"

def risk_score_to_risk_level(score: int) -> RiskLevel:
    """
    Maps an integer risk score (0-100) to standard RiskLevel.
    """
    s = max(0, min(100, int(score)))
    if s <= 25:
        return "LOW"
    elif s <= 50:
        return "MODERATE"
    elif s <= 75:
        return "HIGH"
    else:
        return "CRITICAL"
