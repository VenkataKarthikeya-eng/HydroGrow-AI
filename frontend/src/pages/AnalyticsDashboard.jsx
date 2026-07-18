import React, { useState } from 'react';
import { TrendingUp, BarChart3, Award, Calendar, CheckCircle2, RefreshCw, Zap } from 'lucide-react';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';
import ChartContainer from '../components/ui/ChartContainer';

export default function AnalyticsDashboard() {
  const [timeRange, setTimeRange] = useState('30d');

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-300">
      
      {/* Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
            <TrendingUp className="w-4 h-4" /> Growth & Harvest Analytics
          </div>
          <h1 className="text-3xl font-black text-slate-900 dark:text-white mt-1">
            Crop Intelligence & Insights
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Historical growth cycle trends, yield distributions, and fertigation efficiency metrics.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {['7d', '30d', '90d'].map((range) => (
            <button
              key={range}
              onClick={() => setTimeRange(range)}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                timeRange === range
                  ? 'bg-emerald-600 text-white shadow-xs'
                  : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200'
              }`}
            >
              {range.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      {/* 4 Summary Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        
        <Card padding="p-6" className="space-y-2">
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider">Growth Cycles Completed</div>
          <div className="text-3xl font-black text-slate-900 dark:text-white">24 Cycles</div>
          <div className="text-xs text-emerald-600 font-semibold flex items-center gap-1 mt-1">
            <span>↑ 14% vs last period</span>
          </div>
        </Card>

        <Card padding="p-6" className="space-y-2">
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider">Average Yield / Plant</div>
          <div className="text-3xl font-black text-slate-900 dark:text-white">340.0g</div>
          <div className="text-xs text-emerald-600 font-semibold flex items-center gap-1 mt-1">
            <span>↑ +38g above target</span>
          </div>
        </Card>

        <Card padding="p-6" className="space-y-2">
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider">Harvest Success Rate</div>
          <div className="text-3xl font-black text-emerald-600 dark:text-emerald-400">94.2%</div>
          <div className="text-xs text-slate-500 font-semibold flex items-center gap-1 mt-1">
            <span>0% Pythium loss</span>
          </div>
        </Card>

        <Card padding="p-6" className="space-y-2">
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider">Fertigation Efficiency</div>
          <div className="text-3xl font-black text-slate-900 dark:text-white">98.1%</div>
          <div className="text-xs text-emerald-600 font-semibold flex items-center gap-1 mt-1">
            <span>Optimal dosing</span>
          </div>
        </Card>

      </div>

      {/* Chart Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Main Growth Curve Chart */}
        <div className="lg:col-span-2">
          <ChartContainer title="30-Day Historical Crop Yield Distribution" subtitle="Harvest Weight (g) across 24 Crop Batches">
            <div className="h-64 flex items-end justify-between gap-3 pt-8 pb-2 px-4 border-b border-slate-200 dark:border-slate-800">
              {[280, 310, 340, 325, 360, 390, 375, 410, 382].map((val, idx) => {
                const heightPercent = Math.min(100, Math.round((val / 450) * 100));
                return (
                  <div key={idx} className="flex-1 flex flex-col items-center gap-1 group relative">
                    <div className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 opacity-0 group-hover:opacity-100 transition-opacity">
                      {val}g
                    </div>
                    <div
                      style={{ height: `${heightPercent}%` }}
                      className="w-full bg-emerald-600 rounded-t-md transition-all duration-300 group-hover:bg-emerald-500"
                    />
                    <span className="text-[10px] text-slate-400 mt-1">B#{206 + idx}</span>
                  </div>
                );
              })}
            </div>
            <div className="flex justify-between items-center text-xs text-slate-500 mt-4">
              <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-emerald-600 rounded" /> Batch Harvest Weight</span>
              <span className="font-bold text-slate-700 dark:text-slate-300">Peak Harvest: Batch #213 (410.2g)</span>
            </div>
          </ChartContainer>
        </div>

        {/* Environmental Distribution */}
        <Card padding="p-6 sm:p-8" header="Environmental Compliance Index">
          <div className="space-y-5">
            <div>
              <div className="flex justify-between text-xs font-bold mb-1">
                <span className="text-slate-700 dark:text-slate-300">Air Temperature Target (22°C)</span>
                <span className="text-emerald-600 font-bold">98% Compliant</span>
              </div>
              <div className="w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full overflow-hidden">
                <div className="bg-emerald-600 h-full w-[98%]" />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs font-bold mb-1">
                <span className="text-slate-700 dark:text-slate-300">Water Solution pH (6.0 - 6.4)</span>
                <span className="text-emerald-600 font-bold">96% Compliant</span>
              </div>
              <div className="w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full overflow-hidden">
                <div className="bg-emerald-600 h-full w-[96%]" />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs font-bold mb-1">
                <span className="text-slate-700 dark:text-slate-300">Electrical Conductivity EC (2.0)</span>
                <span className="text-emerald-600 font-bold">92% Compliant</span>
              </div>
              <div className="w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full overflow-hidden">
                <div className="bg-emerald-600 h-full w-[92%]" />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs font-bold mb-1">
                <span className="text-slate-700 dark:text-slate-300">Relative Humidity (60 - 70%)</span>
                <span className="text-emerald-600 font-bold">99% Compliant</span>
              </div>
              <div className="w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full overflow-hidden">
                <div className="bg-emerald-600 h-full w-[99%]" />
              </div>
            </div>
          </div>
        </Card>

      </div>

    </div>
  );
}
