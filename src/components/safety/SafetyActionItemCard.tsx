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
  BookOpen
} from 'lucide-react';
import { SafetyInstructionItem, SafetyPhase, SafetyPriority } from '../../types/safetyGuide';

interface SafetyActionItemCardProps {
  item: SafetyInstructionItem;
  isCompleted?: boolean;
  onToggleComplete?: (id: string) => void;
  defaultExpanded?: boolean;
}

export const SafetyActionItemCard: React.FC<SafetyActionItemCardProps> = ({
  item,
  isCompleted = false,
  onToggleComplete,
  defaultExpanded = false
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
          label: 'CRITICAL PRIORITY',
          badge: 'bg-rose-100 dark:bg-rose-950/70 text-rose-800 dark:text-rose-300 border-rose-300 dark:border-rose-800'
        };
      case 'HIGH':
        return {
          label: 'HIGH PRIORITY',
          badge: 'bg-amber-100 dark:bg-amber-950/70 text-amber-800 dark:text-amber-300 border-amber-300 dark:border-amber-800'
        };
      case 'RECOMMENDED':
      default:
        return {
          label: 'RECOMMENDED',
          badge: 'bg-blue-100 dark:bg-blue-950/70 text-blue-800 dark:text-blue-300 border-blue-300 dark:border-blue-800'
        };
    }
  };

  const getPhaseColor = (phase: SafetyPhase) => {
    switch (phase) {
      case 'BEFORE':
        return {
          label: 'BEFORE // PREPARE',
          icon: <ShieldCheck className="w-3.5 h-3.5" />,
          color: 'bg-paper-200 dark:bg-slate-700 text-charcoal-900 dark:text-slate-100 border-paper-300 dark:border-slate-600'
        };
      case 'DURING':
        return {
          label: 'DURING // SURVIVE',
          icon: <Flame className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />,
          color: 'bg-amber-100 dark:bg-amber-950/60 text-amber-900 dark:text-amber-200 border-amber-300 dark:border-amber-800'
        };
      case 'AFTER':
        return {
          label: 'AFTER // RECOVER',
          icon: <HeartHandshake className="w-3.5 h-3.5 text-teal-600 dark:text-teal-400" />,
          color: 'bg-teal-100 dark:bg-teal-950/60 text-teal-900 dark:text-teal-200 border-teal-300 dark:border-teal-800'
        };
    }
  };

  const priorityMeta = getPriorityBadge(item.priority);
  const phaseMeta = getPhaseColor(item.phase);
  const panelId = `safety-item-panel-${item.id}`;

  return (
    <article
      className={`rounded-2xl border transition-all duration-200 overflow-hidden ${
        isCompleted
          ? 'bg-emerald-50/40 dark:bg-emerald-950/20 border-emerald-300 dark:border-emerald-800'
          : 'bg-white dark:bg-slate-900 border-paper-300 dark:border-slate-800 shadow-sm hover:shadow-md'
      }`}
      aria-labelledby={`safety-item-title-${item.id}`}
    >
      {/* Short Readable Card Header (Default View) */}
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

              <span className="px-2.5 py-0.5 rounded-md bg-paper-100 dark:bg-slate-800 text-charcoal-600 dark:text-slate-400 border border-paper-200 dark:border-slate-700 text-[10px] font-mono uppercase font-semibold">
                {item.category.replace(/_/g, ' ')}
              </span>
            </div>

            {/* Title */}
            <h3
              id={`safety-item-title-${item.id}`}
              className={`text-base sm:text-lg font-bold tracking-tight text-charcoal-950 dark:text-white mb-1.5 ${
                isCompleted ? 'line-through text-charcoal-500 dark:text-slate-400' : ''
              }`}
            >
              {item.title}
            </h3>

            {/* Short Explanation (2 sentences maximum in default state) */}
            <p className="text-xs sm:text-sm text-charcoal-700 dark:text-slate-300 leading-relaxed">
              {item.instruction}
            </p>
          </div>

          {/* Interactive Checklist Quick Toggle */}
          {onToggleComplete && (
            <button
              onClick={() => onToggleComplete(item.id)}
              className="min-h-[44px] min-w-[44px] p-2 rounded-xl text-charcoal-500 hover:text-charcoal-900 dark:text-slate-400 dark:hover:text-white hover:bg-paper-100 dark:hover:bg-slate-800 flex items-center justify-center transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-emerald-600 shrink-0"
              aria-label={isCompleted ? `Mark "${item.title}" as incomplete` : `Mark "${item.title}" as completed`}
            >
              {isCompleted ? (
                <CheckSquare className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
              ) : (
                <Square className="w-5 h-5 text-charcoal-400 dark:text-slate-500" />
              )}
            </button>
          )}
        </div>

        {/* Action Button: Progressive Disclosure Trigger */}
        <div className="mt-3.5 pt-3 border-t border-paper-200 dark:border-slate-800/80 flex items-center justify-between gap-3">
          <div className="flex items-center gap-1.5 text-[11px] font-mono text-charcoal-500 dark:text-slate-400">
            <BookOpen className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
            <span>NDMA Life-Safety Protocol</span>
          </div>

          <button
            onClick={() => setIsExpanded(!isExpanded)}
            aria-expanded={isExpanded}
            aria-controls={panelId}
            className="min-h-[44px] px-3.5 py-1.5 rounded-xl bg-paper-100 hover:bg-paper-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-charcoal-900 dark:text-white font-mono text-xs font-bold transition-all flex items-center gap-2 border border-paper-300 dark:border-slate-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-600"
          >
            <span>{isExpanded ? 'HIDE DETAILS' : 'EXAMINE MORE'}</span>
            {isExpanded ? (
              <ChevronUp className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
            ) : (
              <ChevronDown className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
            )}
          </button>
        </div>
      </div>

      {/* Expanded Deep Details Panel (Progressive Disclosure) */}
      {isExpanded && (
        <div
          id={panelId}
          className="p-5 sm:p-6 bg-paper-50/70 dark:bg-slate-850 border-t border-paper-300 dark:border-slate-800 space-y-4 animate-in fade-in duration-200 text-charcoal-900 dark:text-slate-100"
        >
          {/* 1. WHY THIS MATTERS */}
          <div className="space-y-1.5">
            <div className="text-[11px] font-mono font-bold uppercase tracking-wider text-indigo-700 dark:text-indigo-400 flex items-center gap-1.5">
              <Info className="w-3.5 h-3.5" />
              <span>WHY THIS MATTERS // LIFE-SAFETY RATIONALE</span>
            </div>
            <p className="text-xs sm:text-sm text-charcoal-800 dark:text-slate-200 leading-relaxed pl-5 border-l-2 border-indigo-400 dark:border-indigo-600">
              {item.reason}
            </p>
          </div>

          {/* 2. WHAT TO DO (Practical Steps) */}
          {item.practical_steps && item.practical_steps.length > 0 && (
            <div className="space-y-2">
              <div className="text-[11px] font-mono font-bold uppercase tracking-wider text-emerald-700 dark:text-emerald-400 flex items-center gap-1.5">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>WHAT TO DO // PRACTICAL STEP-BY-STEP ACTIONS</span>
              </div>
              <ol className="space-y-1.5 pl-5 list-decimal text-xs sm:text-sm text-charcoal-800 dark:text-slate-200 leading-relaxed">
                {item.practical_steps.map((step, idx) => (
                  <li key={idx} className="pl-1">
                    {step}
                  </li>
                ))}
              </ol>
            </div>
          )}

          {/* 3. WARNING SIGNS / WHEN TO ACT */}
          {item.warning_signs && item.warning_signs.length > 0 && (
            <div className="space-y-2">
              <div className="text-[11px] font-mono font-bold uppercase tracking-wider text-amber-700 dark:text-amber-400 flex items-center gap-1.5">
                <AlertTriangle className="w-3.5 h-3.5" />
                <span>WARNING SIGNS // WHEN TO ACT</span>
              </div>
              <ul className="space-y-1 pl-5 list-disc text-xs sm:text-sm text-charcoal-800 dark:text-slate-200 leading-relaxed">
                {item.warning_signs.map((sign, idx) => (
                  <li key={idx} className="pl-1">
                    {sign}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* 4. WHAT NOT TO DO (Critical Prohibitions) */}
          {((item.what_not_to_do && item.what_not_to_do.length > 0) || item.warning) && (
            <div className="p-3.5 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900 text-rose-950 dark:text-rose-200 space-y-1.5">
              <div className="text-[11px] font-mono font-bold uppercase tracking-wider text-rose-700 dark:text-rose-400 flex items-center gap-1.5">
                <AlertOctagon className="w-4 h-4 text-rose-600 dark:text-rose-400 shrink-0" />
                <span>WHAT NOT TO DO // DANGEROUS ACTIONS</span>
              </div>
              {item.warning && (
                <p className="text-xs sm:text-sm font-semibold pl-5 leading-relaxed">
                  {item.warning}
                </p>
              )}
              {item.what_not_to_do && item.what_not_to_do.length > 0 && (
                <ul className="space-y-1 pl-5 list-disc text-xs leading-relaxed text-rose-900 dark:text-rose-300">
                  {item.what_not_to_do.map((dont, idx) => (
                    <li key={idx}>{dont}</li>
                  ))}
                </ul>
              )}
            </div>
          )}

          {/* 5. WHO NEEDS EXTRA ATTENTION (Vulnerable Household Members) */}
          {item.vulnerable_groups && (
            <div className="p-3 rounded-xl bg-indigo-50/70 dark:bg-indigo-950/30 border border-indigo-200/80 dark:border-indigo-900 text-xs text-charcoal-800 dark:text-slate-200 flex items-start gap-2.5">
              <Users className="w-4 h-4 text-indigo-600 dark:text-indigo-400 shrink-0 mt-0.5" />
              <div>
                <strong className="font-mono text-[11px] uppercase tracking-wider text-indigo-900 dark:text-indigo-300 block mb-0.5">
                  Who Needs Extra Attention:
                </strong>
                <span>{item.vulnerable_groups}</span>
              </div>
            </div>
          )}

          {/* 6. ACTION CHECKLIST (Interactive Subtasks) */}
          {item.checklist && item.checklist.length > 0 && (
            <div className="space-y-2 pt-2 border-t border-paper-300 dark:border-slate-800">
              <span className="text-[11px] font-mono font-bold uppercase tracking-wider text-charcoal-600 dark:text-slate-400 block">
                HOUSEHOLD ACTION CHECKLIST:
              </span>
              <div className="space-y-1.5">
                {item.checklist.map((task, idx) => {
                  const taskKey = `${item.id}-sub-${idx}`;
                  const isChecked = !!checkedSubtasks[taskKey];
                  return (
                    <label
                      key={idx}
                      onClick={() => toggleSubtask(idx)}
                      className="flex items-start gap-2.5 p-2 rounded-lg hover:bg-paper-100 dark:hover:bg-slate-800 cursor-pointer transition-colors text-xs leading-relaxed"
                    >
                      <input
                        type="checkbox"
                        checked={isChecked}
                        onChange={() => {}}
                        className="sr-only"
                      />
                      <span className="min-w-[18px] min-h-[18px] mt-0.5 flex items-center justify-center">
                        {isChecked ? (
                          <CheckSquare className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                        ) : (
                          <Square className="w-4 h-4 text-charcoal-400 dark:text-slate-500" />
                        )}
                      </span>
                      <span className={isChecked ? 'line-through text-charcoal-500 dark:text-slate-500' : 'text-charcoal-800 dark:text-slate-200'}>
                        {task}
                      </span>
                    </label>
                  );
                })}
              </div>
            </div>
          )}

          {/* Footer: Source & Related Cascading Risk */}
          <div className="pt-2 border-t border-paper-200 dark:border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-[10px] font-mono text-charcoal-500 dark:text-slate-400">
            <div>
              <span className="font-semibold text-charcoal-700 dark:text-slate-300">Statutory Citation: </span>
              <span>{item.source}</span>
            </div>

            {item.related_cascading_risk && (
              <div className="flex items-center gap-1.5 text-indigo-700 dark:text-indigo-400">
                <GitBranch className="w-3 h-3" />
                <span>Mitigates: {item.related_cascading_risk}</span>
              </div>
            )}
          </div>
        </div>
      )}
    </article>
  );
};
