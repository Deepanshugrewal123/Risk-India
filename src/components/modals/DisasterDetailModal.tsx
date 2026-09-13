import React from 'react';
import { DisasterEvent } from '../../types/disaster';
import { RiskBadge } from '../common/RiskBadge';
import { DemoBadge } from '../common/DemoBadge';
import { MagneticButton } from '../common/MagneticButton';
import { X, MapPin, Clock, Users, ShieldAlert, HeartHandshake, PhoneCall, CheckCircle, ExternalLink, Home } from 'lucide-react';

interface DisasterDetailModalProps {
  incident: DisasterEvent | null;
  onClose: () => void;
  onHelpAction?: () => void;
}

export const DisasterDetailModal: React.FC<DisasterDetailModalProps> = ({
  incident,
  onClose,
  onHelpAction,
}) => {
  if (!incident) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 overflow-y-auto bg-charcoal-950/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="relative w-full max-w-3xl rounded-3xl bg-white border border-paper-300 shadow-floating my-8 overflow-hidden max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="p-6 sm:p-8 bg-paper-50/90 border-b border-paper-200 flex items-start justify-between gap-4 shrink-0">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <RiskBadge level={incident.severity} score={incident.riskScore} size="sm" />
              <span className="text-xs font-mono px-2 py-0.5 rounded-full bg-paper-200 text-charcoal-700 border border-paper-300">
                STATUS: {incident.status.toUpperCase()}
              </span>
              <DemoBadge label="MONITORED INCIDENT" />
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-charcoal-950">
              {incident.title}
            </h2>
            <div className="flex flex-wrap items-center gap-3 text-xs font-mono text-charcoal-500 mt-2">
              <span className="flex items-center gap-1">
                <MapPin className="w-3.5 h-3.5 text-charcoal-400" />
                {incident.location}, {incident.state}
              </span>
              <span>•</span>
              <span className="flex items-center gap-1">
                <Clock className="w-3.5 h-3.5 text-charcoal-400" />
                Updated {incident.lastUpdated}
              </span>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-xl text-charcoal-500 hover:text-charcoal-900 hover:bg-paper-200 transition-colors"
            aria-label="Close modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Scrollable Content Body */}
        <div className="p-6 sm:p-8 space-y-8 overflow-y-auto flex-1">
          {/* Section 1: Overview & Population Impact */}
          <div>
            <h3 className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-bold mb-2">
              01 // Situational Overview
            </h3>
            <p className="text-sm text-charcoal-700 leading-relaxed bg-paper-50 p-4 rounded-2xl border border-paper-200">
              {incident.description}
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-4 text-xs font-mono">
              <div className="p-3 rounded-xl bg-paper-100/60 border border-paper-200">
                <span className="text-charcoal-500 block text-[10px] uppercase">Affected Population</span>
                <span className="text-sm font-bold text-charcoal-900">{incident.affectedPopulationEstimate}</span>
              </div>
              <div className="p-3 rounded-xl bg-paper-100/60 border border-paper-200">
                <span className="text-charcoal-500 block text-[10px] uppercase">Relocated / Evacuated</span>
                <span className="text-sm font-bold text-charcoal-900">{incident.reportedEvacuations}</span>
              </div>
              <div className="p-3 rounded-xl bg-paper-100/60 border border-paper-200">
                <span className="text-charcoal-500 block text-[10px] uppercase">Shelters Active</span>
                <span className="text-sm font-bold text-charcoal-900">{incident.activeSheltersCount} Centers</span>
              </div>
            </div>
          </div>

          {/* Section 2: Key Environmental Risk Factors */}
          {incident.keyFactors && incident.keyFactors.length > 0 && (
            <div>
              <h3 className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-bold mb-3">
                02 // Observed Risk Factors & Triggers
              </h3>
              <ul className="space-y-2">
                {incident.keyFactors.map((factor, i) => (
                  <li key={i} className="flex items-start gap-2.5 text-xs sm:text-sm text-charcoal-700">
                    <span className="w-1.5 h-1.5 rounded-full bg-charcoal-900 mt-2 shrink-0" />
                    <span>{factor}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Section 3: Official Safety Advisories */}
          {incident.safetyAdvisories && incident.safetyAdvisories.length > 0 && (
            <div>
              <h3 className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-bold mb-3">
                03 // Citizen Safety Advisories
              </h3>
              <div className="space-y-2.5">
                {incident.safetyAdvisories.map((advisory, i) => (
                  <div
                    key={i}
                    className="p-3.5 rounded-xl bg-amber-50/60 border border-amber-200 flex items-start gap-3 text-xs sm:text-sm text-charcoal-800"
                  >
                    <ShieldAlert className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
                    <span>{advisory}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Section 4: Emergency Contacts & Source */}
          <div className="p-4 rounded-2xl bg-paper-100 border border-paper-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs font-mono">
            <div>
              <span className="text-charcoal-500 block text-[10px] uppercase">Official Reporting Agency</span>
              <span className="font-semibold text-charcoal-900">{incident.officialSource}</span>
            </div>
            <div className="text-right">
              <span className="text-charcoal-500 block text-[10px] uppercase">Emergency Helpline</span>
              <span className="font-bold text-charcoal-950">112 / 1070 (Toll Free)</span>
            </div>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="p-4 sm:p-6 bg-paper-50 border-t border-paper-200 flex flex-col sm:flex-row items-center justify-between gap-3 shrink-0">
          <span className="text-xs text-charcoal-500 font-mono">
            Verified information pipeline provided for disaster evaluation.
          </span>
          <div className="flex items-center gap-3 w-full sm:w-auto">
            <MagneticButton
              variant="secondary"
              size="md"
              onClick={onClose}
              className="w-full sm:w-auto"
            >
              Close Details
            </MagneticButton>
            {onHelpAction && (
              <MagneticButton
                variant="primary"
                size="md"
                onClick={() => {
                  onClose();
                  onHelpAction();
                }}
                className="w-full sm:w-auto gap-2"
              >
                <HeartHandshake className="w-4 h-4" />
                <span>Help This Region</span>
              </MagneticButton>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
