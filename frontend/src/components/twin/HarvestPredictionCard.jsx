import React from 'react';
import { Calendar, Gauge, ShieldAlert } from 'lucide-react';

function HarvestPredictionCard({ harvestData, riskFactors }) {
  if (!harvestData) {
    return (
      <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl h-48 flex items-center justify-center text-slate-500 text-xs font-semibold">
        Simulation run pending.
      </div>
    );
  }

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-4">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Harvest Predictions</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Estimated date, yield potential, and certainty rating</p>
        </div>
        <Calendar className="h-4 w-4 text-emerald-400" />
      </div>

      <div className="grid grid-cols-2 gap-4 text-xs font-bold">
        <div className="space-y-1">
          <p className="text-[9px] uppercase tracking-wider text-slate-500 font-black">Target Harvest Date</p>
          <p className="text-sm font-black text-slate-200">{harvestData.expected_date || 'N/A'}</p>
        </div>

        <div className="space-y-1">
          <p className="text-[9px] uppercase tracking-wider text-slate-500 font-black">Confidence Index</p>
          <div className="flex items-center gap-1.5 mt-0.5">
            <span className="font-mono text-emerald-400 text-sm font-black">
              {(harvestData.confidence_score * 100).toFixed(0)}%
            </span>
            <Gauge className="h-4 w-4 text-emerald-400" />
          </div>
        </div>
      </div>

      {riskFactors && riskFactors.length > 0 && (
        <div className="p-3 bg-rose-500/5 border border-rose-500/10 rounded-2xl text-[10px] text-rose-400 font-semibold space-y-1">
          <div className="flex items-center gap-1 font-bold">
            <ShieldAlert className="h-3.5 w-3.5" />
            <span>Simulated Biological Threats</span>
          </div>
          <ul className="list-disc list-inside space-y-1 mt-1 text-slate-350">
            {riskFactors.map((risk, i) => (
              <li key={i}>{risk}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default HarvestPredictionCard;
