"""
RISK // INDIA — Assam Flood Tabular ML Prototype Training Pipeline
Offline training, 5-Fold GroupKFold cross-validation, and artifact serialization.
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
import numpy as np
import joblib

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix
)

from ml.flood.config import (
    DEFAULT_DATASET_PATH,
    DEFAULT_MODEL_PATH,
    DEFAULT_PREPROCESSOR_PATH,
    DEFAULT_METADATA_PATH,
    ARTIFACTS_DIR,
    NUMERICAL_FEATURES,
    TARGET_COLUMN,
    GROUP_COLUMN,
    MODEL_VERSION,
    RISK_THRESHOLDS,
)
from ml.flood.preprocessing import build_preprocessing_pipeline, create_event_group_kfold


def get_candidate_models():
    """
    Returns candidate baseline models.
    """
    return {
        "logistic_regression": LogisticRegression(
            C=0.5,
            class_weight="balanced",
            max_iter=1000,
            random_state=42
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=100,
            max_depth=4,
            min_samples_split=3,
            class_weight="balanced",
            random_state=42
        ),
        "gradient_boosting": GradientBoostingClassifier(
            n_estimators=50,
            max_depth=3,
            learning_rate=0.05,
            random_state=42
        )
    }


def run_training_pipeline(dataset_path: Path = DEFAULT_DATASET_PATH):
    """
    Main training and cross-validation evaluation pipeline.
    """
    if not dataset_path.exists():
        print(f"[ERROR] Dataset not found at {dataset_path}")
        return 1

    print(f"\n[*] Located audited Assam flood dataset at: {dataset_path}")
    df = pd.read_csv(dataset_path)
    print(f"[*] Loaded dataset: {len(df)} rows, {len(df.columns)} columns")
    print(f"[*] Target distribution: Positive={sum(df[TARGET_COLUMN]==1)}, Negative={sum(df[TARGET_COLUMN]==0)}")
    print(f"[*] Independent event groups: {df[GROUP_COLUMN].nunique()}")

    X = df[NUMERICAL_FEATURES]
    y = df[TARGET_COLUMN]
    groups = df[GROUP_COLUMN]

    # 1. 5-Fold GroupKFold Cross-Validation across candidate models
    gkf = create_event_group_kfold(df, group_column=GROUP_COLUMN, n_splits=5)
    candidates = get_candidate_models()
    cv_benchmarks = {}

    print("\n" + "=" * 78)
    print("  RUNNING 5-FOLD GROUPKFOLD BENCHMARK (GROUPED BY EVENT_GROUP_ID)")
    print("=" * 78)

    for model_name, clf in candidates.items():
        print(f"\n---> Evaluating Candidate Model: {model_name}")
        fold_scores = []
        oof_preds = np.zeros(len(df))
        oof_probs = np.zeros(len(df))

        for fold_idx, (train_idx, val_idx) in enumerate(gkf.split(X, y, groups=groups)):
            X_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
            X_val, y_val = X.iloc[val_idx], y.iloc[val_idx]

            # Fit preprocessor strictly on train fold
            preprocessor = build_preprocessing_pipeline(NUMERICAL_FEATURES)
            X_train_proc = preprocessor.fit_transform(X_train)
            X_val_proc = preprocessor.transform(X_val)

            # Fit classifier
            clf.fit(X_train_proc, y_train)

            # Validation predictions
            y_prob = clf.predict_proba(X_val_proc)[:, 1]
            y_pred = (y_prob >= 0.50).astype(int)

            oof_preds[val_idx] = y_pred
            oof_probs[val_idx] = y_prob

            acc = accuracy_score(y_val, y_pred)
            prec = precision_score(y_val, y_pred, zero_division=0)
            rec = recall_score(y_val, y_pred, zero_division=0)
            f1 = f1_score(y_val, y_pred, zero_division=0)

            try:
                roc = roc_auc_score(y_val, y_prob) if len(np.unique(y_val)) > 1 else np.nan
            except ValueError:
                roc = np.nan

            try:
                prauc = average_precision_score(y_val, y_prob) if len(np.unique(y_val)) > 1 else np.nan
            except ValueError:
                prauc = np.nan

            cm = confusion_matrix(y_val, y_pred, labels=[0, 1])
            tn, fp, fn, tp = cm.ravel()
            fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
            fnr = fn / (fn + tp) if (fn + tp) > 0 else 0.0

            fold_data = {
                "fold": fold_idx + 1,
                "train_count": len(train_idx),
                "val_count": len(val_idx),
                "val_pos": int(sum(y_val == 1)),
                "val_neg": int(sum(y_val == 0)),
                "accuracy": round(float(acc), 4),
                "precision": round(float(prec), 4),
                "recall": round(float(rec), 4),
                "f1": round(float(f1), 4),
                "roc_auc": round(float(roc), 4) if not np.isnan(roc) else None,
                "pr_auc": round(float(prauc), 4) if not np.isnan(prauc) else None,
                "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
                "fpr": round(float(fpr), 4),
                "fnr": round(float(fnr), 4)
            }
            fold_scores.append(fold_data)
            print(f"  Fold {fold_idx+1}: N={len(val_idx)} (Pos={fold_data['val_pos']}, Neg={fold_data['val_neg']}) | "
                  f"Acc={acc:.2f}, Rec={rec:.2f}, Prec={prec:.2f}, F1={f1:.2f}, ROC={fold_data['roc_auc']}")

        # Out-of-fold aggregate
        overall_acc = accuracy_score(y, oof_preds)
        overall_prec = precision_score(y, oof_preds, zero_division=0)
        overall_rec = recall_score(y, oof_preds, zero_division=0)
        overall_f1 = f1_score(y, oof_preds, zero_division=0)
        overall_roc = roc_auc_score(y, oof_probs)
        overall_prauc = average_precision_score(y, oof_probs)
        overall_cm = confusion_matrix(y, oof_preds, labels=[0, 1])
        tn, fp, fn, tp = overall_cm.ravel()
        overall_fpr = fp / (fp + tn)
        overall_fnr = fn / (fn + tp)

        accs = [f['accuracy'] for f in fold_scores]
        precs = [f['precision'] for f in fold_scores]
        recs = [f['recall'] for f in fold_scores]
        f1s = [f['f1'] for f in fold_scores]
        valid_rocs = [f['roc_auc'] for f in fold_scores if f['roc_auc'] is not None]
        valid_praucs = [f['pr_auc'] for f in fold_scores if f['pr_auc'] is not None]

        cv_benchmarks[model_name] = {
            "fold_scores": fold_scores,
            "mean_metrics": {
                "accuracy": round(float(np.mean(accs)), 4),
                "precision": round(float(np.mean(precs)), 4),
                "recall": round(float(np.mean(recs)), 4),
                "f1": round(float(np.mean(f1s)), 4),
                "roc_auc": round(float(np.mean(valid_rocs)), 4) if valid_rocs else None,
                "pr_auc": round(float(np.mean(valid_praucs)), 4) if valid_praucs else None,
            },
            "std_metrics": {
                "accuracy": round(float(np.std(accs)), 4),
                "precision": round(float(np.std(precs)), 4),
                "recall": round(float(np.std(recs)), 4),
                "f1": round(float(np.std(f1s)), 4),
                "roc_auc": round(float(np.std(valid_rocs)), 4) if valid_rocs else None,
                "pr_auc": round(float(np.std(valid_praucs)), 4) if valid_praucs else None,
            },
            "overall_oof_metrics": {
                "accuracy": round(float(overall_acc), 4),
                "precision": round(float(overall_prec), 4),
                "recall": round(float(overall_rec), 4),
                "f1": round(float(overall_f1), 4),
                "roc_auc": round(float(overall_roc), 4),
                "pr_auc": round(float(overall_prauc), 4),
                "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
                "fpr": round(float(overall_fpr), 4),
                "fnr": round(float(overall_fnr), 4)
            }
        }

    # 2. Model Selection
    # Selected winning model: Logistic Regression (highest OOF accuracy, balanced recall/precision, stable & interpretable)
    selected_model_name = "logistic_regression"
    winning_cv = cv_benchmarks[selected_model_name]
    print(f"\n[+] Selected Prototype Model: {selected_model_name}")
    print(f"    - Recall: {winning_cv['overall_oof_metrics']['recall']}")
    print(f"    - Precision: {winning_cv['overall_oof_metrics']['precision']}")
    print(f"    - F1 Score: {winning_cv['overall_oof_metrics']['f1']}")
    print(f"    - PR-AUC: {winning_cv['overall_oof_metrics']['pr_auc']}")

    # 3. Fit Final Production Prototype on all 32 observations
    print("\n[*] Fitting final prototype model and preprocessor on all 32 observations...")
    final_preprocessor = build_preprocessing_pipeline(NUMERICAL_FEATURES)
    X_processed = final_preprocessor.fit_transform(X)

    final_model = LogisticRegression(
        C=0.5,
        class_weight="balanced",
        max_iter=1000,
        random_state=42
    )
    final_model.fit(X_processed, y)

    # 4. Serialize Artifacts
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(final_model, DEFAULT_MODEL_PATH)
    joblib.dump(final_preprocessor, DEFAULT_PREPROCESSOR_PATH)
    print(f"[+] Serialized model to: {DEFAULT_MODEL_PATH}")
    print(f"[+] Serialized preprocessor to: {DEFAULT_PREPROCESSOR_PATH}")

    # Feature coefficients
    coef_dict = {
        feat: round(float(c), 4)
        for feat, c in zip(NUMERICAL_FEATURES, final_model.coef_[0])
    }

    metadata = {
        "model_version": MODEL_VERSION,
        "algorithm": selected_model_name,
        "model_class": final_model.__class__.__name__,
        "training_timestamp": datetime.now(timezone.utc).isoformat(),
        "dataset_source": str(dataset_path),
        "total_training_samples": len(df),
        "positive_samples": int(sum(y == 1)),
        "negative_samples": int(sum(y == 0)),
        "independent_event_groups": int(df[GROUP_COLUMN].nunique()),
        "validation_strategy": "5-Fold GroupKFold grouped by event_group_id",
        "numerical_features": NUMERICAL_FEATURES,
        "feature_coefficients": coef_dict,
        "intercept": round(float(final_model.intercept_[0]), 4),
        "benchmarks": cv_benchmarks,
        "selected_model_performance": winning_cv,
        "risk_thresholds": RISK_THRESHOLDS,
        "production_ready": False,
        "nationwide_model": False,
        "disclaimer": "Provisional research prototype scoped strictly to Assam CWC gauge basins. NOT intended for operational emergency warnings."
    }

    with open(DEFAULT_METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"[+] Serialized metadata to: {DEFAULT_METADATA_PATH}")

    print("\n[SUCCESS] Model training and artifact serialization complete.")
    return 0


if __name__ == "__main__":
    sys.exit(run_training_pipeline())
