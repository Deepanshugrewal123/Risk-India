import React from 'react';
import { WeatherWarning } from '../../types/weather';
import { AlertTriangle, Clock, MapPin, ExternalLink, ShieldAlert } from 'lucide-react';

interface WeatherWarningCardProps {
  warnings: WeatherWarning[];
}

export const WeatherWarningCard: React.FC<WeatherWarningCardProps> = ({ warnings }) => {
  if (!warnings || warnings.length === 0) {
    return (
      <div className="p-4 bg-emerald-50/50 border border-emerald-200 rounded-xl text-emerald-800 text-sm flex items-center gap-2">
        <ShieldAlert className="w-4 h-4 text-emerald-600 shrink-0" />
        <span>No active extreme weather bulletins or warnings issued by IMD for this scope.</span>
      </div>
    );
  }

  const getSeverityStyle = (severity: string) => {
    switch (severity) {
      case 'RED':
        return 'bg-red-50 border-red-200 text-red-900 badge-red';
      case 'ORANGE':
        return 'bg-orange-50 border-orange-200 text-orange-900 badge-orange';
      case 'YELLOW':
        return 'bg-amber-50 border-amber-200 text-amber-900 badge-yellow';
      default:
        return 'bg-emerald-50 border-emerald-200 text-emerald-900 badge-green';
    }
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-bold text-gray-900 uppercase tracking-wider flex items-center gap-1.5">
          <AlertTriangle className="w-4 h-4 text-amber-600" />
          Active Meteorological Bulletins & Warnings ({warnings.length})
        </h4>
        <span className="text-xs text-gray-500 font-mono">Source: IMD Official Warning Feed</span>
      </div>

      <div className="space-y-2">
        {warnings.map((w) => (
          <div
            key={w.warning_id}
            className={`p-4 rounded-xl border ${getSeverityStyle(w.severity)} space-y-2`}
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 text-xs font-bold font-mono uppercase tracking-wide rounded bg-white/80 border border-current shadow-2xs">
                  {w.severity} ALERT
                </span>
                <span className="text-xs font-mono font-semibold text-gray-700">
                  {w.hazard}
                </span>
              </div>
              <div className="flex items-center gap-1 text-[11px] text-gray-500">
                <Clock className="w-3.5 h-3.5" />
                <span>Issued: {new Date(w.issued_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
              </div>
            </div>

            <div className="text-sm font-semibold text-gray-900">{w.headline}</div>
            <p className="text-xs text-gray-700 leading-relaxed">{w.description}</p>

            <div className="pt-2 border-t border-black/5 flex items-center justify-between text-xs text-gray-600">
              <div className="flex items-center gap-1">
                <MapPin className="w-3.5 h-3.5 text-gray-400" />
                <span>Region: <strong className="font-semibold text-gray-800">{w.affected_region}</strong></span>
              </div>
              <a
                href={w.source_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 text-blue-600 hover:text-blue-800 text-[11px]"
              >
                <span>IMD Bulletin</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
