import React from 'react';

function MetricCard({ label, value, unit, icon: Icon, color = 'emerald' }) {
  const colorMap = {
    emerald: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
    blue: 'text-blue-400 bg-blue-500/10 border-blue-500/20',
    orange: 'text-orange-400 bg-orange-500/10 border-orange-500/20',
    purple: 'text-purple-400 bg-purple-500/10 border-purple-500/20',
  };

  const selectedColor = colorMap[color] || colorMap.emerald;

  return (
    <div className="glass-panel p-4 rounded-xl flex items-center justify-between border border-slate-800/80">
      <div className="space-y-1">
        <span className="text-xs text-slate-400 font-medium tracking-wide uppercase">{label}</span>
        <div className="flex items-baseline space-x-1">
          <span className="text-xl font-bold text-white">{value}</span>
          {unit && <span className="text-xs text-slate-500">{unit}</span>}
        </div>
      </div>
      {Icon && (
        <div className={`p-2 rounded-lg border ${selectedColor}`}>
          <Icon className="h-5 w-5" />
        </div>
      )}
    </div>
  );
}

export default MetricCard;
