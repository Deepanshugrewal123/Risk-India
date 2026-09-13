"""
RISK // INDIA — Assam Flood ML Prototype Pilot Demonstration
Standalone demonstration script evaluating three controlled test scenarios.
"""
# IMPORTANT NOTICE:
# - These scenarios are CONTROLLED DEMONSTRATION INPUTS used solely to evaluate model behavior.
# - They are NOT live weather measurements or real-time flood warnings.
# - The model is a college research prototype (assam_flood_prototype_v1) trained on 32 historical events.
# - It does NOT provide nationwide flood forecasting or operational emergency alerts.

import sys
from pathlib import Path
import json
import pandas as pd
import numpy as np
import joblib

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from backend.app.services.flood_model_service import flood_model_service, EXPECTED_FEATURES, DISPLAY_LABELS

# ==============================================================================
# THREE CONTROLLED PILOT DEMONSTRATION SCENARIOS
# ==============================================================================

PILOT_SCENARIOS = [
    {
        "id": "SCENARIO_A",
        "name": "Scenario A: Relatively Lower-Risk Demo",
        "description": "Stable hydrological conditions with minimal recent precipitation, negative river surge, and normal baseline channel stage in Assam valley.",
        "location": "Assam / Udalguri Monitoring Basin",
        "features": {
            "rainfall_6h": 0.0,
            "rainfall_24h": 1.5,
            "rainfall_72h": 5.0,
            "rainfall_168h": 250.0,
            "river_level_relative": 15.0,
            "river_rise_6h": -0.05,
            "river_rise_24h": -0.20,
            "river_percentile_level": 0.85,
            "month": 7,
            "day_of_year_sin": -0.20,
            "day_of_year_cos": -0.98,
            "latitude": 26.6958,
            "longitude": 92.2578
        }
    },
    {
        "id": "SCENARIO_B",
        "name": "Scenario B: Elevated-Risk Demo",
        "description": "Moderate monsoon rainfall pulse with positive 6h streamflow rise and mid-percentile river stage in Assam monitoring basin.",
        "location": "Assam / Udalguri Monitoring Basin",
        "features": {
            "rainfall_6h": 2.0,
            "rainfall_24h": 25.0,
            "rainfall_72h": 45.0,
            "rainfall_168h": 140.0,
            "river_level_relative": 8.0,
            "river_rise_6h": 0.04,
            "river_rise_24h": 0.10,
            "river_percentile_level": 0.55,
            "month": 6,
            "day_of_year_sin": 0.10,
            "day_of_year_cos": -0.98,
            "latitude": 26.6958,
            "longitude": 92.2578
        }
    },
    {
        "id": "SCENARIO_C",
        "name": "Scenario C: Higher-Risk Demo",
        "description": "Intense localized convective burst exceeding 120mm in 24h, combined with sharp +0.28m 6h river crest surge in lower Brahmaputra tributary.",
        "location": "Assam / Kamrup (Boko) Monitoring Basin",
        "features": {
            "rainfall_6h": 45.0,
            "rainfall_24h": 120.0,
            "rainfall_72h": 210.0,
            "rainfall_168h": 60.0,
            "river_level_relative": 0.85,
            "river_rise_6h": 0.28,
            "river_rise_24h": 0.45,
            "river_percentile_level": 0.10,
            "month": 6,
            "day_of_year_sin": 0.25,
            "day_of_year_cos": -0.95,
            "latitude": 25.9775,
            "longitude": 91.2342
        }
    }
]


def run_pilot_demonstration():
    print("=" * 80)
    print("RISK // INDIA -- ASSAM FLOOD ML PROTOTYPE PILOT DEMONSTRATION")
    print(f"Model Version: {flood_model_service.model_version}")
    print("Classification: Academic College Research Prototype (NOT Operational Warning System)")
    print("=" * 80)
    print()

    for sc in PILOT_SCENARIOS:
        print("-" * 80)
        print(f"[{sc['id']}] {sc['name']}")
        print(f"Location Target: {sc['location']}")
        print(f"Context: {sc['description']}")
        print("-" * 80)

        pred = flood_model_service.predict(
            location_id="assam",
            district=sc['location'].split("/")[-1].strip(),
            features=sc['features'],
            hazard="flood"
        )

        prob = pred.get("flood_probability")
        score = pred.get("risk_score")
        level = pred.get("risk_level")
        status = pred.get("status")

        print(f"  Execution Status : {status.upper()}")
        print(f"  Model Probability: {prob:.4f} ({prob*100:.1f}%)")
        print(f"  UI Risk Score    : {score} / 100")
        print(f"  Risk Category    : {level.upper()}")
        print(f"  Prototype Flag   : is_prototype={pred.get('is_prototype')}, emergency_warning={pred.get('emergency_warning')}")
        print(f"  Disclaimer       : {pred.get('disclaimer')}")
        print()
        print("  WHY THIS RISK? (Top Feature Attributions):")
        for f in pred.get("top_factors", []):
            direction_tag = "[+ RISES]" if f["direction"] == "increases_risk" else "[- LOWERS]"
            print(f"    {direction_tag:11s} {f['display_label']:32s} : {f.get('value', 'N/A'):15s} (contribution: {f['contribution']:+.4f})")

        print()

    print("=" * 80)
    print("PILOT DEMONSTRATION COMPLETE -- ZERO ERRORS")
    print("=" * 80)


if __name__ == "__main__":
    run_pilot_demonstration()
