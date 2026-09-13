import React from 'react';
import { ShieldAlert, HeartHandshake, PhoneCall, Home, Heart, FileCheck, ArrowRight } from 'lucide-react';
import { MagneticButton } from '../common/MagneticButton';
import { DemoBadge } from '../common/DemoBadge';
import { TiltCard } from '../common/TiltCard';

interface ReliefHubSectionProps {
  onNeedHelpClick: () => void;
  onWantToHelpClick: () => void;
}

export const ReliefHubSection: React.FC<ReliefHubSectionProps> = ({
  onNeedHelpClick,
  onWantToHelpClick,
}) => {
  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      <div className="text-center max-w-3xl mx-auto mb-16">
        <div className="inline-flex items-center gap-2 mb-3">
          <span className="text-xs font-mono uppercase tracking-wider text-charcoal-500 font-semibold">
            Unified Relief Coordination
          </span>
          <DemoBadge label="RELIEF COORDINATION" />
        </div>
        <h2 className="text-3xl sm:text-5xl font-bold tracking-tight text-charcoal-950 mb-4">
          When Disaster Strikes, Help Should Be Easy to Find.
        </h2>
        <p className="text-sm sm:text-base text-charcoal-600 leading-relaxed">
          Whether you are stranded in an affected valley or reaching out from across the nation to mobilize aid, our verified coordination ecosystem bridges citizens and responders directly.
        </p>
      </div>

      {/* Two Large Distinct Gateway Choices with Subtle Cursor Tilt */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Choice 1: 🆘 I NEED HELP */}
        <TiltCard
          maxTilt={1.5}
          className="rounded-3xl bg-white border-2 border-red-200/80 p-8 sm:p-10 shadow-elevated flex flex-col justify-between relative overflow-hidden group hover:border-red-400 transition-all duration-300"
        >
          <div className="absolute top-0 right-0 w-32 h-32 bg-red-50 rounded-bl-full pointer-events-none -z-0 opacity-60" />
          
          <div className="relative z-10">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-red-50 text-risk-critical border border-red-200 text-xs font-mono font-bold mb-6">
              <span className="w-2 h-2 rounded-full bg-risk-critical animate-ping" />
              <span>EMERGENCY CITIZEN AID</span>
            </div>

            <h3 className="text-3xl font-bold text-charcoal-950 mb-3 flex items-center gap-3">
              <span>🆘 I NEED HELP</span>
            </h3>

            <p className="text-sm text-charcoal-600 leading-relaxed mb-8">
              Immediate life-safety resources for individuals and families in affected disaster zones across India.
            </p>

            {/* Included features checklist */}
            <div className="space-y-3 mb-8">
              <div className="flex items-center gap-3 text-xs text-charcoal-800 font-medium">
                <div className="p-1.5 rounded-lg bg-red-50 text-risk-critical border border-red-100">
                  <PhoneCall className="w-3.5 h-3.5" />
                </div>
                <span>National & State Emergency Helplines (112 / 1070)</span>
              </div>
              <div className="flex items-center gap-3 text-xs text-charcoal-800 font-medium">
                <div className="p-1.5 rounded-lg bg-red-50 text-risk-critical border border-red-100">
                  <Home className="w-3.5 h-3.5" />
                </div>
                <span>Verified Multi-Purpose Shelters with Live Capacity</span>
              </div>
              <div className="flex items-center gap-3 text-xs text-charcoal-800 font-medium">
                <div className="p-1.5 rounded-lg bg-red-50 text-risk-critical border border-red-100">
                  <ShieldAlert className="w-3.5 h-3.5" />
                </div>
                <span>Medical Triage Points & Safe Drinking Water Distribution</span>
              </div>
              <div className="flex items-center gap-3 text-xs text-charcoal-800 font-medium">
                <div className="p-1.5 rounded-lg bg-red-50 text-risk-critical border border-red-100">
                  <FileCheck className="w-3.5 h-3.5" />
                </div>
                <span>Official State Disaster Relief Claim Portals</span>
              </div>
            </div>
          </div>

          <div className="relative z-10 pt-4 border-t border-paper-200">
            <MagneticButton
              variant="danger"
              size="lg"
              onClick={onNeedHelpClick}
              className="w-full justify-between"
            >
              <span>Access Emergency Resources</span>
              <ArrowRight className="w-4 h-4" />
            </MagneticButton>
          </div>
        </TiltCard>

        {/* Choice 2: ❤️ I WANT TO HELP */}
        <TiltCard
          maxTilt={1.5}
          className="rounded-3xl bg-white border-2 border-emerald-200/80 p-8 sm:p-10 shadow-elevated flex flex-col justify-between relative overflow-hidden group hover:border-emerald-400 transition-all duration-300"
        >
          <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-50 rounded-bl-full pointer-events-none -z-0 opacity-60" />

          <div className="relative z-10">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50 text-risk-low-soft border border-emerald-200 text-xs font-mono font-bold mb-6">
              <Heart className="w-3 h-3 text-risk-low" />
              <span>DONOR & VOLUNTEER CORPS</span>
            </div>

            <h3 className="text-3xl font-bold text-charcoal-950 mb-3 flex items-center gap-3">
              <span>❤️ I WANT TO HELP</span>
            </h3>

            <p className="text-sm text-charcoal-600 leading-relaxed mb-8">
              Verified, transparent channels for citizens, corporate CSR teams, and diaspora wishing to assist affected regions.
            </p>

            {/* Included features checklist */}
            <div className="space-y-3 mb-8">
              <div className="flex items-center gap-3 text-xs text-charcoal-800 font-medium">
                <div className="p-1.5 rounded-lg bg-emerald-50 text-risk-low-soft border border-emerald-100">
                  <FileCheck className="w-3.5 h-3.5" />
                </div>
                <span>Direct Government Relief Funds (CM & PM Relief Portals)</span>
              </div>
              <div className="flex items-center gap-3 text-xs text-charcoal-800 font-medium">
                <div className="p-1.5 rounded-lg bg-emerald-50 text-risk-low-soft border border-emerald-100">
                  <HeartHandshake className="w-3.5 h-3.5" />
                </div>
                <span>Verified Grassroots NGOs with Itemized Supply Wishlists</span>
              </div>
              <div className="flex items-center gap-3 text-xs text-charcoal-800 font-medium">
                <div className="p-1.5 rounded-lg bg-emerald-50 text-risk-low-soft border border-emerald-100">
                  <Home className="w-3.5 h-3.5" />
                </div>
                <span>On-Ground Volunteer Opportunities with Logistics Roles</span>
              </div>
              <div className="flex items-center gap-3 text-xs text-charcoal-800 font-medium">
                <div className="p-1.5 rounded-lg bg-emerald-50 text-risk-low-soft border border-emerald-100">
                  <ShieldAlert className="w-3.5 h-3.5" />
                </div>
                <span>Audited Transparency Scores & Utilization Reports</span>
              </div>
            </div>
          </div>

          <div className="relative z-10 pt-4 border-t border-paper-200">
            <MagneticButton
              variant="primary"
              size="lg"
              onClick={onWantToHelpClick}
              className="w-full justify-between"
            >
              <span>Explore Ways to Help</span>
              <ArrowRight className="w-4 h-4" />
            </MagneticButton>
          </div>
        </TiltCard>
      </div>
    </section>
  );
};
