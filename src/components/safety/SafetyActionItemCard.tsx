import React, { useState } from 'react';
import {
  AlertTriangle,
  AlertOctagon,
  CheckSquare,
  Square,
  ChevronDown,
  ChevronUp,
  ShieldCheck,
  Flame,
  HeartHandshake,
  Users,
  CheckCircle2,
  Info,
  GitBranch,
  BookOpen,
  Clock,
  ArrowRight
} from 'lucide-react';
import { SafetyInstructionItem, SafetyPhase, SafetyPriority } from '../../types/safetyGuide';
import { NavigationPage } from '../common/Navbar';

interface SafetyActionItemCardProps {
  item: SafetyInstructionItem;
  isCompleted?: boolean;
  onToggleComplete?: (id: string) => void;
  defaultExpanded?: boolean;
  onNavigate?: (page: NavigationPage, context?: { hazard?: string; category?: string; regionId?: string }) => void;
}

export const SafetyActionItemCard: React.FC<SafetyActionItemCardProps> = ({
  item,
  isCompleted = false,
  onToggleComplete,
  defaultExpanded = false,
  onNavigate
}) => {
  const [isExpanded, setIsExpanded] = useState<boolean>(defaultExpanded);
  const [checkedSubtasks, setCheckedSubtasks] = useState<Record<string, boolean>>({});

  const toggleSubtask = (index: number) => {
    setCheckedSubtasks((prev) => ({
      ...prev,
      [`${item.id}-sub-${index}`]: !prev[`${item.id}-sub-${index}`]
    }));
  };

  const getPriorityBadge = (priority: SafetyPriority) => {
    switch (priority) {
      case 'CRITICAL':
        return {
          label: '🚨 CRITICAL LIFE SAFETY',
          badge: 'bg-rose-100 text-rose-800 border-rose-300 font-bold'
        };
      case 'HIGH':
      case 'IMPORTANT':
        return {
          label: '⚠️ IMPORTANT ACTION',
          badge: 'bg-amber-100 text-amber-800 border-amber-300 font-bold'
        };
      case 'RECOMMENDED':
      case 'HELPFUL':
      default:
        return {
          label: 'ℹ️ HELPFUL PREPARATION',
          badge: 'bg-blue-100 text-blue-800 border-blue-300 font-medium'
        };
    }
  };

  const getPhaseColor = (phase: SafetyPhase) => {
    switch (phase) {
      case 'BEFORE':
        return {
          label: 'BEFORE // PREPARE',
          icon: <ShieldCheck className="w-3.5 h-3.5 text-blue-700" />,
          color: 'bg-slate-100 text-slate-900 border-slate-300'
        };
      case 'DURING':
        return {
          label: 'DURING // SURVIVE',
          icon: <Flame className="w-3.5 h-3.5 text-amber-600" />,
          color: 'bg-amber-100 text-amber-900 border-amber-300'
        };
      case 'AFTER':
        return {
          label: 'AFTER // RECOVER',
          icon: <HeartHandshake className="w-3.5 h-3.5 text-teal-600" />,
          color: 'bg-teal-100 text-teal-900 border-teal-300'
        };
    }
  };

  const getTimingGuidance = () => {
    if (item.when_to_do) return item.when_to_do;
    if (item.when_urgent) return item.when_urgent;
    switch (item.phase) {
      case 'BEFORE':
        return 'Pre-disaster planning window — execute during household preparedness planning or immediately upon early warning alert issuance before physical hazards reach your locality.';
      case 'DURING':
        return 'Active hazard survival window — execute immediately when active hazard conditions emerge. Do not delay emergency evacuation or life-protection actions.';
      case 'AFTER':
        return 'Post-disaster recovery phase — execute only after civil authorities declare all-clear and immediate structural, electrical, or biological hazards have been mitigated.';
    }
  };

  const priorityMeta = getPriorityBadge(item.priority);
  const phaseMeta = getPhaseColor(item.phase);
  const panelId = `safety-item-panel-${item.id}`;

  return (
    <article
      className={`rounded-2xl border transition-all duration-200 overflow-hidden ${
        isCompleted
          ? 'bg-emerald-50/40 border-emerald-300 shadow-xs'
          : 'bg-white border-slate-200 shadow-xs hover:shadow-sm'
      }`}
      aria-labelledby={`safety-item-title-${item.id}`}
    >
      {/* Short Readable Card Header (Default Level 1 View) */}
      <div className="p-4 sm:p-5">
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1 min-w-0">
            {/* Badges Bar */}
            <div className="flex flex-wrap items-center gap-2 mb-2">
              <span className={`px-2.5 py-0.5 rounded-md border text-[10px] font-mono font-bold uppercase tracking-wider flex items-center gap-1.5 ${phaseMeta.color}`}>
                {phaseMeta.icon}
                <span>{phaseMeta.label}</span>
              </span>

              <span className={`px-2.5 py-0.5 rounded-md border text-[10px] font-mono font-bold uppercase tracking-wider ${priorityMeta.badge}`}>
                {priorityMeta.label}
              </span>

              <span className="px-2.5 py-0.5 rounded-md bg-slate-100 text-slate-700 border border-slate-200 text-[10px] font-mono uppercase font-semibold">
                {item.category.replace(/_/g, ' ')}
              </span>
            </div>

            {/* Title */}
            <h3
              id={`safety-item-title-${item.id}`}
              className={`text-base sm:text-lg font-bold tracking-tight text-slate-900 mb-1.5 ${
                isCompleted ? 'line-through text-slate-500' : ''
              }`}
            >
              {item.title}
            </h3>

            {/* Level 1 Concise Action Directive */}
            <p className="text-xs sm:text-sm text-slate-700 leading-relaxed">
              {item.instruction}
            </p>
          </div>

          {/* Interactive Checklist Quick Toggle */}
          {onToggleComplete && (
            <button
              onClick={() => onToggleComplete(item.id)}
              className="min-h-[44px] min-w-[44px] p-2 rounded-xl text-slate-500 hover:text-slate-900 hover:bg-slate-100 flex items-center justify-center transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-emerald-600 shrink-0"
              aria-label={isCompleted ? `Mark "${item.title}" as incomplete` : `Mark "${item.title}" as completed`}
            >
              {isCompleted ? (
                <CheckSquare className="w-5 h-5 text-emerald-600" />
              ) : (
                <Square className="w-5 h-5 text-slate-400" />
              )}
            </button>
          )}
        </div>

        {/* Action Button: Progressive Disclosure Trigger */}
        <div className="mt-3.5 pt-3 border-t border-slate-200 flex items-center justify-between gap-3">
          <div className="flex items-center gap-1.5 text-[11px] font-mono text-slate-500">
            <BookOpen className="w-3.5 h-3.5 text-emerald-600" />
            <span>NDMA Life-Safety Protocol</span>
          </div>

          <button
            onClick={() => setIsExpanded(!isExpanded)}
            aria-expanded={isExpanded}
            aria-controls={panelId}
            className="min-h-[44px] px-3.5 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-900 font-mono text-xs font-bold transition-all flex items-center gap-2 border border-slate-300 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-600"
          >
            <span>{isExpanded ? '[ HIDE DETAILS ▴ ]' : '[ EXAMINE MORE ▾ ]'}</span>
            {isExpanded ? (
              <ChevronUp className="w-4 h-4 text-blue-700" />
            ) : (
              <ChevronDown className="w-4 h-4 text-blue-700" />
            )}
          </button>
        </div>
      </div>

      {/* Expanded Deep Details Panel (Level 2 Progressive Disclosure - 10 Dimensions) */}
      {isExpanded && (
        <div
          id={panelId}
          className="p-5 sm:p-6 bg-slate-50 border-t border-slate-200 space-y-4 animate-in fade-in duration-200 text-slate-900"
        >
          {/* 1. WHAT TO DO */}
          <div className="p-3.5 rounded-xl bg-white border border-slate-200 space-y-1">
            <div className="text-[11px] font-mono font-bold uppercase tracking-wider text-slate-900 flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-blue-700" />
              <span>1. WHAT TO DO // CORE OPERATIONAL DIRECTIVE</span>
            </div>
            <p className="text-xs sm:text-sm text-slate-800 leading-relaxed pl-5 font-semibold">
              {item.action || item.instruction}
            </p>
          </div>

          {/* 2. HOW TO DO IT (Step-by-Step Practical Actions) */}
          {((item.practical_steps && item.practical_steps.length > 0) || (item.how_to_do_it && item.how_to_do_it.length > 0)) && (
            <div className="p-4 rounded-xl bg-white border border-slate-200 space-y-2">
              <div className="text-[11px] font-mono font-bold uppercase tracking-wider text-emerald-800 flex items-center gap-1.5">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                <span>2. HOW TO DO IT // PRACTICAL STEP-BY-STEP ACTIONS</span>
              </div>
              <ol className="space-y-1.5 pl-5 list-decimal text-xs sm:text-sm text-slate-800 leading-relaxed">
                {(item.practical_steps || item.how_to_do_it || []).map((step, idx) => (
                  <li key={idx} className="pl-1">
                    {step}
                  </li>
                ))}
              </ol>
            </div>
          )}

          {/* 3. WHEN TO DO IT (Timing & Execution Trigger Window) */}
          <div className="p-3.5 rounded-xl bg-blue-50/80 border border-blue-200 text-xs text-slate-800 flex items-start gap-2.5">
            <Clock className="w-4 h-4 text-blue-700 shrink-0 mt-0.5" />
            <div>
              <strong className="font-mono text-[11px] uppercase tracking-wider text-blue-900 block mb-0.5">
                3. When To Do It // Action Window &amp; Execution Trigger:
              </strong>
              <span className="leading-relaxed text-slate-800">{getTimingGuidance()}</span>
            </div>
          </div>

          {/* 4. WHY THIS MATTERS (Life-Safety Rationale) */}
          <div className="p-3.5 rounded-xl bg-white border border-slate-200 space-y-1 border-l-4 border-l-blue-600">
            <div className="text-[11px] font-mono font-bold uppercase tracking-wider text-blue-800 flex items-center gap-1.5">
              <Info className="w-3.5 h-3.5 text-blue-600" />
              <span>4. WHY THIS MATTERS // LIFE-SAFETY &amp; SCIENTIFIC RATIONALE</span>
            </div>
            <p className="text-xs sm:text-sm text-slate-700 leading-relaxed pl-5">
              {item.why_it_matters || item.reason}
            </p>
          </div>

          {/* 5. WHAT NOT TO DO (Dangerous Mistakes & Avoidance) */}
          {((item.what_not_to_do && item.what_not_to_do.length > 0) || item.warning || item.common_mistake || (item.what_to_avoid && item.what_to_avoid.length > 0)) && (
            <div className="p-4 rounded-xl bg-rose-50/80 border border-rose-200 text-rose-950 space-y-2">
              <div className="text-[11px] font-mono font-bold uppercase tracking-wider text-rose-800 flex items-center gap-1.5">
                <AlertOctagon className="w-4 h-4 text-rose-600 shrink-0" />
                <span>5. WHAT NOT TO DO // DANGEROUS MISTAKES &amp; LETHAL PITFALLS</span>
              </div>
              {item.warning && (
                <p className="text-xs sm:text-sm font-semibold pl-5 leading-relaxed text-rose-900">
                  {item.warning}
                </p>
              )}
              {item.common_mistake && (
                <div className="pl-5 text-xs text-rose-900">
                  <strong>Common Civilian Mistake: </strong>
                  <span>{item.common_mistake}</span>
                </div>
              )}
              {((item.what_not_to_do && item.what_not_to_do.length > 0) || (item.what_to_avoid && item.what_to_avoid.length > 0)) && (
                <ul className="space-y-1 pl-5 list-disc text-xs leading-relaxed text-rose-900">
                  {(item.what_not_to_do || item.what_to_avoid || []).map((dont, idx) => (
                    <li key={idx}>{dont}</li>
                  ))}
                </ul>
              )}
            </div>
          )}

          {/* 6. WARNING SIGNS (Observable Field Indicators) */}
          {item.warning_signs && item.warning_signs.length > 0 && (
            <div className="p-4 rounded-xl bg-amber-50/70 border border-amber-200 text-amber-950 space-y-2">
              <div className="text-[11px] font-mono font-bold uppercase tracking-wider text-amber-800 flex items-center gap-1.5">
                <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
                <span>6. WARNING SIGNS // OBSERVED GROUND-LEVEL FIELD SIGNS</span>
              </div>
              <ul className="space-y-1 pl-5 list-disc text-xs sm:text-sm text-amber-950 leading-relaxed">
                {item.warning_signs.map((sign, idx) => (
                  <li key={idx} className="pl-1">
                    {sign}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* 7. WHO NEEDS EXTRA ATTENTION (Vulnerable Household Members) */}
          {item.vulnerable_groups && (
            <div className="p-3.5 rounded-xl bg-indigo-50/70 border border-indigo-200 text-xs text-slate-800 flex items-start gap-2.5">
              <Users className="w-4 h-4 text-indigo-700 shrink-0 mt-0.5" />
              <div>
                <strong className="font-mono text-[11px] uppercase tracking-wider text-indigo-900 block mb-0.5">
                  7. Who Needs Extra Attention // Vulnerable Household Demographics:
                </strong>
                <span className="leading-relaxed text-indigo-950">{item.vulnerable_groups}</span>
              </div>
            </div>
          )}

          {/* 8. ACTION CHECKLIST (Interactive Subtasks) */}
          {item.checklist && item.checklist.length > 0 && (
            <div className="p-4 rounded-xl bg-white border border-slate-200 space-y-2">
              <div className="text-[11px] font-mono font-bold uppercase tracking-wider text-slate-700 flex items-center gap-1.5">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                <span>8. HOUSEHOLD ACTION CHECKLIST // INTERACTIVE SUBTASKS</span>
              </div>
              <div className="space-y-1.5 pl-1">
                {item.checklist.map((task, idx) => {
                  const taskKey = `${item.id}-sub-${idx}`;
                  const isChecked = !!checkedSubtasks[taskKey];
                  return (
                    <label
                      key={idx}
                      onClick={() => toggleSubtask(idx)}
                      className="flex items-start gap-2.5 p-2 rounded-lg hover:bg-slate-100 cursor-pointer transition-colors text-xs leading-relaxed"
                    >
                      <input
                        type="checkbox"
                        checked={isChecked}
                        onChange={() => {}}
                        className="sr-only"
                      />
                      <span className="min-w-[18px] min-h-[18px] mt-0.5 flex items-center justify-center">
                        {isChecked ? (
                          <CheckSquare className="w-4 h-4 text-emerald-600" />
                        ) : (
                          <Square className="w-4 h-4 text-slate-400" />
                        )}
                      </span>
                      <span className={isChecked ? 'line-through text-slate-400' : 'text-slate-800 font-medium'}>
                        {task}
                      </span>
                    </label>
                  );
                })}
              </div>
            </div>
          )}

          {/* 9. RELATED SECONDARY / CASCADING RISK (With Direct Link to Cascading Explorer) */}
          {item.related_cascading_risk && (
            <div className="p-4 rounded-xl bg-purple-50/70 border border-purple-200 text-purple-950 space-y-2">
              <div className="text-[11px] font-mono font-bold uppercase tracking-wider text-purple-800 flex items-center gap-1.5">
                <GitBranch className="w-3.5 h-3.5 text-purple-700" />
                <span>9. RELATED SECONDARY &amp; CASCADING RISK PATHWAY</span>
              </div>
              <p className="text-xs sm:text-sm text-purple-950 font-medium leading-relaxed pl-5">
                {item.related_cascading_risk}
              </p>
              {onNavigate && (
                <div className="pl-5 pt-1">
                  <button
                    onClick={() => onNavigate('cascading-risk', { hazard: item.hazard })}
                    className="min-h-[36px] px-3.5 py-1.5 rounded-lg bg-purple-700 hover:bg-purple-800 text-white font-mono text-[11px] font-bold flex items-center gap-1.5 transition-colors shadow-2xs"
                  >
                    <GitBranch className="w-3.5 h-3.5" />
                    <span>VIEW {item.hazard} CASCADING CONSEQUENCE CHAIN →</span>
                  </button>
                </div>
              )}
            </div>
          )}

          {/* 10. STATUTORY CITATION & EMERGENCY ACTIONS */}
          <div className="pt-3 border-t border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-[10px] font-mono text-slate-500">
            <div>
              <strong className="text-slate-700">10. Official Statutory Citation: </strong>
              <span>{item.source}</span>
            </div>

            {item.related_emergency_action && (
              <div className="flex items-center gap-1 text-emerald-800 font-semibold">
                <ShieldCheck className="w-3 h-3 text-emerald-600" />
                <span>Cross-Ref: {item.related_emergency_action}</span>
              </div>
            )}
          </div>
        </div>
      )}
    </article>
  );
};
