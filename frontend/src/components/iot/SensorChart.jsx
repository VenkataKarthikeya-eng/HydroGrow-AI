import React, { useState } from 'react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

function SensorChart({ data }) {
  const [activeTab, setActiveTab] = useState('temperature');

  const tabs = [
    { key: 'temperature', label: 'Air Temp', color: '#10b981', unit: '°C' },
    { key: 'water_ph', label: 'pH Balance', color: '#34d399', unit: 'pH' },
    { key: 'water_ec', label: 'EC Level', color: '#2dd4bf', unit: 'mS' },
    { key: 'humidity', label: 'Humidity', color: '#38bdf8', unit: '%' },
    { key: 'co2', label: 'CO2 Level', color: '#a78bfa', unit: 'ppm' }
  ];

  const activeConf = tabs.find(t => t.key === activeTab);

  const formatTime = (isoString) => {
    if (!isoString) return '';
    try {
      const d = new Date(isoString);
      return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    } catch (e) {
      return '';
    }
  };

  const chartData = (data || []).map(d => ({
    ...d,
    formattedTime: formatTime(d.timestamp)
  }));

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-4">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-white tracking-wider">Environmental Real-Time Timelines</h4>
          <p className="text-[10px] text-slate-500">Live streams of hydroponic parameter fluctuations</p>
        </div>

        <div className="flex flex-wrap gap-1">
          {tabs.map(t => (
            <button
              key={t.key}
              onClick={() => setActiveTab(t.key)}
              className={`px-2.5 py-1 rounded-lg text-[9px] font-black uppercase tracking-wider transition-all ${
                activeTab === t.key
                  ? 'bg-slate-900 border border-slate-800 text-white shadow-md'
                  : 'text-slate-500 hover:text-slate-300'
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>
      </div>

      <div className="h-[240px] w-full">
        {chartData.length === 0 ? (
          <div className="h-full flex items-center justify-center text-slate-500 text-xs font-semibold">
            No live timeline signals recorded yet. Click Ingest/Simulate.
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={activeConf.color} stopOpacity={0.15} />
                  <stop offset="95%" stopColor={activeConf.color} stopOpacity={0.0} />
                </linearGradient>
              </defs>
              <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" vertical={false} />
              <XAxis 
                dataKey="formattedTime" 
                stroke="#475569" 
                fontSize={8} 
                fontWeight={700}
                tickLine={false} 
              />
              <YAxis 
                stroke="#475569" 
                fontSize={8} 
                fontWeight={700}
                tickLine={false} 
                domain={['auto', 'auto']}
                unit={activeConf.unit}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#020617',
                  borderColor: '#1e293b',
                  borderRadius: '12px',
                  fontSize: '10px',
                  fontWeight: 'bold',
                  color: '#f8fafc'
                }}
                labelStyle={{ color: '#64748b', marginBottom: '2px' }}
              />
              <Area
                type="monotone"
                dataKey={activeConf.key}
                stroke={activeConf.color}
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorValue)"
              />
            </AreaChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}

export default SensorChart;
