# RISK // INDIA — Technical Documentation Index

This directory contains comprehensive technical reports, forensic audits, model governance cards, and operational documentation for the **RISK // INDIA** disaster risk intelligence prototype.

---

## 📑 Core Documentation Categories

### 1. Model Governance & Explainability
- [Assam Flood Model Card](assam_flood_model_card.md) — Official model card detailing architecture, training distribution, evaluation metrics, and operational limitations.
- [Flood Model Explainability](flood_model_explainability.md) — Mathematical formulation of standardized risk score outputs, logistic feature weights, and risk tier categorization.
- [Flood Feature Quality Report](flood_feature_quality_report.md) — Missing value audits, variance thresholds, correlation analysis, and temporal leakage verification.

### 2. Official Data Provenance & Ingestion
- [Flood Data Acquisition Report](flood_data_acquisition_report.md) — Ingestion protocols for CWC river level & rainfall telemetry, IMD precipitation records, and ISRO/NRSC Bhuvan inundation layers.
- [Data Forensic Verification](data_forensic_verification.md) — Multi-gauge synchronization, zero synthetic record guarantees, and physical sensor integrity audits.
- [Assam Flood Event Inventory](assam_flood_event_inventory.md) — Chronological inventory of verified flood waves (2021–2024) across Assam CWC monitoring stations.

### 3. Label Construction & Dataset Audits
- [Assam Flood Label Construction Report](assam_flood_label_construction_report.md) — Ground-truth label derivation methodology combining satellite inundation rasters and river stage thresholds.
- [Assam Flood Overlap Audit](assam_flood_overlap_audit.md) — Spatial overlap validation between CWC telemetry stations and satellite flood polygons.
- [Expanded Assam Dataset Forensic Audit](expanded_assam_dataset_forensic_audit.md) — Event group independence and GroupKFold cross-validation partitioning.

### 4. System Integration & Phase Audits
- [Phase 8: ML Prototype Report](phase_8_ml_prototype_report.md) — Training, cross-validation, and baseline benchmark comparisons (Logistic Regression vs Random Forest vs Gradient Boosting).
- [Phase 9: ML Integration Report](phase_9_ml_integration_report.md) — FastAPI model serving, frontend contracts, and inference pipeline integration.
- [Phase 10: Pilot Evaluation Report](phase_10_evaluation_report.md) — End-to-end evaluation across low, elevated, and high-risk scenarios.
- [Phase 11: Operational Intelligence](phase_11_operational_data_integration.md) — Live seismic feed integration (USGS) and official meteorological bulletin parsing.
- [Phase 12: Verified Help Ecosystem](phase_12_help_hub.md) — Emergency contact directory, relief camps, and NGO assistance registries.
- [Phase 13: Final Product Audit](phase_13_final_product_audit.md) — Comprehensive pre-release QA, security, and integrity audit.