import React from 'react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

function GrowthForecastChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl h-64 flex items-center justify-center text-slate-500 text-xs font-semibold">
        No active simulation telemetry. Adjust sliders and run simulation.
      </div>
    );
  }

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-4">
      <div>
        <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Growth Projections Curve</h4>
        <p className="text-[10px] text-slate-500 font-semibold">Day-by-day simulated height (cm) and fresh biomass weight (g) progression</p>
      </div>

      <div className="h-60 w-full text-[10px] font-mono">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="colorWeight" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.4}/>
                <stop offset="95%" stopColor="#10b981" stopOpacity={0.0}/>
              </linearGradient>
              <linearGradient id="colorHeight" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4}/>
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="day" stroke="#475569" tickLine={false} />
            <YAxis stroke="#475569" tickLine={false} />
            <Tooltip
              contentStyle={{ backgroundColor: '#020617', borderColor: '#1e293b', borderRadius: '12px' }}
              labelFormatter={(label) => `Day ${label}`}
            />
            <Legend verticalAlign="top" height={36} iconType="circle" />
            <Area
              name="Biomass Weight (g)"
              type="monotone"
              dataKey="predicted_weight"
              stroke="#10b981"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorWeight)"
            />
            <Area
              name="Plant Height (cm)"
              type="monotone"
              dataKey="predicted_height"
              stroke="#3b82f6"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorHeight)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default GrowthForecastChart;
