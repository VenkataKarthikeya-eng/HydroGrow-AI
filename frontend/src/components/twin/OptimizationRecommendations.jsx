import React from 'react';
import { Lightbulb, CheckCircle2 } from 'lucide-react';

function OptimizationRecommendations({ recommendations }) {
  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl h-48 flex items-center justify-center text-slate-500 text-xs font-semibold">
        No active optimization strategies formulated.
      </div>
    );
  }

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-4">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">AI Optimization Strategies</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Agronomic parameters corrections guidelines</p>
        </div>
        <Lightbulb className="h-4 w-4 text-emerald-400" />
      </div>

      <div className="space-y-2.5">
        {recommendations.map((rec, idx) => (
          <div key={idx} className="flex gap-2 p-3 bg-slate-950/40 rounded-2xl border border-slate-900/50">
            <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0 mt-0.5" />
            <div className="text-[11px] font-semibold space-y-0.5">
              <p className="text-slate-400 uppercase text-[9px] font-black tracking-wider">{rec.parameter}</p>
              <p className="text-slate-200 font-bold">{rec.recommendation}</p>
              <p className="text-[10px] text-slate-500 font-medium">Impact: <span className="text-emerald-400 font-semibold">{rec.impact}</span> (current: {rec.current})</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default OptimizationRecommendations;
