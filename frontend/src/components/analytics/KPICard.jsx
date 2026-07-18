import React from 'react';

function KPICard({ title, value, unit = '', change = '', changeType = 'positive', icon: Icon }) {
  const isPositive = changeType === 'positive';
  
  return (
    <div className="glass-panel p-5 rounded-2xl border border-slate-900 bg-slate-950/20 shadow-lg relative overflow-hidden flex flex-col justify-between min-h-[110px]">
      <div className="flex justify-between items-start">
        <div>
          <span className="text-[10px] font-black uppercase text-slate-500 tracking-wider block leading-none">{title}</span>
          <h3 className="text-2xl font-black text-white mt-2 tracking-tight leading-none">
            {value}
            {unit && <span className="text-xs font-bold text-slate-400 ml-1">{unit}</span>}
          </h3>
        </div>
        {Icon && (
          <div className="p-2 rounded-lg bg-slate-900 border border-slate-850 text-emerald-400">
            <Icon className="h-4 w-4" />
          </div>
        )}
      </div>

      {change && (
        <div className="flex items-center gap-1 mt-3 text-[10px] font-semibold leading-none">
          <span className={isPositive ? 'text-emerald-400' : 'text-rose-400'}>
            {isPositive ? '▲' : '▼'} {change}
          </span>
          <span className="text-slate-500 font-medium">vs benchmark</span>
        </div>
      )}
    </div>
  );
}

export default KPICard;
