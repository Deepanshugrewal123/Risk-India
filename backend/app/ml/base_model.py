"""
RISK // INDIA — Backend ML Model Adapter

Connects FastAPI backend directly to the ML intelligence layer (ml/flood/predict.py)
maintaining strict separation between online runtime inference and offline batch training.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Dict, Any, List

# Ensure root directory containing 'ml' is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml.flood.predict import predict_flood_risk, inference_engine


class MLModelInterface(ABC):
    """
    Abstract interface for ML risk inference models.
    """

    @property
    @abstractmethod
    def model_name(self) -> str:
        pass

    @property
    @abstractmethod
    def model_version(self) -> str:
        pass

    @abstractmethod
    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute prediction pipeline given telemetry & geographical features.
        Returns standardized dictionary.
        """
        pass


class FloodRiskModelAdapter(MLModelInterface):
    """
    Inference adapter delegating directly to ml/flood/predict.py.
    Transparently handles both trained pipeline artifacts and provisional fallback states.
    """

    @property
    def model_name(self) -> str:
        return "flood-risk-pipeline"

    @property
    def model_version(self) -> str:
        if inference_engine.is_model_trained and inference_engine.metadata:
            return inference_engine.metadata.get("model_id", "flood-v1-trained")
        return "v1.0-pending"

    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delegates to the official ML inference service.
        """
        raw_result = predict_flood_risk(features)

        # Map to backend schema format
        feature_importances = [
            {
                "factor_name": f["factor_name"],
                "factor_value": f["factor_value"],
                "importance": "High" if f["importance_rank"] <= 2 else "Medium",
                "unit": f.get("unit")
            }
            for f in raw_result.get("factors", [])
        ]

        return {
            "score": raw_result["risk_score"],
            "probability": raw_result["probability"],
            "risk_level": raw_result["risk_level"],
            "status": raw_result["status"],
            "model_version": raw_result["model_version"],
            "primary_driver": raw_result.get("primary_driver", "Catchment Precipitation Influx"),
            "recommended_immediate_action": raw_result.get("recommended_action", ""),
            "disclaimer": raw_result.get("disclaimer", "PROVISIONAL ASSESSMENT -- MODEL INTEGRATION PENDING"),
            "feature_importances": feature_importances
        }


FloodRiskModelPlaceholder = FloodRiskModelAdapter
flood_model = FloodRiskModelAdapter()
