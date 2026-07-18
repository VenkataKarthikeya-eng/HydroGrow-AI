import React from 'react';
import { AlertCircle, ShieldAlert, CheckCircle } from 'lucide-react';

function AlertCard({ anomalies }) {
  const hasAnomalies = anomalies && anomalies.length > 0;

  return (
    <div className="glass-panel p-6 rounded-2xl border border-slate-900 bg-slate-950/20 shadow-lg h-full flex flex-col justify-between">
      <div className="mb-4">
        <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Active Farm Anomalies</h4>
        <p className="text-[10px] text-slate-500">Real-time environmental warning and critical alerts</p>
      </div>

      <div className="flex-grow space-y-3 overflow-y-auto max-h-[220px] pr-1 scrollbar-thin">
        {!hasAnomalies ? (
          <div className="flex flex-col items-center justify-center text-center py-8">
            <CheckCircle className="h-8 w-8 text-emerald-500 mb-2" />
            <span className="text-slate-300 text-xs font-bold block">All Systems Optimal</span>
            <p className="text-[9px] text-slate-500 max-w-[180px] mt-1">
              No anomalies, sudden drops, or extreme parameters found.
            </p>
          </div>
        ) : (
          anomalies.map((a, i) => {
            const isCritical = a.severity === 'critical';
            return (
              <div
                key={i}
                className={`p-3 rounded-xl border flex items-start gap-2.5 transition-all ${
                  isCritical 
                    ? 'bg-rose-500/5 border-rose-500/10 text-rose-300' 
                    : 'bg-amber-500/5 border-amber-500/10 text-amber-300'
                }`}
              >
                {isCritical ? (
                  <ShieldAlert className="h-4 w-4 shrink-0 text-rose-450 mt-0.5" />
                ) : (
                  <AlertCircle className="h-4 w-4 shrink-0 text-amber-400 mt-0.5" />
                )}
                <div className="space-y-0.5">
                  <span className="text-[11px] font-bold block leading-tight">{a.alert}</span>
                  <p className="text-[10px] text-slate-400 leading-normal font-medium">{a.reason}</p>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

export default AlertCard;
