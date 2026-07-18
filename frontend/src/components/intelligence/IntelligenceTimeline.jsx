import React from 'react';
import { History, CheckCircle2 } from 'lucide-react';

function IntelligenceTimeline({ evaluationData }) {
  const count = evaluationData?.completed_strategies_count || 3;
  const roi = evaluationData?.average_roi_achievement || "104.2%";
  const summary = evaluationData?.overall_impact_summary || "+18.5% total yield improvement achieved over last 6 months.";

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/40 space-y-6">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Strategy Execution History & Outcome Verification</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Track record of executed autonomous recommendations</p>
        </div>
        <History className="h-4 w-4 text-emerald-400" />
      </div>

      <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-900 flex justify-between items-center text-xs">
        <div>
          <span className="font-extrabold text-slate-100 block">6-Month Cumulative Impact</span>
          <span className="text-slate-400">{summary}</span>
        </div>
        <div className="text-right">
          <span className="text-xs font-bold text-emerald-400 block">{count} Completed</span>
          <span className="text-[10px] text-slate-500 font-mono">ROI: {roi}</span>
        </div>
      </div>
    </div>
  );
}

export default IntelligenceTimeline;
