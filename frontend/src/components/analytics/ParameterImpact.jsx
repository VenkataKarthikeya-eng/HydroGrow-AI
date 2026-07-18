import React from 'react';
import { ArrowUpRight, ArrowDownRight } from 'lucide-react';

function ParameterImpact({ correlations }) {
  if (!correlations || Object.keys(correlations).length === 0) {
    return (
      <div className="glass-panel p-6 rounded-2xl border border-slate-900 bg-slate-950/20 h-[320px] flex items-center justify-center text-slate-500 text-xs font-semibold">
        No environmental correlation data.
      </div>
    );
  }

  const formatTitle = (key) => {
    return key
      .replace(/_/g, ' ')
      .replace('ml', '(mL)')
      .replace('l', '(L)')
      .replace(/\b\w/g, (c) => c.toUpperCase());
  };

  return (
    <div className="glass-panel p-6 rounded-2xl border border-slate-900 bg-slate-950/20 shadow-lg h-[320px] flex flex-col justify-between">
      <div>
        <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Environmental Parameter Impact</h4>
        <p className="text-[10px] text-slate-500">Pearson correlation with lettuce harvest weight</p>
      </div>

      <div className="flex-grow mt-3.5 overflow-y-auto space-y-2 pr-1 scrollbar-thin">
        {Object.entries(correlations).map(([key, val]) => {
          const isPositive = val.impact === 'positive';
          const corrVal = val.correlation;
          
          return (
            <div key={key} className="flex justify-between items-center p-2.5 rounded-xl bg-slate-950/40 border border-slate-900 hover:border-slate-850 transition-all">
              <div className="flex items-center gap-2.5">
                <div className={`p-1.5 rounded-lg border ${
                  isPositive 
                    ? 'bg-emerald-500/5 border-emerald-500/10 text-emerald-400' 
                    : 'bg-rose-500/5 border-rose-500/10 text-rose-400'
                }`}>
                  {isPositive ? <ArrowUpRight className="h-3.5 w-3.5" /> : <ArrowDownRight className="h-3.5 w-3.5" />}
                </div>
                <div>
                  <span className="text-[11px] font-semibold text-slate-200 block leading-tight">{formatTitle(key)}</span>
                  <span className="text-[9px] text-slate-500 font-medium">Optimal Target: {val.optimal_range}</span>
                </div>
              </div>

              <div className="text-right">
                <span className={`text-[11px] font-black block font-mono ${isPositive ? 'text-emerald-400' : 'text-rose-400'}`}>
                  {corrVal >= 0 ? `+${corrVal.toFixed(2)}` : corrVal.toFixed(2)}
                </span>
                <span className="text-[8px] text-slate-600 uppercase font-bold tracking-wider block">
                  {isPositive ? 'Positive' : 'Negative'}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default ParameterImpact;
