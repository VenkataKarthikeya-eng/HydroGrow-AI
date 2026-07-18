import React from 'react';
import { History } from 'lucide-react';

function RecommendationTimeline({ decisions }) {
  const formatTime = (ts) => {
    if (!ts) return "Recently";
    try {
      return new Date(ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch {
      return "Recently";
    }
  };

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-4">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">AI Decision History Logs</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Chronological multi-agent recommendations and actions</p>
        </div>
        <History className="h-4 w-4 text-emerald-400" />
      </div>

      <div className="space-y-3 max-h-[280px] overflow-y-auto pr-1 scrollbar-thin">
        {(!decisions || decisions.length === 0) ? (
          <div className="py-12 text-center text-slate-500 text-xs font-semibold">
            No historic copilot decisions recorded yet.
          </div>
        ) : (
          decisions.map((dec, i) => (
            <div key={dec.id || i} className="flex gap-3 items-start border-l-2 border-slate-900 pl-4 relative ml-2 py-1">
              <div className="absolute h-1.5 w-1.5 rounded-full bg-emerald-500 border border-emerald-400 -left-[4px] top-2.5" />
              <div className="space-y-1 flex-grow">
                <div className="flex justify-between items-center gap-2">
                  <span className="text-[9px] font-black uppercase tracking-wider text-slate-400">
                    {dec.decision_type} • {dec.priority}
                  </span>
                  <span className="text-[8px] text-slate-500 font-mono">
                    {formatTime(dec.created_at)}
                  </span>
                </div>
                <p className="text-[11px] font-bold text-slate-200 leading-tight">{dec.title}</p>
                <p className="text-[10px] text-slate-400 leading-normal">{dec.recommended_action}</p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default RecommendationTimeline;
