import React from 'react';
import { Target, AlertTriangle, CheckCircle, ArrowRight, RefreshCw } from 'lucide-react';

function StrategyPlanner({ strategyData, onGeneratePlan }) {
  const strategies = strategyData?.strategies || [];

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/40 space-y-6">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Autonomous Farm Strategy & Improvement Plan</h4>
          <p className="text-[10px] text-slate-500 font-semibold">AI generated 6-month farming roadmap & high-impact initiatives</p>
        </div>
        <button
          onClick={onGeneratePlan}
          className="px-3 py-1.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-xs font-black uppercase tracking-wider transition-all flex items-center gap-1.5"
        >
          <RefreshCw className="h-3.5 w-3.5" /> Re-generate Strategy
        </button>
      </div>

      <div className="space-y-4">
        {strategies.map((s) => (
          <div key={s.id} className="p-5 rounded-2xl bg-slate-950/60 border border-slate-900 space-y-3">
            <div className="flex justify-between items-start">
              <div className="flex items-center gap-2">
                <span className={`px-2 py-0.5 rounded text-[9px] font-black uppercase ${
                  s.priority === 'CRITICAL' ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 'bg-emerald-500/10 text-emerald-400'
                }`}>
                  [{s.priority}] {s.strategy_type}
                </span>
                <span className="text-[10px] text-slate-500 font-mono">Confidence: {s.confidence_score}%</span>
              </div>
              <span className="px-2 py-0.5 rounded bg-slate-900 text-slate-400 text-[9px] font-bold">
                {s.status}
              </span>
            </div>

            <p className="text-xs text-slate-200 font-medium leading-relaxed">{s.recommendation}</p>

            <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-emerald-400 font-bold flex items-center gap-2">
              <Target className="h-4 w-4 shrink-0 text-emerald-400" />
              <span>Expected Impact: {s.expected_impact}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default StrategyPlanner;
