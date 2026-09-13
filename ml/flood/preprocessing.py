"""
RISK // INDIA — Preprocessing Pipeline & Data Leakage Prevention
Reproducible scikit-learn ColumnTransformer & Event-Group Partitioning.
"""

from typing import Tuple, List, Dict, Any, Optional
import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.model_selection import GroupKFold

from ml.flood.config import (
    NUMERICAL_FEATURES,
    TARGET_COLUMN,
    GROUP_COLUMN,
)


def build_preprocessing_pipeline(
    numerical_features: Optional[List[str]] = None,
    scaler_type: str = "standard"
) -> ColumnTransformer:
    """
    Constructs a reproducible scikit-learn ColumnTransformer.
    
    - Numerical: Median imputation + StandardScaler (or RobustScaler).
    - Pipeline is fitted strictly on training data within cross-validation folds.
    """
    num_cols = numerical_features or NUMERICAL_FEATURES

    scaler = StandardScaler() if scaler_type == "standard" else RobustScaler(with_centering=True, with_scaling=True)

    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", scaler),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_pipeline, num_cols),
        ],
        remainder="drop",
        verbose_feature_names_out=False
    )

    return preprocessor


def create_event_group_kfold(
    df: pd.DataFrame,
    group_column: str = GROUP_COLUMN,
    n_splits: int = 5
) -> GroupKFold:
    """
    Configures a GroupKFold generator grouped by event_group_id to prevent multi-pass
    and intra-event temporal/spatial leakage across cross-validation folds.
    """
    unique_groups = df[group_column].nunique()
    actual_splits = min(n_splits, unique_groups)
    return GroupKFold(n_splits=actual_splits)
