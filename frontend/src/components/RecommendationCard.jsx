import React from 'react';
import { CheckCircle2, AlertTriangle, AlertCircle, PlayCircle } from 'lucide-react';

function RecommendationCard({ recommendation }) {
  if (!recommendation) return null;

  const { parameter, status, message, action, value } = recommendation;
  
  // Clean values
  const displayStatus = status || 'Optimal';
  const normStatus = displayStatus.toLowerCase();

  const getStatusConfig = (st) => {
    if (st.includes('critical') || st.includes('danger') || st.includes('error')) {
      return {
        border: 'border-rose-500/30 bg-rose-950/20',
        text: 'text-rose-400',
        badge: 'bg-rose-500/10 text-rose-400 border-rose-500/20',
        icon: AlertCircle,
      };
    }
    if (st.includes('warning') || st.includes('caution')) {
      return {
        border: 'border-amber-500/30 bg-amber-950/20',
        text: 'text-amber-400',
        badge: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
        icon: AlertTriangle,
      };
    }
    return {
      border: 'border-emerald-500/25 bg-emerald-950/15',
      text: 'text-emerald-400',
      badge: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
      icon: CheckCircle2,
    };
  };

  const config = getStatusConfig(normStatus);
  const StatusIcon = config.icon;

  return (
    <div className={`p-5 rounded-xl border ${config.border} flex flex-col md:flex-row gap-4 transition-all duration-300`}>
      {/* Icon Area */}
      <div className={`p-2 rounded-lg shrink-0 w-fit h-fit ${config.badge}`}>
        <StatusIcon className="h-5 w-5" />
      </div>

      {/* Content Area */}
      <div className="flex-grow space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-900/65 pb-2">
          <div className="flex items-center gap-2">
            <span className="font-bold text-white text-base">{parameter}</span>
            {value !== undefined && value !== null && (
              <span className="text-xs text-slate-400 bg-slate-900 px-2 py-0.5 rounded border border-slate-800 font-mono">
                Current: {value}
              </span>
            )}
          </div>
          <span className={`px-2 py-0.5 text-xs font-bold rounded border ${config.badge}`}>
            {displayStatus}
          </span>
        </div>

        {/* Diagnostic explanation */}
        <p className="text-slate-300 text-xs leading-relaxed">{message}</p>

        {/* Action Item */}
        {action && (
          <div className="bg-slate-950/50 p-3 rounded-lg border border-slate-900/80 flex items-start gap-2">
            <PlayCircle className={`h-4.5 w-4.5 shrink-0 mt-0.5 ${config.text}`} />
            <div className="space-y-0.5">
              <span className="text-[10px] text-slate-500 uppercase tracking-wider font-extrabold block">Recommended Action</span>
              <span className="text-slate-200 text-xs font-medium leading-relaxed">{action}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default RecommendationCard;
