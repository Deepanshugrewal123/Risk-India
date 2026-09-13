"""
RISK // INDIA — Model Evaluation Metrics for Disaster Risk Modeling

Calculates scientifically appropriate metrics for imbalanced disaster occurrence data:
- Precision, Recall, F1-Score (both binary positive class and macro-average)
- ROC-AUC & PR-AUC (Average Precision score)
- Complete Confusion Matrix (TP, FP, FN, TN)
- False Alarm (FPR) vs Missed Event (FNR) operational risk trade-off analysis
- Brier Score (probability calibration / probabilistic accuracy)
"""

from typing import Dict, Any, Union
import numpy as np
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    brier_score_loss,
)

def evaluate_binary_disaster_metrics(
    y_true: Union[np.ndarray, list],
    y_pred_proba: Union[np.ndarray, list],
    decision_threshold: float = 0.50
) -> Dict[str, Any]:
    """
    Computes comprehensive evaluation metrics for binary disaster event prediction.

    Parameters:
        y_true: Ground truth binary labels (0 = No Flood, 1 = Flood Occurrence).
        y_pred_proba: Predicted probabilities P(Flood = 1 | X).
        decision_threshold: Classification threshold for binary decisions (default 0.50).

    Returns:
        Structured dictionary of metrics, trade-offs, and operational diagnostics.
    """
    y_true_arr = np.asarray(y_true, dtype=int)
    y_prob_arr = np.asarray(y_pred_proba, dtype=float)
    y_pred_arr = (y_prob_arr >= decision_threshold).astype(int)

    total_samples = len(y_true_arr)
    positive_samples = int(np.sum(y_true_arr == 1))
    negative_samples = int(np.sum(y_true_arr == 0))
    event_prevalence = float(positive_samples / total_samples) if total_samples > 0 else 0.0

    # Confusion matrix extraction
    # tn, fp, fn, tp
    cm = confusion_matrix(y_true_arr, y_pred_arr, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()

    # Rates
    fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0  # False Positive Rate (False Alarm Rate)
    fnr = float(fn / (fn + tp)) if (fn + tp) > 0 else 0.0  # False Negative Rate (Miss Rate)

    # Standard classification metrics
    precision = float(precision_score(y_true_arr, y_pred_arr, zero_division=0))
    recall = float(recall_score(y_true_arr, y_pred_arr, zero_division=0))
    f1 = float(f1_score(y_true_arr, y_pred_arr, zero_division=0))
    f1_macro = float(f1_score(y_true_arr, y_pred_arr, average="macro", zero_division=0))

    # Curve AUC metrics (handle single-class edge cases gracefully)
    try:
        roc_auc = float(roc_auc_score(y_true_arr, y_prob_arr))
    except ValueError:
        roc_auc = float("nan")

    try:
        pr_auc = float(average_precision_score(y_true_arr, y_prob_arr))
    except ValueError:
        pr_auc = float("nan")

    # Probability calibration metric
    brier = float(brier_score_loss(y_true_arr, y_prob_arr))

    return {
        "dataset_statistics": {
            "total_samples": total_samples,
            "positive_events": positive_samples,
            "negative_events": negative_samples,
            "event_prevalence_pct": round(event_prevalence * 100, 2),
        },
        "classification_metrics": {
            "decision_threshold": decision_threshold,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "f1_macro": round(f1_macro, 4),
        },
        "probabilistic_and_ranking_metrics": {
            "roc_auc": round(roc_auc, 4) if not np.isnan(roc_auc) else None,
            "pr_auc": round(pr_auc, 4) if not np.isnan(pr_auc) else None,
            "brier_score": round(brier, 4),
            "calibration_commentary": "Lower Brier score (near 0) indicates superior probabilistic calibration.",
        },
        "confusion_matrix": {
            "true_negatives": int(tn),
            "false_positives": int(fp),
            "false_negatives": int(fn),
            "true_positives": int(tp),
        },
        "operational_risk_tradeoff": {
            "false_positive_rate_fpr": round(fpr, 4),
            "false_negative_rate_fnr": round(fnr, 4),
            "interpretation": (
                f"FPR ({round(fpr*100, 2)}% false alarms) vs FNR ({round(fnr*100, 2)}% missed floods). "
                "In humanitarian disaster management, FNR is heavily penalized because missed catastrophic "
                "floods result in loss of human life and unmitigated infrastructure collapse. "
                "However, excessive FPR causes warning fatigue and costly unwarranted evacuations."
            )
        }
    }
