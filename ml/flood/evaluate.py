"""
RISK // INDIA — Flood Model Evaluation & Baseline Benchmarking Suite

Executes rigorous scientific evaluation across candidate model families:
1. Baseline: Logistic Regression (L2 regularization, class-weighted)
2. Baseline: Random Forest Classifier (ensemble bagged trees)
3. Advanced: HistGradientBoostingClassifier (gradient-boosted decision trees)

Evaluates on:
- Imbalance-resilient metrics (PR-AUC, ROC-AUC, Brier score, Recall/Precision)
- Operational False Positive vs False Negative trade-off
- Out-of-region spatial transferability via GroupKFold
"""

from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.model_selection import cross_validate

from ml.common.metrics import evaluate_binary_disaster_metrics
from ml.flood.preprocessing import build_preprocessing_pipeline, create_spatial_group_kfold
from ml.flood.config import TARGET_COLUMN


def get_candidate_models() -> Dict[str, Any]:
    """
    Returns the 3 candidate baseline & advanced classification algorithms.
    """
    return {
        "logistic_regression": LogisticRegression(
            penalty="l2",
            C=1.0,
            class_weight="balanced",
            max_iter=1000,
            random_state=42
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=100,
            max_depth=8,
            class_weight="balanced_subsample",
            random_state=42,
            n_jobs=-1
        ),
        "hist_gradient_boosting": HistGradientBoostingClassifier(
            max_iter=150,
            max_depth=6,
            learning_rate=0.08,
            class_weight="balanced",
            random_state=42
        )
    }


def evaluate_model_pipeline(
    pipeline: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    decision_threshold: float = 0.50
) -> Dict[str, Any]:
    """
    Evaluates a trained model pipeline on held-out test data.
    """
    y_prob = pipeline.predict_proba(X_test)[:, 1]
    metrics = evaluate_binary_disaster_metrics(
        y_true=y_test.values,
        y_pred_proba=y_prob,
        decision_threshold=decision_threshold
    )
    return metrics


def benchmark_baseline_models(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series
) -> Dict[str, Any]:
    """
    Trains and benchmarks all 3 candidate models on identical temporal train/test sets.
    """
    candidates = get_candidate_models()
    benchmark_results = {}

    for name, estimator in candidates.items():
        preprocessor = build_preprocessing_pipeline()
        pipe = Pipeline([
            ("preprocessor", preprocessor),
            ("classifier", estimator)
        ])

        print(f"[*] Training and evaluating candidate model: {name}...")
        pipe.fit(X_train, y_train)
        eval_metrics = evaluate_model_pipeline(pipe, X_test, y_test)

        benchmark_results[name] = {
            "metrics": eval_metrics,
            "pipeline": pipe
        }

    return benchmark_results


def evaluate_spatial_transferability(
    pipeline: Pipeline,
    df: pd.DataFrame,
    group_column: str = "location_id",
    target_column: str = TARGET_COLUMN,
    n_splits: int = 5
) -> Dict[str, Any]:
    """
    Performs GroupKFold spatial cross-validation to assess how well the model
    generalizes to geographically unseen states/regions.
    """
    if group_column not in df.columns or target_column not in df.columns:
        return {"error": f"Required columns '{group_column}' or '{target_column}' missing."}

    X = df.drop(columns=[target_column])
    y = df[target_column]
    groups = df[group_column]

    gkf = create_spatial_group_kfold(df, group_column=group_column, n_splits=n_splits)

    scoring = ["roc_auc", "average_precision", "recall", "precision", "f1"]
    cv_res = cross_validate(
        pipeline,
        X,
        y,
        groups=groups,
        cv=gkf,
        scoring=scoring,
        error_score="raise",
        n_jobs=1
    )

    return {
        "group_column": group_column,
        "n_splits": gkf.get_n_splits(X, y, groups),
        "mean_roc_auc": round(float(np.mean(cv_res["test_roc_auc"])), 4),
        "mean_pr_auc": round(float(np.mean(cv_res["test_average_precision"])), 4),
        "mean_recall": round(float(np.mean(cv_res["test_recall"])), 4),
        "mean_precision": round(float(np.mean(cv_res["test_precision"])), 4),
        "mean_f1": round(float(np.mean(cv_res["test_f1"])), 4),
    }
