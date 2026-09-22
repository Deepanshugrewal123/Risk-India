import React from 'react';
import { 
  Activity, 
  Sparkles, 
  GitBranch, 
  BookOpen, 
  Radio, 
  Compass, 
  ArrowRight,
  CheckCircle2,
  Layers
} from 'lucide-react';
import { NavigationPage } from './Navbar';

interface PublicSafetyWorkflowBarProps {
  currentPage: NavigationPage;
  onNavigate?: (page: NavigationPage, context?: any) => void;
  className?: string;
}

interface WorkflowStep {
  page: NavigationPage;
  stepNumber: number;
  label: string;
  tagline: string;
  icon: React.ReactNode;
  accent: string;
}

const WORKFLOW_STEPS: WorkflowStep[] = [
  {
    page: 'home',
    stepNumber: 1,
    label: 'Current Risk',
    tagline: 'Real-time telemetry & warnings',
    icon: <Activity className="w-4 h-4" />,
    accent: 'text-slate-800'
  },
  {
    page: 'future-risk',
    stepNumber: 2,
    label: 'Future Risk',
    tagline: '5 forecast horizons (NOW–7d)',
    icon: <Sparkles className="w-4 h-4" />,
    accent: 'text-blue-700'
  },
  {
    page: 'cascading-risk',
    stepNumber: 3,
    label: 'Cascading Risk',
    tagline: 'What could happen next?',
    icon: <GitBranch className="w-4 h-4" />,
    accent: 'text-amber-700'
  },
  {
    page: 'safety-guide',
    stepNumber: 4,
    label: 'Safety Guide',
    tagline: '148 verified action protocols',
    icon: <BookOpen className="w-4 h-4" />,
    accent: 'text-emerald-700'
  },
  {
    page: 'disasters',
    stepNumber: 5,
    label: 'Live Disasters',
    tagline: 'Active Incident Command Stream',
    icon: <Radio className="w-4 h-4" />,
    accent: 'text-rose-700'
  },
  {
    page: 'risk-map',
    stepNumber: 6,
    label: 'Open Risk Map',
    tagline: '36-region geospatial matrix',
    icon: <Compass className="w-4 h-4" />,
    accent: 'text-indigo-700'
  },
];

export const PublicSafetyWorkflowBar: React.FC<PublicSafetyWorkflowBarProps> = ({
  currentPage,
  onNavigate,
  className = ''
}) => {
  const currentIndex = WORKFLOW_STEPS.findIndex((s) => s.page === currentPage);
  const nextStep = currentIndex >= 0 && currentIndex < WORKFLOW_STEPS.length - 1 
    ? WORKFLOW_STEPS[currentIndex + 1] 
    : WORKFLOW_STEPS[0];

  return (
    <section 
      className={`rounded-3xl bg-white border border-slate-200 p-6 sm:p-8 shadow-xs space-y-5 ${className}`}
      aria-labelledby="workflow-nav-heading"
    >
      {/* Eyebrow & Headline */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-200">
        <div className="space-y-1">
          <div className="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full bg-blue-50 border border-blue-200 text-blue-800 text-[11px] font-mono font-bold uppercase tracking-wider">
            <Layers className="w-3.5 h-3.5" />
            <span>CONNECTIVE PUBLIC SAFETY INTELLIGENCE</span>
          </div>
          <h2 id="workflow-nav-heading" className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
            Integrated Disaster Workflow
          </h2>
          <p className="text-xs sm:text-sm text-slate-600">
            Navigate seamlessly through every phase of national disaster decision-support.
          </p>
        </div>

        {/* Next Step Quick Action Button */}
        {onNavigate && nextStep && (
          <button
            onClick={() => onNavigate(nextStep.page)}
            className="min-h-[44px] px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-mono text-xs font-bold transition-all shadow-xs flex items-center justify-center gap-2 shrink-0 self-start sm:self-center"
          >
            <span>NEXT: {nextStep.label.toUpperCase()}</span>
            <ArrowRight className="w-3.5 h-3.5 text-blue-400" />
          </button>
        )}
      </div>

      {/* Stepped Progress Workflow (6 Connected Pillars) */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2.5">
        {WORKFLOW_STEPS.map((step) => {
          const isCurrent = step.page === currentPage;
          return (
            <button
              key={step.page}
              onClick={() => onNavigate && onNavigate(step.page)}
              className={`p-3.5 rounded-2xl border text-left transition-all relative flex flex-col justify-between min-h-[105px] focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 ${
                isCurrent
                  ? 'bg-blue-50/60 border-blue-600 shadow-xs'
                  : 'bg-slate-50/80 border-slate-200 hover:bg-white hover:border-slate-300'
              }`}
              aria-current={isCurrent ? 'page' : undefined}
            >
              <div>
                <div className="flex items-center justify-between gap-1 mb-1.5">
                  <span className="text-[10px] font-mono font-bold text-slate-500">
                    STEP {step.stepNumber}
                  </span>
                  <span className={step.accent}>
                    {step.icon}
                  </span>
                </div>
                <h3 className={`text-xs font-bold leading-tight ${isCurrent ? 'text-blue-900' : 'text-slate-900'}`}>
                  {step.label}
                </h3>
              </div>
              <p className="text-[10px] text-slate-600 line-clamp-2 mt-1 font-sans">
                {step.tagline}
              </p>
              {isCurrent && (
                <div className="mt-2 flex items-center gap-1 text-[10px] font-mono font-bold text-blue-700">
                  <CheckCircle2 className="w-3 h-3 text-blue-600" />
                  <span>ACTIVE VIEW</span>
                </div>
              )}
            </button>
          );
        })}
      </div>
    </section>
  );
};
