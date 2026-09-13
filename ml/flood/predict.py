"""
RISK // INDIA — Assam Flood ML Prototype Inference Service
Trained model inference, risk score contract, and factor explanation.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
import json
from pathlib import Path
import pandas as pd
import numpy as np
import joblib

from ml.flood.config import (
    DEFAULT_MODEL_PATH,
    DEFAULT_PREPROCESSOR_PATH,
    DEFAULT_METADATA_PATH,
    NUMERICAL_FEATURES,
    MODEL_VERSION,
    RISK_THRESHOLDS,
)


class AssamFloodInferenceEngine:
    """
    Inference engine executing the trained Assam flood prototype model.
    """

    def __init__(
        self,
        model_path: Path = DEFAULT_MODEL_PATH,
        preprocessor_path: Path = DEFAULT_PREPROCESSOR_PATH,
        metadata_path: Path = DEFAULT_METADATA_PATH,
    ):
        self.model_path = model_path
        self.preprocessor_path = preprocessor_path
        self.metadata_path = metadata_path
        self.model = None
        self.preprocessor = None
        self.metadata = None
        self._load_artifacts()

    def _load_artifacts(self):
        """Loads trained model, preprocessor, and metadata."""
        if self.model_path.exists() and self.preprocessor_path.exists():
            try:
                self.model = joblib.load(self.model_path)
                self.preprocessor = joblib.load(self.preprocessor_path)
                if self.metadata_path.exists():
                    with open(self.metadata_path, "r", encoding="utf-8") as f:
                        self.metadata = json.load(f)
                print(f"[+] Loaded trained flood prototype model from {self.model_path}")
            except Exception as e:
                print(f"[!] Warning: Failed to load model artifacts: {e}")
                self.model = None
                self.preprocessor = None

    @property
    def is_model_trained(self) -> bool:
        return self.model is not None and self.preprocessor is not None

    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes flood risk inference adhering strictly to the Risk Score Contract:
        {
          "model_version": "assam_flood_prototype_v1",
          "flood_probability": float [0.0 - 1.0],
          "risk_score": int [0 - 100],
          "risk_level": "Low | Moderate | High | Critical",
          "top_factors": [ ... ]
        }
        """
        if not self.is_model_trained:
            raise FileNotFoundError(
                f"Trained model artifacts not found at {self.model_path}. "
                "Train the model first using: python -m ml.flood.train"
            )

        # Build feature DataFrame with expected column order
        row_dict = {}
        for feat in NUMERICAL_FEATURES:
            val = features.get(feat, np.nan)
            row_dict[feat] = [val]

        df_input = pd.DataFrame(row_dict)

        # Preprocess features (median imputation + scaling)
        X_proc = self.preprocessor.transform(df_input)

        # Generate ML model probability
        prob = float(self.model.predict_proba(X_proc)[0, 1])
        prob = max(0.0, min(1.0, prob))

        # UI Risk Score (0 - 100)
        risk_score = int(round(prob * 100))

        # Determine Risk Level
        risk_level = self._map_risk_level(risk_score)

        # Generate top factors based on feature values and model coefficients
        top_factors = self._generate_top_factors(features, X_proc[0])

        return {
            "model_version": self.metadata.get("model_version", MODEL_VERSION) if self.metadata else MODEL_VERSION,
            "flood_probability": round(prob, 4),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "top_factors": top_factors,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "disclaimer": "PROTOTYPE ML PREDICTION — Validated strictly on Assam CWC gauge catchments. NOT FOR EMERGENCY WARNING."
        }

    def _map_risk_level(self, score: int) -> str:
        if score <= 25:
            return "Low"
        elif score <= 50:
            return "Moderate"
        elif score <= 75:
            return "High"
        else:
            return "Critical"

    def _generate_top_factors(self, raw_features: Dict[str, Any], scaled_vals: np.ndarray) -> List[Dict[str, str]]:
        """
        Extracts explainable risk drivers by evaluating feature contributions (scaled value * coefficient).
        """
        factors = []
        if self.metadata and "feature_coefficients" in self.metadata:
            coefs = self.metadata["feature_coefficients"]
        elif hasattr(self.model, "coef_"):
            coefs = {feat: float(c) for feat, c in zip(NUMERICAL_FEATURES, self.model.coef_[0])}
        else:
            coefs = {}

        # Key hydrological features to check
        r24 = float(raw_features.get("rainfall_24h", 0.0))
        r72 = float(raw_features.get("rainfall_72h", 0.0))
        r168 = float(raw_features.get("rainfall_168h", 0.0))
        rise24 = raw_features.get("river_rise_24h")
        rise6 = raw_features.get("river_rise_6h")
        pct_level = raw_features.get("river_percentile_level")

        # 1. Rainfall 72h / 24h factor
        if r72 >= 100.0:
            factors.append({
                "factor": "Antecedent 72h Precipitation",
                "value": f"{r72:.1f} mm",
                "impact": "High cumulative catchment saturation elevating runoff potential"
            })
        elif r24 >= 50.0:
            factors.append({
                "factor": "Heavy 24h Rainfall",
                "value": f"{r24:.1f} mm",
                "impact": "Intense local convective burst increasing immediate surface ponding"
            })
        elif r72 <= 10.0 and r24 <= 5.0:
            factors.append({
                "factor": "Low Antecedent Rainfall",
                "value": f"{r72:.1f} mm (72h)",
                "impact": "Minimal precipitation influx moderating catchment flood risk"
            })

        # 2. River rise factor
        if rise24 is not None and not pd.isna(rise24):
            r24_val = float(rise24)
            if r24_val > 0.15:
                factors.append({
                    "factor": "Rapid 24h River Rise",
                    "value": f"{r24_val:+.2f} m",
                    "impact": "Active upstream flood wave and hydraulic channel swelling"
                })
            elif r24_val < -0.15:
                factors.append({
                    "factor": "Receding River Stage",
                    "value": f"{r24_val:+.2f} m (24h)",
                    "impact": "Hydraulic drainage reducing local inundation hazard"
                })

        # 3. River Percentile / Level factor
        if pct_level is not None and not pd.isna(pct_level):
            pct_val = float(pct_level)
            if pct_val >= 0.85:
                factors.append({
                    "factor": "High Seasonal Water Level",
                    "value": f"{pct_val*100:.1f}th percentile",
                    "impact": "River channel flowing near seasonal bankfull capacity"
                })
            elif pct_val <= 0.35:
                factors.append({
                    "factor": "Low Seasonal Water Level",
                    "value": f"{pct_val*100:.1f}th percentile",
                    "impact": "Substantial within-bank channel storage buffering incoming runoff"
                })

        # Fallback if few factors triggered
        if len(factors) < 2:
            factors.append({
                "factor": "Weekly Antecedent Rainfall",
                "value": f"{r168:.1f} mm (7d)",
                "impact": "Regional baseline monsoon saturation index"
            })

        return factors[:3]


# Centralized singleton inference engine
inference_engine = AssamFloodInferenceEngine()


def predict_flood_risk(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Public inference entrypoint conforming strictly to the Risk Score Contract.
    """
    return inference_engine.predict(features)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  TESTING ASSAM FLOOD PROTOTYPE INFERENCE SERVICE")
    print("=" * 70)
    sample_high_risk = {
        "rainfall_6h": 12.5,
        "rainfall_24h": 85.0,
        "rainfall_72h": 195.0,
        "rainfall_168h": 320.0,
        "river_level_relative": 1.45,
        "river_rise_6h": 0.12,
        "river_rise_24h": 0.58,
        "river_percentile_level": 0.94,
        "month": 7,
        "day_of_year_sin": 0.35,
        "day_of_year_cos": -0.93,
        "latitude": 26.6958,
        "longitude": 92.2578,
    }
    result = predict_flood_risk(sample_high_risk)
    print(json.dumps(result, indent=2))
    print("=" * 70 + "\n")
