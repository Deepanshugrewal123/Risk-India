"""
RISK // INDIA — Dedicated Flood ML Model Inference Service
Seamless integration of the trained Assam flood prototype model (assam_flood_prototype_v1).
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timezone
import pandas as pd
import numpy as np
import joblib

# Paths to artifacts in ml/flood/artifacts/
PROJECT_ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS_DIR = PROJECT_ROOT / "ml" / "flood" / "artifacts"
MODEL_PATH = ARTIFACTS_DIR / "model.joblib"
PREPROCESSOR_PATH = ARTIFACTS_DIR / "preprocessor.joblib"
METADATA_PATH = ARTIFACTS_DIR / "metadata.json"

# The 13 empirical features expected by the trained model (strictly no future data)
EXPECTED_FEATURES = [
    "rainfall_6h",
    "rainfall_24h",
    "rainfall_72h",
    "rainfall_168h",
    "river_level_relative",
    "river_rise_6h",
    "river_rise_24h",
    "river_percentile_level",
    "month",
    "day_of_year_sin",
    "day_of_year_cos",
    "latitude",
    "longitude",
]

DISPLAY_LABELS = {
    "rainfall_72h": "72-Hour Cumulative Rainfall",
    "rainfall_24h": "24-Hour Rainfall",
    "rainfall_168h": "7-Day Antecedent Precipitation",
    "rainfall_6h": "6-Hour Precipitation",
    "river_rise_6h": "6-Hour River Surge",
    "river_rise_24h": "24-Hour River Stage Rise",
    "river_percentile_level": "Seasonal River Level Percentile",
    "river_level_relative": "River Stage Above Seasonal Minimum",
    "month": "Monsoon Month Cycle",
    "day_of_year_sin": "Storm Phase (Sine)",
    "day_of_year_cos": "Storm Phase (Cosine)",
    "latitude": "Catchment Latitude",
    "longitude": "Catchment Longitude",
}

SUPPORTED_ASSAM_LOCATIONS = {"assam", "as", "assam-state", "in-as"}

# Known CWC gauge reference stations in Assam with empirical coordinates
ASSAM_GAUGE_PROFILES = {
    "udalguri": {
        "name": "NH15 Crossing Dhansirighat",
        "river": "Dhansiri (North)",
        "district": "Udalguri",
        "latitude": 26.6958,
        "longitude": 92.2578,
    },
    "darrang": {
        "name": "NH15 Crossing Fakirpara Tangni",
        "river": "Tangni",
        "district": "Darrang",
        "latitude": 26.5083,
        "longitude": 92.1164,
    },
    "kamrup": {
        "name": "NH17 Crossing Boko",
        "river": "Boko",
        "district": "Kamrup",
        "latitude": 25.9775,
        "longitude": 91.2342,
    },
    "kamrup metro": {
        "name": "NH17 Crossing Boko",
        "river": "Boko",
        "district": "Kamrup Metro",
        "latitude": 25.9775,
        "longitude": 91.2342,
    },
    "kamrup rural": {
        "name": "NH17 Crossing Boko",
        "river": "Boko",
        "district": "Kamrup Rural",
        "latitude": 25.9775,
        "longitude": 91.2342,
    }
}


class FloodModelService:
    """
    Thread-safe, singleton ML inference service for the Assam flood prototype model.
    Loads model and preprocessor once at application startup.
    """

    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.metadata = None
        self.model_version = "assam_flood_prototype_v1"
        self.load_error = None
        self.load_model()

    def load_model(self) -> bool:
        """Attempts to load model artifacts from disk."""
        try:
            if not MODEL_PATH.exists() or not PREPROCESSOR_PATH.exists():
                self.load_error = f"Artifacts not found in {ARTIFACTS_DIR}"
                return False

            self.model = joblib.load(MODEL_PATH)
            self.preprocessor = joblib.load(PREPROCESSOR_PATH)
            if METADATA_PATH.exists():
                with open(METADATA_PATH, "r", encoding="utf-8") as f:
                    self.metadata = json.load(f)
                self.model_version = self.metadata.get("model_version", "assam_flood_prototype_v1")

            self.load_error = None
            print(f"[FloodModelService] Loaded {self.model_version} successfully from {MODEL_PATH}")
            return True
        except Exception as e:
            self.load_error = str(e)
            print(f"[FloodModelService] Error loading model: {e}")
            return False

    @property
    def is_ready(self) -> bool:
        return self.model is not None and self.preprocessor is not None

    def is_supported_location(self, location_id: str, district: Optional[str] = None) -> bool:
        """
        Assam Scope Guard: Checks if the target location falls within the supported Assam prototype basin.
        """
        clean_loc = (location_id or "").lower().strip()
        clean_dist = (district or "").lower().strip()

        if clean_loc in SUPPORTED_ASSAM_LOCATIONS:
            return True
        if clean_dist in ASSAM_GAUGE_PROFILES:
            return True
        if "assam" in clean_loc:
            return True
        return False

    def predict(
        self,
        location_id: str,
        district: Optional[str] = None,
        features: Optional[Dict[str, Any]] = None,
        hazard: str = "flood"
    ) -> Dict[str, Any]:
        """
        Executes end-to-end flood risk inference adhering to model inference contracts.
        """
        loc_id = location_id.lower().strip()
        dist_clean = (district or "").lower().strip()

        # 1. Model Availability Guard
        if not self.is_ready:
            if not self.load_model():
                return {
                    "status": "model_unavailable",
                    "message": f"ML prototype model is currently unavailable: {self.load_error}",
                    "location_id": location_id,
                    "district": district,
                    "hazard": hazard,
                    "model_version": self.model_version,
                    "is_prototype": True,
                    "emergency_warning": False
                }

        # 2. Assam Scope Guard (Section 8)
        hazard_clean = (hazard or "flood").lower().strip()
        if hazard_clean not in ["flood", "waterlogging", "inundation"]:
            return {
                "status": "model_scope_limited",
                "message": "AI risk analysis is currently available only for the Assam flood prototype (limited to selected Assam monitoring areas).",
                "location_id": location_id,
                "district": district,
                "hazard": hazard,
                "model_version": self.model_version,
                "is_prototype": True,
                "emergency_warning": False
            }

        if not self.is_supported_location(loc_id, district=dist_clean):
            return {
                "status": "model_scope_limited",
                "message": "AI risk analysis is currently available only for the Assam flood prototype (limited to selected Assam monitoring areas).",
                "location_id": location_id,
                "district": district,
                "hazard": hazard,
                "model_version": self.model_version,
                "is_prototype": True,
                "emergency_warning": False
            }

        # 3. Missing Inputs Guard (Section 7)
        feat_dict = dict(features or {})

        # If district matches a known gauge, provide default coordinates if omitted
        gauge_prof = ASSAM_GAUGE_PROFILES.get(dist_clean)
        if gauge_prof:
            if feat_dict.get("latitude") is None:
                feat_dict["latitude"] = gauge_prof["latitude"]
            if feat_dict.get("longitude") is None:
                feat_dict["longitude"] = gauge_prof["longitude"]

        # Check for essential environmental inputs (rainfall or river level)
        has_rainfall = any(
            feat_dict.get(k) is not None and not pd.isna(feat_dict.get(k))
            for k in ["rainfall_6h", "rainfall_24h", "rainfall_72h", "rainfall_168h"]
        )
        has_river = any(
            feat_dict.get(k) is not None and not pd.isna(feat_dict.get(k))
            for k in ["river_level_relative", "river_rise_6h", "river_rise_24h", "river_percentile_level"]
        )

        if not has_rainfall and not has_river:
            return {
                "status": "insufficient_data",
                "message": "Insufficient environmental data available for this prototype analysis.",
                "location_id": location_id,
                "district": district,
                "hazard": hazard,
                "model_version": self.model_version,
                "is_prototype": True,
                "emergency_warning": False
            }

        # Default temporal signals to current time if omitted
        now = datetime.now(timezone.utc)
        if feat_dict.get("month") is None:
            feat_dict["month"] = now.month
        if feat_dict.get("day_of_year_sin") is None or feat_dict.get("day_of_year_cos") is None:
            doy = now.timetuple().tm_yday
            feat_dict["day_of_year_sin"] = round(np.sin(2 * np.pi * doy / 365.25), 5)
            feat_dict["day_of_year_cos"] = round(np.cos(2 * np.pi * doy / 365.25), 5)

        # 4. Construct input DataFrame for expected features
        row = {}
        for col in EXPECTED_FEATURES:
            val = feat_dict.get(col)
            row[col] = [val if val is not None else np.nan]

        df_input = pd.DataFrame(row)

        # 5. Preprocessing & Prediction
        try:
            X_proc = self.preprocessor.transform(df_input)
            prob = float(self.model.predict_proba(X_proc)[0, 1])
            prob = max(0.0, min(1.0, prob))
        except Exception as e:
            return {
                "status": "inference_error",
                "message": f"Error during ML pipeline transformation: {str(e)}",
                "location_id": location_id,
                "district": district,
                "hazard": hazard,
                "model_version": self.model_version,
                "is_prototype": True,
                "emergency_warning": False
            }

        # Deterministic Risk Score transformation (0-100)
        risk_score = int(round(prob * 100))

        # Risk Level based on thresholds (0-25: Low, 26-50: Moderate, 51-75: High, 76-100: Critical)
        if risk_score <= 25:
            risk_level = "Low"
        elif risk_score <= 50:
            risk_level = "Moderate"
        elif risk_score <= 75:
            risk_level = "High"
        else:
            risk_level = "Critical"

        # 6. Model Explanation ("Why this risk?") (Section 5)
        top_factors = self._compute_explanations(X_proc[0], feat_dict)

        # Recommended guidance
        recommended_action = self._get_action(risk_level)

        return {
            "status": "success",
            "location_id": location_id,
            "district": district or (gauge_prof["district"] if gauge_prof else "Assam Valley"),
            "state": "Assam",
            "hazard": hazard,
            "model_version": self.model_version,
            "flood_probability": round(prob, 4),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "top_factors": top_factors,
            "is_prototype": True,
            "emergency_warning": False,
            "recommended_action": recommended_action,
            "disclaimer": (
                "Experimental Assam flood-risk prototype based on a limited event dataset. "
                "Results are for research and awareness only and should not replace official emergency warnings."
            ),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _compute_explanations(self, scaled_vals: np.ndarray, raw_features: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Calculates exact linear contribution for each feature:
        contribution = coef * scaled_val
        """
        if not hasattr(self.model, "coef_"):
            return []

        coefs = self.model.coef_[0]
        factor_items = []

        for i, feat_name in enumerate(EXPECTED_FEATURES):
            scaled_val = scaled_vals[i]
            coef = coefs[i]
            contribution = float(coef * scaled_val)
            raw_val = raw_features.get(feat_name)

            direction = "increases_risk" if contribution > 0 else "decreases_risk"
            label = DISPLAY_LABELS.get(feat_name, feat_name.replace("_", " ").title())

            # Format human-readable value string
            if raw_val is not None and not pd.isna(raw_val):
                if "rainfall" in feat_name:
                    val_str = f"{float(raw_val):.1f} mm"
                elif "rise" in feat_name:
                    val_str = f"{float(raw_val):+.2f} m"
                elif feat_name == "river_percentile_level":
                    val_str = f"{float(raw_val)*100:.1f}%"
                elif feat_name == "river_level_relative":
                    val_str = f"{float(raw_val):.2f} m"
                else:
                    val_str = str(raw_val)
            else:
                val_str = "Imputed Median"

            factor_items.append({
                "feature": feat_name,
                "contribution": round(contribution, 4),
                "direction": direction,
                "display_label": label,
                "value": val_str,
                "abs_contribution": abs(contribution)
            })

        # Rank by absolute magnitude of contribution
        factor_items.sort(key=lambda x: x["abs_contribution"], reverse=True)

        # Return top 4 most influential factors without internal sorting key
        for item in factor_items:
            del item["abs_contribution"]

        return factor_items[:4]

    def _get_action(self, level: str) -> str:
        if level == "Critical":
            return "Extreme catchment water ingress predicted. Evacuate low-lying floodplains and monitor official CWC bulletins."
        elif level == "High":
            return "Significant river swelling anticipated. Prepare essential emergency supplies and secure livestock/property."
        elif level == "Moderate":
            return "Elevated streamflow and surface runoff likely. Monitor local drainage channels and local weather advisories."
        else:
            return "Normal seasonal hydrological flow. Maintain standard preparedness and monitor monsoon forecasts."


# Singleton instance
flood_model_service = FloodModelService()
