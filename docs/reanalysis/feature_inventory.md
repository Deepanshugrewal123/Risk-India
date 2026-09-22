# RISK // INDIA — Comprehensive Feature Inventory & Integration Matrix
## Mapping Backend Capabilities to Frontend Citizen Exposure

**Document:** `feature_inventory.md`  
**Classification:** Forensic System Re-Analysis  
**Authoritative Workspace:** `C:\Users\HP\Desktop\Risk Analyser`  

---

### 1. End-to-End Feature Integration Matrix

| Subsystem / Feature | Backend Implementation | REST API Endpoint | Frontend Service | UI Component / Exposure | Integration Status | Required Action |
| :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **National Predictive Overview** | `NationalPredictiveRiskFusionService` | `GET /api/predictive-risk/national` | `predictiveRiskService.getNationalOverview()` | `NationalFutureRisk.tsx` | **Partial** (Only inside Map tab) | **Expose prominent summary on HomePage** |
| **5-Horizon Future Risk Timeline** | `MultiHazardForecastEngine` + `timeline` | `GET /api/predictive-risk/{reg}/timeline` | `predictiveRiskService.getTimeline()` | `RiskForecastTimeline.tsx` | **Partial** (Hidden behind map click) | **Create Future Risk Hero directly on HomePage** |
| **Directional Trend (RISING/STABLE)** | `RiskTrendEngine` | `GET /api/predictive-risk/trends` | `predictiveRiskService.getTrends()` | `RiskTrendIndicator.tsx` | **Partial** | **Display trend on all hazard cards and search** |
| **Qualitative Confidence** | `QualitativeConfidenceEngine` | Inside assessment payload | `predictiveRiskService.getRegionalAssessment()` | `UncertaintyBadge.tsx` | **Partial** | **Purge fake % in AnalyzeArea; use LOW/MOD/HIGH** |
| **Qualitative Uncertainty** | `PredictiveUncertaintyEngine` | Inside assessment payload | `predictiveRiskService.getRegionalAssessment()` | `UncertaintyBadge.tsx` | **Partial** | **Display expanding uncertainty across horizons** |
| **Forward Scenarios (Baseline/Likely/Escalation)** | `ScenarioEngine` | `GET /api/predictive-risk/{reg}/scenarios` | `predictiveRiskService.getScenarios()` | `ScenarioPanel.tsx` | **Partial** (In Map tab) | **Link from homepage future risk section** |
| **Early Warning Decision Support** | `EarlyWarningEngine` | `GET /api/predictive-risk/{reg}/early-warning` | `predictiveRiskService.getEarlyWarning()` | `EarlyWarningPanel.tsx` | **Partial** (In Map tab) | **Prominent Early Warning Banner on HomePage** |
| **12 Citizen Safety Questions** | `PredictionExplanationEngine` | `GET /api/predictive-risk/{reg}/explanation` | `predictiveRiskService.getExplanation()` | `RiskExplanationCard.tsx` | **Partial** (In Map tab) | **Expose in location-first checker on HomePage** |
| **Location Risk Analysis** | `riskService.analyzeArea()` | `POST /api/risk/analyze` | `riskService.analyzeArea()` | `AnalyzeAreaSection.tsx` | **FLAWED** | **Purge demo mock (`isDemoData: true`); wire to live fusion** |
| **Assam Flood ML Prototype** | `flood_model_service` (Random Forest) | `GET /api/risk/predict/flood` | `riskService.predictFlood()` | Risk Explanation modals | **Operational** | **Preserve hash integrity (0e05bcdf...)** |
| **Non-Assam ML Scope Guard** | Hard-coded `ml_available = False` | Evaluated in all routes | `ml_scope` | `PredictionScopeNotice.tsx` | **Operational** | **Expose clear transparency notice** |
| **Earthquake Non-Prediction Guard** | Hard-coded `is_predictable = False` | Evaluated in all routes | `hazard == 'EARTHQUAKE'` | `PredictionScopeNotice.tsx` | **Operational** | **Preserve disclaimer; no future prediction** |
| **Live Synoptic Weather** | `national_weather_service` | `GET /api/weather/current` | `weatherService.getCurrentWeather()` | `WeatherStatusCard.tsx` | **Disconnected** | **Incorporate into Location Checker** |
| **NWP Weather Forecasts** | `national_weather_service` | `GET /api/weather/forecast` | `weatherService.getForecasts()` | `WeatherForecastTimeline.tsx` | **Disconnected** | **Corroborate in Future Risk Hero** |
| **Statutory Weather Warnings** | `national_weather_service` | `GET /api/weather/warnings` | `weatherService.getWarnings()` | `WeatherWarningCard.tsx` | **Disconnected** | **Display in Early Warning section** |
| **Dynamic CWC River Telemetry** | `dynamic_telemetry_service` | `GET /api/telemetry/observations` | `apiClient.get('/api/telemetry/...')` | None (Backend only) | **Disconnected** | **Expose river danger ratios in Flood cards** |
| **National Crisis Mode** | `national_crisis_service` | `GET /api/crisis/*` | `crisisService.*` | `CrisisDashboard.tsx`, `CrisisRecommendedBanner.tsx` | **Operational** | **Keep active for critical threshold triggers** |
| **Verified Emergency Helplines** | `CrisisResourceEngine` | `GET /api/crisis/{reg}/resources` | `crisisService.getResources()` | `EmergencyAccessHub.tsx` | **Operational** | **Add mandatory fallback note everywhere** |
| **Interactive Risk Map** | `IndiaRiskMap.tsx` | Combined endpoints | `riskService.getAllRegions()` | `RiskMapPage.tsx` | **Needs Betterment** | **Add Mode Selector: Current vs Future vs Early Warning** |

---

### 2. Summary of Key Disconnects

1. **The Disconnected Modern Backend**:
   - `predictiveRiskService` has 10 powerful methods.
   - `weatherService` has 6 methods.
   - `dynamic_telemetry_service` provides live CWC river gauge data.
   - **Yet the homepage was almost completely decoupled from these services**, relying instead on the older `LiveRiskSnapshot` and an outdated `AnalyzeAreaSection` that still had simulated fallback flags from an earlier prototype phase.
2. **Missing Citizen Entry Point for Future Risk**:
   - A user who wants to know *"What could happen in my district tomorrow?"* had to click "Explore Risk Map", notice a small toggle, and navigate tabs.
   - The primary call-to-action on the homepage must directly answer: *"What could happen next in your area?"*
