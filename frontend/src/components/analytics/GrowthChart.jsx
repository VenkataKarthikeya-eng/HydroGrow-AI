import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function GrowthChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="glass-panel p-6 rounded-2xl border border-slate-900 bg-slate-950/20 h-[320px] flex items-center justify-center text-slate-500 text-xs font-semibold">
        No growth cycles recorded yet.
      </div>
    );
  }

  const chartData = data.map((d, i) => ({
    name: d.date !== 'N/A' ? d.date : `Cycle ${i+1}`,
    weight: d.weight,
    category: d.category
  }));

  return (
    <div className="glass-panel p-6 rounded-2xl border border-slate-900 bg-slate-950/20 shadow-lg h-[320px] flex flex-col justify-between">
      <div className="mb-2">
        <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Lettuce Harvest Weight Progression</h4>
        <p className="text-[10px] text-slate-500">Historical prediction yield trajectory (g)</p>
      </div>

      <div className="flex-grow w-full h-[200px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="colorWeight" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.2}/>
                <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" opacity={0.3} />
            <XAxis dataKey="name" stroke="#64748b" fontSize={9} tickLine={false} />
            <YAxis stroke="#64748b" fontSize={9} tickLine={false} domain={['auto', 'auto']} />
            <Tooltip
              contentStyle={{ backgroundColor: '#020617', borderColor: '#1e293b', borderRadius: '12px' }}
              labelStyle={{ color: '#94a3b8', fontSize: '10px', fontWeight: 'bold' }}
              itemStyle={{ color: '#10b981', fontSize: '11px', fontWeight: 'black' }}
            />
            <Area type="monotone" dataKey="weight" stroke="#10b981" strokeWidth={2.5} fillOpacity={1} fill="url(#colorWeight)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default GrowthChart;
