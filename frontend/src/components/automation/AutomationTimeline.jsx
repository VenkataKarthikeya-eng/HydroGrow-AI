import React from 'react';
import { Clock } from 'lucide-react';

function AutomationTimeline({ events }) {
  const formatTime = (isoString) => {
    if (!isoString) return '';
    try {
      const d = new Date(isoString);
      return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    } catch (e) {
      return '';
    }
  };

  return (
    <div className="glass-panel p-6 rounded-2xl border border-slate-900 bg-slate-950/20 shadow-lg flex flex-col justify-between h-full">
      <div className="mb-4">
        <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Actuator Event Logs</h4>
        <p className="text-[10px] text-slate-500">Live operational decisions matching logic triggers</p>
      </div>

      <div className="flex-grow space-y-3 overflow-y-auto max-h-[300px] pr-1 scrollbar-thin">
        {!events || events.length === 0 ? (
          <div className="py-12 text-center text-slate-500 text-xs font-semibold">
            No actuation events logged yet. Trigger simulation readings.
          </div>
        ) : (
          events.map((e, index) => (
            <div key={e.id || index} className="flex gap-3 items-start border-l-2 border-emerald-500/20 pl-4 relative ml-2 py-1">
              <div className="absolute h-1.5 w-1.5 rounded-full bg-emerald-500 border border-emerald-400 -left-[4px] top-2.5" />
              
              <div className="space-y-1 flex-grow">
                <div className="flex justify-between items-center gap-2">
                  <span className="text-[9px] px-2 py-0.5 bg-emerald-500/10 border border-emerald-500/20 rounded text-emerald-400 font-extrabold uppercase tracking-wide">
                    {e.status || 'executed'}
                  </span>
                  <span className="text-[8px] text-slate-500 font-bold uppercase flex items-center gap-0.5">
                    <Clock className="h-2.5 w-2.5" /> {formatTime(e.created_at)}
                  </span>
                </div>
                <p className="text-[10px] text-slate-350 font-semibold leading-normal">
                  {e.message}
                </p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default AutomationTimeline;
