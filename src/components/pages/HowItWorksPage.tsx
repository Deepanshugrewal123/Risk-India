import React from 'react';
import { Database, Cpu, Compass, HeartHandshake, ShieldCheck, Code, Layers, Server, Sparkles, ArrowRight } from 'lucide-react';
import { MagneticButton } from '../common/MagneticButton';

interface HowItWorksPageProps {
  onAnalyzeArea: () => void;
  onExploreMap: () => void;
}

export const HowItWorksPage: React.FC<HowItWorksPageProps> = ({
  onAnalyzeArea,
  onExploreMap,
}) => {
  return (
    <div className="pt-28 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto min-h-screen">
      {/* Header */}
      <div className="text-center max-w-3xl mx-auto mb-16">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-paper-200 border border-paper-300 text-charcoal-700 text-xs font-mono font-semibold mb-4">
          <Layers className="w-3.5 h-3.5" />
          <span>TECHNICAL ARCHITECTURE BLUEPRINT</span>
        </div>
        <h1 className="text-4xl sm:text-6xl font-bold tracking-tight text-charcoal-950 mb-4">
          Engineering India's Next-Gen Disaster AI.
        </h1>
        <p className="text-base sm:text-lg text-charcoal-600 leading-relaxed">
          How RISK//INDIA transforms complex geospatial, meteorological, and telemetry streams into zero-delay life safety intelligence.
        </p>
      </div>

      {/* 4 Architectural Pillars */}
      <div className="space-y-12 mb-20">
        {/* Pillar 1 */}
        <div className="rounded-3xl bg-white border border-paper-300 p-8 sm:p-12 shadow-subtle grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          <div className="lg:col-span-6 space-y-4">
            <div className="flex items-center gap-2">
              <span className="w-8 h-8 rounded-xl bg-charcoal-900 text-paper-50 flex items-center justify-center font-mono font-bold text-sm">
                01
              </span>
              <span className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-semibold">
                Telemetry & Ingestion Layer
              </span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-charcoal-950">
              Multimodal Sensor & Satellite Data Feeds
            </h2>
            <p className="text-sm text-charcoal-600 leading-relaxed">
              Synthesizes real-time telemetry from Central Water Commission (CWC) river gauges, India Meteorological Department (IMD) Doppler radar meshes, INSAT-3DR thermal infrared imagery, and National Center for Seismology (NCS) accelerometer stations.
            </p>
            <div className="flex flex-wrap gap-2 pt-2">
              <span className="px-3 py-1 rounded-full bg-paper-100 text-charcoal-700 font-mono text-xs border border-paper-200">
                • CWC Hydro-telemetry
              </span>
              <span className="px-3 py-1 rounded-full bg-paper-100 text-charcoal-700 font-mono text-xs border border-paper-200">
                • IMD Radar & Rainfall Grids
              </span>
              <span className="px-3 py-1 rounded-full bg-paper-100 text-charcoal-700 font-mono text-xs border border-paper-200">
                • GSI Landslide Susceptibility Index
              </span>
            </div>
          </div>

          <div className="lg:col-span-6 bg-paper-50 rounded-2xl p-6 border border-paper-200 font-mono text-xs space-y-3">
            <div className="text-charcoal-400 text-[11px] uppercase tracking-wider border-b border-paper-200 pb-2 flex justify-between">
              <span>Telemetry Ingestion Pipeline</span>
              <span className="text-emerald-600">Active Telemetry Stream</span>
            </div>
            <div className="text-charcoal-800 space-y-1.5">
              <div><span className="text-charcoal-400">&gt;</span> GET /api/v1/telemetry/gauge/brahmaputra</div>
              <div className="text-charcoal-500 pl-4">{`{ river_stage_m: 49.38, danger_level: 48.00, status: "BREACH_WARN" }`}</div>
              <div><span className="text-charcoal-400">&gt;</span> GET /api/v1/telemetry/soil/mandi-nh21</div>
              <div className="text-charcoal-500 pl-4">{`{ pore_pressure_kpa: 142.8, shear_stability_factor: 0.88 }`}</div>
              <div><span className="text-charcoal-400">&gt;</span> GET /api/v1/radar/bay-of-bengal/vortex</div>
              <div className="text-charcoal-500 pl-4">{`{ central_pressure_hpa: 988, wind_gust_kmh: 105 }`}</div>
            </div>
          </div>
        </div>

        {/* Pillar 2 */}
        <div className="rounded-3xl bg-white border border-paper-300 p-8 sm:p-12 shadow-subtle grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          <div className="lg:col-span-6 order-2 lg:order-1 bg-paper-50 rounded-2xl p-6 border border-paper-200 font-mono text-xs space-y-3">
            <div className="text-charcoal-400 text-[11px] uppercase tracking-wider border-b border-paper-200 pb-2 flex justify-between">
              <span>National ML Intelligence Pipeline</span>
              <span className="text-emerald-700 font-bold">risk_india_flood_v1 Active</span>
            </div>
            <div className="text-charcoal-800 space-y-1.5">
              <div><span className="text-charcoal-400">Deployed Model:</span> RISK // INDIA Flood Model v1 (GradientBoostingClassifier)</div>
              <div><span className="text-charcoal-400">Observational Base:</span> 18,184 Empirical IMD District Records across 38 States/UTs</div>
              <div><span className="text-charcoal-400">River Basin Coverage:</span> All 12 Major Indian River Basins (Ganga, Brahmaputra, Mahanadi, Godavari, Krishna, etc.)</div>
              <div><span className="text-charcoal-400">Target Science:</span> Compound Hydrological Inundation (Distinguishes Rain-Only from Inundation)</div>
              <div><span className="text-charcoal-400">Multi-Hazard Fusion:</span> IMD NWP Forecasts, CWC River Basins, NDMA Baselines, GSI LEWS</div>
              <div><span className="text-charcoal-400">Earthquake Guard:</span> Non-Predictable Invariant Enforced (BIS IS 1893:2016)</div>
              <div className="p-2 rounded bg-paper-100 border border-paper-200 text-[11px] text-charcoal-600">
                Pan-India Empirical Flood Model: 100% Observational Data • Zero Synthetic Telemetry
              </div>
            </div>
          </div>

          <div className="lg:col-span-6 order-1 lg:order-2 space-y-4">
            <div className="flex items-center gap-2">
              <span className="w-8 h-8 rounded-xl bg-charcoal-900 text-paper-50 flex items-center justify-center font-mono font-bold text-sm">
                02
              </span>
              <span className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-semibold">
                Empirical ML &amp; Multi-Source Fusion
              </span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-charcoal-950">
              RISK // INDIA Flood Model v1 — India-Wide Empirical Flood Intelligence
            </h2>
            <p className="text-sm text-charcoal-600 leading-relaxed">
              RISK // INDIA combines an India-wide empirical machine learning flood engine with authoritative multi-source operational fusion. The deployed <code className="font-mono font-bold bg-paper-100 px-1 py-0.5 rounded border border-paper-200">risk_india_flood_v1</code> model evaluates compound inundation risk across all 28 States and 8 Union Territories by processing acute rainfall surges against antecedent catchment saturation and river basin vulnerability with zero synthetic records.
            </p>
            <div className="flex flex-wrap gap-2 pt-2">
              <span className="px-3 py-1 rounded-full bg-paper-100 text-charcoal-700 font-mono text-xs border border-paper-200">
                • 18,184 Empirical Observations
              </span>
              <span className="px-3 py-1 rounded-full bg-paper-100 text-charcoal-700 font-mono text-xs border border-paper-200">
                • All 12 Major Indian River Basins
              </span>
              <span className="px-3 py-1 rounded-full bg-paper-100 text-charcoal-700 font-mono text-xs border border-paper-200">
                • Zero Synthetic Data
              </span>
            </div>
          </div>
        </div>

        {/* Pillar 3 */}
        <div className="rounded-3xl bg-white border border-paper-300 p-8 sm:p-12 shadow-subtle grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          <div className="lg:col-span-6 space-y-4">
            <div className="flex items-center gap-2">
              <span className="w-8 h-8 rounded-xl bg-charcoal-900 text-paper-50 flex items-center justify-center font-mono font-bold text-sm">
                03
              </span>
              <span className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-semibold">
                Human-Centered Preparedness
              </span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-charcoal-950">
              Contextual Citizen Advisory &amp; Preparedness Intelligence
            </h2>
            <p className="text-sm text-charcoal-600 leading-relaxed">
              Converts complex probabilistic predictions into immediate, non-alarmist human action plans. The conversational assistant provides answers in local contexts—such as preparing livestock in floodplains or securing roofs during cyclonic depressions.
            </p>
            <div className="flex flex-wrap gap-2 pt-2">
              <span className="px-3 py-1 rounded-full bg-paper-100 text-charcoal-700 font-mono text-xs border border-paper-200">
                • Before / During / After Guides
              </span>
              <span className="px-3 py-1 rounded-full bg-paper-100 text-charcoal-700 font-mono text-xs border border-paper-200">
                • Offline Card Generators
              </span>
              <span className="px-3 py-1 rounded-full bg-paper-100 text-charcoal-700 font-mono text-xs border border-paper-200">
                • Low-Bandwidth Optimization
              </span>
            </div>
          </div>

          <div className="lg:col-span-6 bg-paper-50 rounded-2xl p-6 border border-paper-200 font-mono text-xs space-y-3">
            <div className="text-charcoal-400 text-[11px] uppercase tracking-wider border-b border-paper-200 pb-2 flex justify-between">
              <span>Production API &amp; Client Architecture</span>
              <span className="text-emerald-700 font-bold">FastAPI / REST / TLS</span>
            </div>
            <div className="text-charcoal-800 space-y-1.5">
              <div><span className="text-charcoal-400">Flood ML Inference:</span> POST /api/risk/analyze &bull; risk_india_flood_v1</div>
              <div><span className="text-charcoal-400">Future Risk Horizons:</span> GET /api/future-risk/{'{state}'} (5 Lead Windows)</div>
              <div><span className="text-charcoal-400">Cascading Perils DAG:</span> GET /api/cascading/evaluate (5-Stage Propagation)</div>
              <div><span className="text-charcoal-400">Offline Resilience:</span> IndexedDB caching with graceful regional baseline fallback</div>
              <div><span className="text-charcoal-400">Statutory Grounding:</span> NDMA, IMD, CWC, GSI, and BIS IS 1893:2016</div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Call to Action */}
      <div className="rounded-3xl bg-charcoal-900 text-paper-50 p-8 sm:p-14 text-center">
        <h2 className="text-2xl sm:text-4xl font-bold mb-3">
          Explore the Interactive Live Platform
        </h2>
        <p className="text-xs sm:text-sm text-charcoal-400 max-w-xl mx-auto mb-8">
          Test the interactive India risk map or evaluate risk levels for your district.
        </p>
        <div className="flex flex-wrap items-center justify-center gap-4">
          <MagneticButton
            variant="secondary"
            size="lg"
            onClick={onAnalyzeArea}
          >
            Analyze Area Risk
          </MagneticButton>
          <MagneticButton
            variant="ghost"
            size="lg"
            onClick={onExploreMap}
            className="text-white hover:bg-white/10"
          >
            Open Risk Map
          </MagneticButton>
        </div>
      </div>
    </div>
  );
};
