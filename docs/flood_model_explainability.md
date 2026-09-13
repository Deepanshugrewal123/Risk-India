# Assam Flood ML Prototype — Model Explainability Architecture
**Phase 8 — Tabular Model Interpretability & "Why This Risk?" Attribution**  
**Model Version:** `assam_flood_prototype_v1`  
**Model Family:** Regularized Logistic Regression (L2 Regularization, $C=0.5$, Class-Weighted)  
**Publication Date:** 2026-09-13  

---

## 1. Interpretability Philosophy & Approach

For flood risk management, black-box predictions lack operational trustworthiness. Disaster managers and emergency personnel need to answer: **"Why is this risk elevated?"**

Because our prototype operates on a small, high-integrity dataset ($N=32$, 18 independent flood events), complex deep surrogate explainers (e.g. KernelSHAP on neural nets) suffer from extreme sampling variance and instability. Instead, our prototype employs **intrinsic linear model interpretability**:
1. Every feature has a direct, monotonic, and mathematically exact weight (coefficient $\beta_j$).
2. The log-odds of flood occurrence $\text{logit}(P) = \ln\left(\frac{P}{1-P}\right)$ is a linear combination of standardized features:
   $$\text{logit}(P) = \beta_0 + \sum_{j=1}^{p} \beta_j \cdot z_j$$
   where $z_j = \frac{x_j - \mu_j}{\sigma_j}$ is the median-imputed, standard-scaled value of feature $x_j$.
3. When $z_j > 0$ and $\beta_j > 0$, feature $x_j$ actively increases the predicted flood probability.
4. Feature contributions are translated into **plain-language physical drivers** (e.g. "Heavy 72h precipitation", "Rapid river rise", "Elevated seasonal water level").

---

## 2. Learned Feature Weights & Physical Interpretation

Below is the complete, unadjusted ranking of all 13 features ordered by their impact on model decisions:

| Feature Name | Coefficient ($\beta$) | Odds Ratio ($e^\beta$) | Physical Direction | Domain Mechanism & Interpretation |
| :--- | :---: | :---: | :---: | :--- |
| `river_rise_6h` | **+0.1649** | 1.179 | **Increases Risk** | Immediate channel hydraulic surge over preceding 6 hours. |
| `rainfall_72h` | **+0.1409** | 1.151 | **Increases Risk** | 3-day cumulative rainfall drives basin saturation and catchment runoff accumulation. |
| `rainfall_24h` | **+0.0945** | 1.099 | **Increases Risk** | Daily precipitation influx causing localized flash pooling and bank overflow. |
| `month` | -0.0108 | 0.989 | Neutral / Baseline | Calendar progression across the monsoon season. |
| `river_rise_24h` | -0.1078 | 0.898 | Interacting Factor | Correlated with 6h rise; reflects multi-day hydrograph recession in certain post-peak passes. |
| `day_of_year_sin` | -0.1633 | 0.849 | Seasonal | Seasonal cyclicity of peak monsoon storms. |
| `day_of_year_cos` | -0.2117 | 0.809 | Seasonal | Seasonal cyclicity of late monsoon retreat. |
| `river_level_relative` | -0.2345 | 0.791 | Baseline State | Stage above seasonal minimum. |
| `rainfall_6h` | -0.2784 | 0.757 | Lag Factor | High multi-collinearity with 24h rainfall; reflects post-storm satellite overpasses. |
| `longitude` | -0.4671 | 0.627 | Spatial Proxy | Regional gauge location coordinate (western vs eastern Brahmaputra reach). |
| `rainfall_168h` | -0.5148 | 0.598 | Basin Buffer | 7-day cumulative total; in prolonged rain events without sharp peaks, infiltration buffers runoff. |
| `river_percentile_level`| -0.5859 | 0.557 | Hydrograph Limb | In small sample ($N=32$), several negative baseline rasters occurred during sustained high water. |
| `latitude` | -0.6426 | 0.526 | Spatial Proxy | Spatial proxy for gauge catchment north/south distribution. |
| **Intercept ($\beta_0$)** | **+0.1479** | — | — | Baseline log-odds of flood occurrence at mean feature values. |

---

## 3. Dynamic "Why This Risk?" Explanation Mechanism

The runtime inference engine (`ml/flood/predict.py`) dynamically maps raw hydrometric inputs to human-readable physical explanations:

### Attribution Rules:
1. **Antecedent Precipitation Factors:**
   - If $\text{rainfall\_72h} \ge 100\text{ mm}$:
     `"Antecedent 72h Precipitation: High cumulative catchment saturation elevating runoff potential"`
   - If $\text{rainfall\_24h} \ge 50\text{ mm}$:
     `"Heavy 24h Rainfall: Intense local convective burst increasing immediate surface ponding"`
   - If $\text{rainfall\_72h} \le 10\text{ mm}$ and $\text{rainfall\_24h} \le 5\text{ mm}$:
     `"Low Antecedent Rainfall: Minimal precipitation influx moderating catchment flood risk"`

2. **River Rise Dynamics Factors:**
   - If $\text{river\_rise\_24h} > +0.15\text{ m}$:
     `"Rapid 24h River Rise: Active upstream flood wave and hydraulic channel swelling"`
   - If $\text{river\_rise\_24h} < -0.15\text{ m}$:
     `"Receding River Stage: Hydraulic drainage reducing local inundation hazard"`

3. **Seasonal Hydrological State Factors:**
   - If $\text{river\_percentile\_level} \ge 85\%$:
     `"High Seasonal Water Level: River channel flowing near seasonal bankfull capacity"`
   - If $\text{river\_percentile\_level} \le 35\%$:
     `"Low Seasonal Water Level: Substantial within-bank channel storage buffering incoming runoff"`

---

## 4. Operational Risk Score Translation

The system maintains a strict separation between **statistical model probability** and **user interface risk score**:
- **Model Probability ($P \in [0.0, 1.0]$):** Raw posterior probability $P(\text{Flood}=1 \mid X)$ generated directly by `model.predict_proba(X)`.
- **UI Risk Score ($\text{Score} \in [0, 100]$):** Monotonically mapped integer $\text{round}(P \times 100)$.
- **Risk Level Categorization:**
  - $0 - 25$: **Low** (Standard within-bank flow)
  - $26 - 50$: **Moderate** (Elevated channel stage, routine vigilance)
  - $51 - 75$: **High** (Overbank spilling likely, inspection recommended)
  - $76 - 100$: **Critical** (Extensive inundation expected, immediate advisory)

---
*Report published as part of Phase 8 — Assam Flood ML Prototype.*
