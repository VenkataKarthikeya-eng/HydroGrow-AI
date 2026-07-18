import React from 'react';
import { TrendingUp, Globe, ArrowUpRight, ArrowRight, ArrowDownRight } from 'lucide-react';

function MarketTrendDashboard({ marketData }) {
  const report = marketData?.market_report || [];
  const opportunities = marketData?.opportunities || [];

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/40 space-y-6">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Regional Market Intelligence & Demand Forecasting</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Commodity price predictions & seasonal market opportunities</p>
        </div>
        <Globe className="h-4 w-4 text-emerald-400" />
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {report.map((r, idx) => (
          <div key={idx} className="p-4 rounded-2xl bg-slate-950/60 border border-slate-900 space-y-2">
            <div className="flex justify-between items-start">
              <h5 className="font-extrabold text-slate-100 text-xs">{r.crop_name}</h5>
              <span className={`px-2 py-0.5 rounded text-[9px] font-black uppercase ${
                r.trend_direction === 'RISING' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-slate-800 text-slate-400'
              }`}>
                {r.trend_direction}
              </span>
            </div>
            <div className="flex justify-between items-center text-xs pt-1">
              <span className="text-slate-400">Predicted Price</span>
              <span className="font-mono font-bold text-slate-100">${r.price_prediction?.toFixed(2)}</span>
            </div>
            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-400">Demand Score</span>
              <span className="font-mono font-bold text-emerald-400">{r.demand_score}%</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MarketTrendDashboard;
