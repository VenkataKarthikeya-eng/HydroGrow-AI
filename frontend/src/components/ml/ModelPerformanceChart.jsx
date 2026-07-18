import React from 'react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { TrendingUp } from 'lucide-react';

function ModelPerformanceChart({ metrics }) {
  const chartData = metrics?.accuracy_trends || [
    { version: 'v0.9.0', growth_r2: 0.85, disease_acc: 0.88 },
    { version: 'v0.9.5', growth_r2: 0.89, disease_acc: 0.92 },
    { version: 'v1.0.0', growth_r2: 0.935, disease_acc: 0.96 }
  ];

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-4">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Model Performance & Accuracy Progression</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Historical R² score & classification accuracy trends</p>
        </div>
        <TrendingUp className="h-4 w-4 text-emerald-400" />
      </div>

      <div className="h-48 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="colorGrowthR2" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.4}/>
                <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="version" stroke="#64748b" tick={{ fontSize: 10 }} />
            <YAxis domain={[0.7, 1.0]} stroke="#64748b" tick={{ fontSize: 10 }} />
            <Tooltip
              contentStyle={{ backgroundColor: '#020617', borderColor: '#1e293b', borderRadius: '1rem', fontSize: '12px' }}
            />
            <Area type="monotone" dataKey="growth_r2" name="Growth R² Score" stroke="#10b981" strokeWidth={2} fill="url(#colorGrowthR2)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default ModelPerformanceChart;
