import React from 'react';
import { WeatherForecast } from '../../types/weather';
import { Calendar, Droplets, Wind, Gauge, HelpCircle, Thermometer } from 'lucide-react';

interface WeatherForecastTimelineProps {
  forecasts: WeatherForecast[];
  regionName: string;
}

export const WeatherForecastTimeline: React.FC<WeatherForecastTimelineProps> = ({ forecasts, regionName }) => {
  if (!forecasts || forecasts.length === 0) {
    return (
      <div className="p-6 bg-gray-50 border border-gray-200 rounded-2xl text-center text-sm text-gray-500">
        No forecast timeline available for {regionName}.
      </div>
    );
  }

  const getUncertaintyBadge = (uncertainty: string) => {
    switch (uncertainty) {
      case 'LOW':
        return <span className="px-2 py-0.5 text-[10px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-full">Low Uncertainty</span>;
      case 'MODERATE':
        return <span className="px-2 py-0.5 text-[10px] font-semibold bg-blue-50 text-blue-700 border border-blue-200 rounded-full">Moderate Uncertainty</span>;
      case 'HIGH':
        return <span className="px-2 py-0.5 text-[10px] font-semibold bg-amber-50 text-amber-700 border border-amber-200 rounded-full">High Uncertainty</span>;
      default:
        return <span className="px-2 py-0.5 text-[10px] font-semibold bg-purple-50 text-purple-700 border border-purple-200 rounded-full">Wide Spread</span>;
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-bold text-gray-900 uppercase tracking-wider flex items-center gap-1.5">
          <Calendar className="w-4 h-4 text-blue-600" />
          Multi-Horizon Forecast Timeline — {regionName}
        </h4>
        <span className="text-xs text-gray-500 font-mono">
          NWP Horizon Progression (0h → 7d)
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
        {forecasts.map((fc) => (
          <div
            key={fc.forecast_id}
            className="p-4 bg-white border border-gray-200 rounded-xl shadow-xs space-y-3 hover:border-blue-200 transition-colors"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded">
                {fc.forecast_horizon}
              </span>
              {getUncertaintyBadge(fc.uncertainty)}
            </div>

            <div className="space-y-1.5">
              <div className="text-sm font-semibold text-gray-900 truncate">
                {fc.weather_condition}
              </div>
              <div className="text-[11px] text-gray-500 truncate">
                Source: {fc.forecast_source}
              </div>
            </div>

            <div className="pt-2 border-t border-gray-100 grid grid-cols-2 gap-2 text-xs">
              {fc.temperature_celsius !== undefined && fc.temperature_celsius !== null && (
                <div className="flex items-center gap-1 text-gray-700">
                  <Thermometer className="w-3.5 h-3.5 text-red-500 shrink-0" />
                  <span>{fc.temperature_celsius}°C</span>
                </div>
              )}
              {fc.rainfall_mm !== undefined && fc.rainfall_mm !== null && (
                <div className="flex items-center gap-1 text-gray-700">
                  <Droplets className="w-3.5 h-3.5 text-blue-500 shrink-0" />
                  <span>{fc.rainfall_mm} mm</span>
                </div>
              )}
              {fc.wind_speed_mps !== undefined && fc.wind_speed_mps !== null && (
                <div className="flex items-center gap-1 text-gray-700">
                  <Wind className="w-3.5 h-3.5 text-teal-500 shrink-0" />
                  <span>{fc.wind_speed_mps} m/s</span>
                </div>
              )}
              {fc.surface_pressure_hpa !== undefined && fc.surface_pressure_hpa !== null && (
                <div className="flex items-center gap-1 text-gray-700">
                  <Gauge className="w-3.5 h-3.5 text-purple-500 shrink-0" />
                  <span>{fc.surface_pressure_hpa} hPa</span>
                </div>
              )}
            </div>

            <div className="pt-1 text-[10px] text-gray-400 font-mono truncate">
              Valid until: {new Date(fc.forecast_valid_until).toLocaleDateString()}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
