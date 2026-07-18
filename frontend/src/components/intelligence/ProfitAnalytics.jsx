import React from 'react';
import { DollarSign, TrendingUp, Sparkles, PieChart } from 'lucide-react';

function ProfitAnalytics({ profitData }) {
  const current = profitData?.current_crop || {};
  const comparison = profitData?.crop_comparison || [];

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/40 space-y-6">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Crop Profitability & Revenue Analytics</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Production costs, income forecasting & crop ROI ranking</p>
        </div>
        <DollarSign className="h-4 w-4 text-emerald-400" />
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-900 text-center space-y-1">
          <span className="text-[9px] font-bold text-slate-500 uppercase">Production Cost / Unit</span>
          <div className="text-2xl font-black text-slate-100 font-mono">${current.production_cost?.toFixed(2) || "1.20"}</div>
        </div>
        <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-900 text-center space-y-1">
          <span className="text-[9px] font-bold text-slate-500 uppercase">Estimated Market Value</span>
          <div className="text-2xl font-black text-slate-100 font-mono">${current.estimated_income?.toFixed(2) || "3.50"}</div>
        </div>
        <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-900 text-center space-y-1">
          <span className="text-[9px] font-bold text-slate-500 uppercase">Net Profit Margin</span>
          <div className="text-2xl font-black text-emerald-400 font-mono">{current.profit_margin || 65.7}%</div>
        </div>
      </div>

      <div className="space-y-3">
        <h5 className="text-xs font-extrabold text-slate-300">Crop Profitability Ranking</h5>
        <div className="space-y-2">
          {comparison.map((c, idx) => (
            <div key={idx} className="p-3.5 rounded-2xl bg-slate-950/60 border border-slate-900 flex justify-between items-center text-xs">
              <span className="font-extrabold text-slate-200">{c.crop_name}</span>
              <div className="flex items-center gap-4">
                <span className="text-slate-400">{c.growth_cycle_days} Days Cycle</span>
                <span className="font-mono font-black text-emerald-400">{c.profit_margin}% Margin</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ProfitAnalytics;
