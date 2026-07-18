import React from 'react';
import { Activity, ShieldCheck, ShieldAlert } from 'lucide-react';

function FarmHealthScore({ score, issuesCount }) {
  const isHealthy = score >= 85;
  const isModerate = score >= 70 && score < 85;

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-4 text-center">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3 text-left">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Composite Farm Vigor Index</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Aggregated multi-system health rating</p>
        </div>
        <Activity className="h-4 w-4 text-emerald-400" />
      </div>

      <div className="relative py-4 flex flex-col items-center justify-center">
        <div className="relative flex items-center justify-center">
          <svg className="w-32 h-32 transform -rotate-90">
            <circle
              cx="64"
              cy="64"
              r="52"
              stroke="#0f172a"
              strokeWidth="10"
              fill="transparent"
            />
            <circle
              cx="64"
              cy="64"
              r="52"
              stroke={isHealthy ? "#10b981" : isModerate ? "#f59e0b" : "#f43f5e"}
              strokeWidth="10"
              strokeDasharray={326}
              strokeDashoffset={326 - (326 * score) / 100}
              strokeLinecap="round"
              fill="transparent"
              className="transition-all duration-1000 ease-out"
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className={`text-3xl font-black font-mono tracking-tight ${
              isHealthy ? 'text-emerald-400' : isModerate ? 'text-amber-400' : 'text-rose-400'
            }`}>
              {score}
            </span>
            <span className="text-[9px] uppercase tracking-wider text-slate-500 font-bold">/ 100</span>
          </div>
        </div>

        <div className="mt-4 flex items-center gap-1.5 justify-center">
          {isHealthy ? (
            <div className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[10px] font-black uppercase tracking-wider flex items-center gap-1">
              <ShieldCheck className="h-3.5 w-3.5" /> Optimal Condition
            </div>
          ) : (
            <div className="px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 text-[10px] font-black uppercase tracking-wider flex items-center gap-1">
              <ShieldAlert className="h-3.5 w-3.5" /> {issuesCount || 1} Active Stresses
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default FarmHealthScore;
