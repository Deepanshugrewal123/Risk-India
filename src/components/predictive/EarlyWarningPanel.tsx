import React from 'react';
import { EarlyWarningAssessment, EarlyWarningStatus } from '../../types/predictiveRisk';
import {
  BellRing,
  AlertTriangle,
  ShieldCheck,
  LifeBuoy,
  FileCheck2,
  Clock,
  ExternalLink
} from 'lucide-react';

interface EarlyWarningPanelProps {
  earlyWarning: EarlyWarningAssessment;
  hazard: string;
}

export const EarlyWarningPanel: React.FC<EarlyWarningPanelProps> = ({
  earlyWarning,
  hazard
}) => {
  const getStatusConfig = (status: EarlyWarningStatus) => {
    switch (status) {
      case 'EMERGENCY':
        return {
          title: 'STATE EMERGENCY — IMMEDIATE ACTION REQUIRED',
          badge: 'EMERGENCY',
          bg: 'bg-rose-600 text-white',
          border: 'border-rose-600',
          desc: 'Imminent severe hazard threshold reached. Immediate protective and sheltering action essential.'
        };
      case 'EVACUATION_READINESS':
        return {
          title: 'EVACUATION READINESS ADVISORY',
          badge: 'EVACUATION READINESS',
          bg: 'bg-rose-50 text-rose-900',
          border: 'border-rose-200',
          desc: 'High hazard convergence. Residents in vulnerable structures should stand ready for orderly relocation.'
        };
      case 'GET_READY':
        return {
          title: 'GET READY — HEIGHTENED READINESS',
          badge: 'GET READY',
          bg: 'bg-amber-50 text-amber-900',
          border: 'border-amber-200',
          desc: 'Hazard escalation probable within short lead time. Finalize supplies and secure surroundings.'
        };
      case 'PREPARE':
        return {
          title: 'PREPARE — COMMUNITY PREPAREDNESS',
          badge: 'PREPARE',
          bg: 'bg-blue-50 text-blue-900',
          border: 'border-blue-200',
          desc: 'Emerging risk signal detected. Review household disaster checklists and replenish consumables.'
        };
      case 'WATCH':
        return {
          title: 'WATCH — SITUATIONAL MONITORING',
          badge: 'WATCH',
          bg: 'bg-sky-50 text-sky-900',
          border: 'border-sky-200',
          desc: 'Atmospheric or environmental conditions warrant routine tracking. No immediate disruption.'
        };
      case 'NO_ACTIVE_SIGNAL':
      default:
        return {
          title: 'NO ACTIVE WARNING SIGNAL',
          badge: 'NORMAL MONITORING',
          bg: 'bg-emerald-50 text-emerald-900',
          border: 'border-emerald-200',
          desc: 'Baseline conditions persist across local catchment and meteorological stations.'
        };
    }
  };

  const cfg = getStatusConfig(earlyWarning.status);

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-4 sm:p-5 shadow-xs space-y-4">
      <div className="flex items-center justify-between flex-wrap gap-2 pb-2 border-b border-slate-100">
        <div className="flex items-center gap-2">
          <BellRing className="w-4 h-4 text-blue-700" />
          <h4 className="text-sm font-bold uppercase tracking-wider text-slate-900">
            Decision Support & Early Warning Status
          </h4>
        </div>
        <div className="flex items-center gap-2 text-xs font-mono text-slate-500">
          <Clock className="w-3.5 h-3.5" />
          <span>Lead Time Window: {earlyWarning.lead_time_window}</span>
        </div>
      </div>

      {/* Main Status Banner */}
      <div className={`p-3.5 rounded-xl border ${cfg.border} ${cfg.bg} flex items-start gap-3`}>
        <div className="p-2 rounded-lg bg-black/5 shrink-0">
          <LifeBuoy className="w-5 h-5" />
        </div>
        <div className="space-y-0.5">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs font-mono font-bold uppercase tracking-wide">
              {cfg.badge}
            </span>
            {earlyWarning.official_bulletin_reference && (
              <span className="text-[11px] font-mono opacity-80">
                [{earlyWarning.official_bulletin_reference}]
              </span>
            )}
          </div>
          <h5 className="text-sm font-bold">{cfg.title}</h5>
          <p className="text-xs opacity-90 leading-relaxed font-normal">{cfg.desc}</p>
        </div>
      </div>

      {/* Strict Separation: Evacuation Order vs Preparation Guidance */}
      {earlyWarning.is_evacuation_advised && earlyWarning.evacuation_guidance && (
        <div className="p-3.5 rounded-xl border border-rose-200 bg-rose-50 text-xs text-rose-900 space-y-1.5">
          <div className="flex items-center gap-1.5 font-bold text-rose-700 uppercase tracking-wide">
            <AlertTriangle className="w-4 h-4 text-rose-600" />
            <span>Evacuation Advisory Active</span>
          </div>
          <p className="text-xs leading-relaxed font-medium">
            {earlyWarning.evacuation_guidance}
          </p>
        </div>
      )}

      {/* Preparation Guidance Checklist */}
      {earlyWarning.preparation_guidance.length > 0 && (
        <div className="space-y-2 pt-1 text-xs">
          <span className="font-semibold text-slate-800 flex items-center gap-1.5">
            <FileCheck2 className="w-4 h-4 text-blue-700" />
            <span>Pre-Disaster Readiness Actions ({hazard}):</span>
          </span>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {earlyWarning.preparation_guidance.map((step, idx) => (
              <div
                key={idx}
                className="flex items-start gap-2 p-2.5 rounded-xl border border-slate-200 bg-slate-50"
              >
                <ShieldCheck className="w-3.5 h-3.5 text-blue-700 shrink-0 mt-0.5" />
                <span className="text-slate-700 leading-relaxed font-normal">
                  {step}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default EarlyWarningPanel;
