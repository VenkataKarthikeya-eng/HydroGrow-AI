import React from 'react';
import { ArrowUpRight, Percent, Award } from 'lucide-react';

function ScenarioComparison({ simulationResult }) {
  if (!simulationResult) {
    return (
      <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl h-48 flex items-center justify-center text-slate-500 text-xs font-semibold">
        No active yield comparison.
      </div>
    );
  }

  const change = parseFloat(simulationResult.yield_change_percentage || 0);
  const isPositive = change >= 0;

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-4">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Yield Outcome Comparison</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Comparing override simulation outcome with active baseline</p>
        </div>
        <Percent className="h-4 w-4 text-emerald-450" />
      </div>

      <div className="grid grid-cols-3 gap-4 text-center">
        <div className="bg-slate-950/40 border border-slate-900/60 p-3 rounded-2xl">
          <p className="text-[8px] uppercase tracking-wider text-slate-500 font-black">Baseline Yield</p>
          <p className="text-base font-black text-slate-300 font-mono mt-1">284.6g</p>
        </div>

        <div className="bg-slate-950/40 border border-slate-900/60 p-3 rounded-2xl">
          <p className="text-[8px] uppercase tracking-wider text-slate-500 font-black">Optimized Yield</p>
          <p className="text-base font-black text-emerald-400 font-mono mt-1">
            {simulationResult.final_prediction?.weight || 0}g
          </p>
        </div>

        <div className="bg-slate-950/40 border border-slate-900/60 p-3 rounded-2xl relative overflow-hidden">
          <p className="text-[8px] uppercase tracking-wider text-slate-500 font-black">Yield Change</p>
          <div className="flex items-center justify-center gap-0.5 mt-1">
            <span className={`text-base font-black font-mono ${isPositive ? 'text-emerald-400' : 'text-rose-450'}`}>
              {isPositive ? '+' : ''}{change}%
            </span>
            <ArrowUpRight className={`h-3 w-3 ${isPositive ? 'text-emerald-400' : 'text-rose-450 rotate-90'}`} />
          </div>
        </div>
      </div>

      {simulationResult.recommendations && simulationResult.recommendations.length > 0 && (
        <div className="p-3 bg-emerald-500/5 rounded-2xl border border-emerald-500/10 text-[10px] text-emerald-400 font-semibold space-y-1">
          <div className="flex items-center gap-1 font-bold text-xs">
            <Award className="h-3.5 w-3.5 text-emerald-400" />
            <span>Simulation Insight Advisory</span>
          </div>
          <ul className="list-disc list-inside space-y-1 mt-1 text-slate-300">
            {simulationResult.recommendations.map((rec, i) => (
              <li key={i}>{rec}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default ScenarioComparison;
