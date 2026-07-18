import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function EnvironmentChart({ envStats }) {
  if (!envStats || Object.keys(envStats).length === 0 || envStats.water_ph?.avg === 0) {
    return (
      <div className="glass-panel p-6 rounded-2xl border border-slate-900 bg-slate-950/20 h-[320px] flex items-center justify-center text-slate-500 text-xs font-semibold">
        No environmental metrics to analyze.
      </div>
    );
  }

  const data = [
    { name: 'pH Level', avg: envStats.water_ph?.avg || 0, min: envStats.water_ph?.min || 0, max: envStats.water_ph?.max || 0 },
    { name: 'EC (mS/cm)', avg: envStats.water_ec?.avg || 0, min: envStats.water_ec?.min || 0, max: envStats.water_ec?.max || 0 },
    { name: 'Water Temp /10', avg: (envStats.water_temperature?.avg || 0) / 10, min: (envStats.water_temperature?.min || 0) / 10, max: (envStats.water_temperature?.max || 0) / 10 }
  ];

  return (
    <div className="glass-panel p-6 rounded-2xl border border-slate-900 bg-slate-950/20 shadow-lg h-[320px] flex flex-col justify-between">
      <div>
        <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Solution Stability Ranges</h4>
        <p className="text-[10px] text-slate-500">Comparing parameter variance (Water Temp scaled by /10)</p>
      </div>

      <div className="flex-grow w-full h-[200px] mt-2">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" opacity={0.3} />
            <XAxis dataKey="name" stroke="#64748b" fontSize={9} tickLine={false} />
            <YAxis stroke="#64748b" fontSize={9} tickLine={false} />
            <Tooltip
              contentStyle={{ backgroundColor: '#020617', borderColor: '#1e293b', borderRadius: '12px' }}
              itemStyle={{ fontSize: '11px', fontWeight: 'semibold' }}
            />
            <Legend verticalAlign="top" height={36} iconType="circle" iconSize={6} wrapperStyle={{ fontSize: '9px' }} />
            <Bar dataKey="min" fill="#38bdf8" radius={[4, 4, 0, 0]} name="Minimum" />
            <Bar dataKey="avg" fill="#10b981" radius={[4, 4, 0, 0]} name="Average" />
            <Bar dataKey="max" fill="#f43f5e" radius={[4, 4, 0, 0]} name="Maximum" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default EnvironmentChart;
