import React from 'react';
import { ShieldAlert, AlertTriangle, CheckCircle } from 'lucide-react';

function SensorCard({ title, value, unit, icon: Icon, alert }) {
  const isCritical = alert?.severity === 'critical';
  const isWarning = alert?.severity === 'warning';

  return (
    <div className={`glass-panel p-5 rounded-2xl border transition-all ${
      isCritical 
        ? 'border-rose-500/20 bg-rose-950/5 shadow-rose-950/5' 
        : isWarning 
        ? 'border-amber-500/20 bg-amber-950/5 shadow-amber-950/5' 
        : 'border-slate-900 bg-slate-950/20 hover:border-slate-850'
    } shadow-md flex flex-col justify-between h-[130px]`}>
      <div className="flex justify-between items-start">
        <div className="flex items-center gap-2">
          <div className={`p-1.5 rounded-lg border ${
            isCritical 
              ? 'bg-rose-500/10 border-rose-500/20 text-rose-400' 
              : isWarning 
              ? 'bg-amber-500/10 border-amber-500/20 text-amber-400' 
              : 'bg-emerald-500/5 border-emerald-500/10 text-emerald-400'
          }`}>
            <Icon className="h-4 w-4" />
          </div>
          <span className="text-[10px] font-black uppercase text-slate-400 tracking-wider leading-none">{title}</span>
        </div>

        {isCritical ? (
          <ShieldAlert className="h-4.5 w-4.5 text-rose-500 animate-pulse" />
        ) : isWarning ? (
          <AlertTriangle className="h-4.5 w-4.5 text-amber-500 animate-pulse" />
        ) : (
          <CheckCircle className="h-4.5 w-4.5 text-emerald-500/30" />
        )}
      </div>

      <div className="mt-3">
        <div className="flex items-baseline gap-1">
          <span className={`text-2xl font-black font-mono leading-none tracking-tight ${
            isCritical ? 'text-rose-400' : isWarning ? 'text-amber-400' : 'text-white'
          }`}>
            {value !== undefined ? value : '--'}
          </span>
          <span className="text-[10px] text-slate-500 font-bold uppercase">{unit}</span>
        </div>
        <p className="text-[9px] text-slate-500 mt-1 font-semibold leading-tight truncate">
          {alert ? alert.message : 'Optimal reading'}
        </p>
      </div>
    </div>
  );
}

export default SensorCard;
