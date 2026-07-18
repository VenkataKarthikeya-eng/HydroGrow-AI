import React from 'react';
import { Calendar, Heart, ShieldAlert, ChevronRight } from 'lucide-react';

function VisionHistory({ scans, onSelectScan, selectedId }) {
  const formatDate = (isoString) => {
    if (!isoString) return '';
    try {
      const d = new Date(isoString);
      return d.toLocaleDateString([], { month: 'short', day: 'numeric' }) + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch (e) {
      return '';
    }
  };

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-4">
      <div>
        <h3 className="text-xs font-black uppercase text-white tracking-wider">Crop Scan History</h3>
        <p className="text-[10px] text-slate-500 font-semibold">List of previously uploaded crop image diagnostics</p>
      </div>

      <div className="space-y-3 max-h-[300px] overflow-y-auto pr-1 scrollbar-thin">
        {!scans || scans.length === 0 ? (
          <div className="py-12 text-center text-slate-500 text-xs font-medium bg-slate-950/40 border border-slate-900 rounded-2xl">
            No previous scans logged. Upload a crop photo to start.
          </div>
        ) : (
          scans.map((s) => {
            const isSelected = selectedId === s.id;
            const isHealthy = s.disease === 'Healthy';
            return (
              <div
                key={s.id}
                onClick={() => onSelectScan(s.id)}
                className={`flex justify-between items-center p-3 rounded-2xl cursor-pointer border transition-all ${
                  isSelected 
                    ? 'bg-emerald-500/5 border-emerald-500/20' 
                    : 'bg-slate-950/40 border-slate-900 hover:border-slate-800'
                }`}
              >
                <div className="flex gap-3 items-center">
                  <div className={`p-2 rounded-xl ${
                    isHealthy ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'
                  }`}>
                    {isHealthy ? <Heart className="h-4.5 w-4.5" /> : <ShieldAlert className="h-4.5 w-4.5" />}
                  </div>
                  <div>
                    <span className="text-[10px] font-black text-white uppercase block leading-tight">
                      {s.disease}
                    </span>
                    <span className="text-[8px] text-slate-500 font-bold uppercase mt-0.5 block flex items-center gap-0.5">
                      <Calendar className="h-2.5 w-2.5" /> {formatDate(s.uploaded_at)}
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <span className="font-mono text-[10px] font-black text-slate-350 bg-slate-950/60 border border-slate-900 px-2 py-0.5 rounded-lg">
                    {s.health_score}%
                  </span>
                  <ChevronRight className="h-4 w-4 text-slate-500" />
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

export default VisionHistory;
