import React from 'react';
import { TrendingUp, DollarSign, BarChart3, Activity } from 'lucide-react';
import Card from '../../components/ui/Card';
import Badge from '../../components/ui/Badge';
import ChartContainer from '../../components/ui/ChartContainer';

export default function FarmIntelligenceDashboard() {
  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-300">
      <div className="border-b border-slate-200 dark:border-slate-800 pb-6">
        <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
          <TrendingUp className="w-4 h-4" /> Global Intelligence & Profitability
        </div>
        <h1 className="text-3xl font-black text-slate-900 dark:text-white mt-1">
          Profitability & Market Intelligence
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Analyze crop margins, electricity & fertigation input costs, and wholesale market pricing trends.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card padding="p-8" header="Projected Harvest Revenue">
          <div className="space-y-2">
            <div className="text-3xl font-black text-emerald-600">$14,280.00</div>
            <div className="text-xs text-slate-500">Based on 3,600 units @ $3.96 / unit wholesale.</div>
          </div>
        </Card>

        <Card padding="p-8" header="Total Fertigation Input Cost">
          <div className="space-y-2">
            <div className="text-3xl font-black text-slate-900 dark:text-white">$1,420.00</div>
            <div className="text-xs text-slate-500">Nutrients, water, & electricity consumption.</div>
          </div>
        </Card>

        <Card padding="p-8" header="Net Profit Margin">
          <div className="space-y-2">
            <div className="text-3xl font-black text-emerald-600">90.1% Net Margin</div>
            <div className="text-xs text-slate-500">High efficiency DWC hydroponic setup.</div>
          </div>
        </Card>
      </div>

      <ChartContainer title="6-Month Wholesale Market Price Trend (Hydroponic Lettuce)" subtitle="Wholesale Spot Prices ($/kg)">
        <div className="h-64 flex items-end justify-between gap-3 pt-8 pb-2 px-4 border-b border-slate-200 dark:border-slate-800">
          {[3.2, 3.4, 3.8, 3.6, 4.1, 3.9, 4.3, 4.2, 4.5].map((val, idx) => {
            const heightPercent = Math.min(100, Math.round((val / 5.0) * 100));
            return (
              <div key={idx} className="flex-1 flex flex-col items-center gap-1 group relative">
                <div className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 opacity-0 group-hover:opacity-100 transition-opacity">
                  ${val}
                </div>
                <div
                  style={{ height: `${heightPercent}%` }}
                  className="w-full bg-emerald-600 rounded-t-md transition-all duration-300 group-hover:bg-emerald-500"
                />
                <span className="text-[10px] text-slate-400 mt-1">M{idx + 1}</span>
              </div>
            );
          })}
        </div>
      </ChartContainer>
    </div>
  );
}
