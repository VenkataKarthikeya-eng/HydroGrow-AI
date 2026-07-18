import React from 'react';
import { ShieldAlert, AlertCircle, CheckCircle, Clock } from 'lucide-react';

function AlertPanel({ alerts }) {
  const hasAlerts = alerts && alerts.length > 0;

  const formatTime = (isoString) => {
    if (!isoString) return 'Just now';
    try {
      const d = new Date(isoString);
      return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch (e) {
      return 'Just now';
    }
  };

  return (
    <div className="glass-panel p-6 rounded-2xl border border-slate-900 bg-slate-950/20 shadow-lg h-full flex flex-col justify-between">
      <div className="mb-4">
        <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Active Device Warnings</h4>
        <p className="text-[10px] text-slate-500">Real-time alerts triggered by threshold violations</p>
      </div>

      <div className="flex-grow space-y-2.5 overflow-y-auto max-h-[220px] pr-1 scrollbar-thin">
        {!hasAlerts ? (
          <div className="flex flex-col items-center justify-center text-center py-8">
            <CheckCircle className="h-8 w-8 text-emerald-500 mb-2" />
            <span className="text-slate-300 text-xs font-bold block">All Systems Optimal</span>
            <p className="text-[9px] text-slate-500 max-w-[185px] mt-1 font-semibold">
              No threshold spikes, pH imbalances, or water temperature stresses.
            </p>
          </div>
        ) : (
          alerts.map((a, i) => {
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
                  <AlertCircle className="h-4 w-4 shrink-0 text-amber-450 mt-0.5" />
                )}
                <div className="space-y-0.5 flex-grow">
                  <div className="flex justify-between items-start gap-1">
                    <span className="text-[11px] font-bold block leading-tight">{a.parameter} Alert</span>
                    <span className="text-[8px] text-slate-500 font-bold uppercase shrink-0 flex items-center gap-0.5">
                      <Clock className="h-2.5 w-2.5" /> {formatTime(a.created_at)}
                    </span>
                  </div>
                  <p className="text-[10px] text-slate-400 leading-normal font-semibold">{a.message}</p>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

export default AlertPanel;
