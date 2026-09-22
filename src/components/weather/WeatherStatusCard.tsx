import React from 'react';
import { WeatherSubsystemStatus } from '../../types/weather';
import { CloudRain, ShieldCheck, Activity, Radio, AlertTriangle } from 'lucide-react';

interface WeatherStatusCardProps {
  status: WeatherSubsystemStatus | null;
  loading?: boolean;
}

export const WeatherStatusCard: React.FC<WeatherStatusCardProps> = ({ status, loading }) => {
  if (loading) {
    return (
      <div className="p-6 bg-white border border-gray-200 rounded-2xl animate-pulse">
        <div className="h-6 w-48 bg-gray-200 rounded mb-4" />
        <div className="h-4 w-64 bg-gray-100 rounded" />
      </div>
    );
  }

  if (!status) return null;

  return (
    <div className="p-6 bg-white border border-gray-200 rounded-2xl shadow-sm space-y-6">
      <div className="flex items-start justify-between">
        <div>
          <div className="flex items-center gap-2">
            <CloudRain className="w-5 h-5 text-blue-600" />
            <h3 className="text-lg font-bold text-gray-900 tracking-tight">
              National Weather Intelligence
            </h3>
          </div>
          <p className="text-xs text-gray-500 mt-1 font-mono">
            Subsystem: {status.subsystem} // {status.backend_storage}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
            <Activity className="w-3.5 h-3.5" />
            {status.status}
          </span>
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200 font-mono">
            <ShieldCheck className="w-3.5 h-3.5" />
            0 SYNTHETIC
          </span>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="p-3 bg-gray-50 rounded-xl border border-gray-100">
          <div className="text-xs font-medium text-gray-500">Monitored Entities</div>
          <div className="text-2xl font-bold text-gray-900 mt-1">{status.entities_monitored}</div>
          <div className="text-[10px] text-gray-400 mt-0.5">28 States + 8 UTs</div>
        </div>
        <div className="p-3 bg-gray-50 rounded-xl border border-gray-100">
          <div className="text-xs font-medium text-gray-500">Synoptic Observations</div>
          <div className="text-2xl font-bold text-gray-900 mt-1">{status.total_observations_ingested}</div>
          <div className="text-[10px] text-emerald-600 mt-0.5">Surface Telemetry Ingested</div>
        </div>
        <div className="p-3 bg-gray-50 rounded-xl border border-gray-100">
          <div className="text-xs font-medium text-gray-500">Forecast Horizontals</div>
          <div className="text-2xl font-bold text-gray-900 mt-1">{status.total_forecasts_managed}</div>
          <div className="text-[10px] text-blue-600 mt-0.5">Multi-Horizon Predictions</div>
        </div>
        <div className="p-3 bg-gray-50 rounded-xl border border-gray-100">
          <div className="text-xs font-medium text-gray-500">Active Warnings</div>
          <div className="text-2xl font-bold text-gray-900 mt-1">{status.total_active_warnings}</div>
          <div className="text-[10px] text-amber-600 mt-0.5">Official IMD Bulletins</div>
        </div>
      </div>

      {/* Provider Circuits */}
      <div>
        <div className="text-xs font-semibold text-gray-700 uppercase tracking-wider mb-2 flex items-center gap-1.5">
          <Radio className="w-3.5 h-3.5 text-gray-500" />
          Authoritative Provider Feeds
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
          {Object.entries(status.provider_circuits).map(([provider, info]) => (
            <div key={provider} className="p-2.5 bg-gray-50 rounded-lg border border-gray-100 text-xs">
              <div className="font-semibold text-gray-800 truncate">{provider}</div>
              <div className="flex items-center justify-between mt-1 text-[11px]">
                <span className={info.healthy ? "text-emerald-600 font-medium" : "text-amber-600 font-medium"}>
                  {info.state}
                </span>
                <span className="text-gray-400 font-mono">{info.latency_ms.toFixed(0)}ms</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
