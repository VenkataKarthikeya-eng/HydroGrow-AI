import React from 'react';
import { Calendar } from 'lucide-react';

function GrowthStageTimeline({ currentStage }) {
  const stages = [
    { name: 'Seedling', duration: 'Days 1-10', desc: 'Germination & cotyledons opening' },
    { name: 'Vegetative', duration: 'Days 11-25', desc: 'Rapid leaf development' },
    { name: 'Maturity', duration: 'Days 26-35', desc: 'Head enlargement & density expansion' },
    { name: 'Harvest Ready', duration: 'Days 36+', desc: 'Max weight & crisp turgidity' }
  ];

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-4">
      <div>
        <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Crop Growth Phase Timeline</h4>
        <p className="text-[10px] text-slate-500 font-semibold">Track estimated developmental stage matching scan size metrics</p>
      </div>

      <div className="relative pl-6 space-y-4 py-1">
        <div className="absolute left-[9px] top-0 bottom-0 w-0.5 bg-slate-900" />

        {stages.map((st, index) => {
          const isCurrent = currentStage === st.name || (currentStage === "Harvest" && st.name === "Harvest Ready") || (currentStage === "Harvest Ready" && st.name === "Harvest Ready");
          return (
            <div key={index} className="relative flex gap-3 items-start">
              <div className={`absolute -left-[22px] h-3 w-3 rounded-full border transition-all ${
                isCurrent 
                  ? 'bg-emerald-400 border-emerald-500 scale-125 shadow-[0_0_8px_rgba(52,211,153,0.4)]' 
                  : 'bg-slate-950 border-slate-800'
              }`} />

              <div className="space-y-0.5 flex-grow">
                <div className="flex justify-between items-center">
                  <span className={`text-[11px] font-black uppercase tracking-wider ${
                    isCurrent ? 'text-emerald-400' : 'text-slate-400'
                  }`}>{st.name}</span>
                  <span className="text-[8px] text-slate-500 font-bold uppercase flex items-center gap-0.5">
                    <Calendar className="h-2.5 w-2.5" /> {st.duration}
                  </span>
                </div>
                <p className="text-[10px] text-slate-500 font-semibold">{st.desc}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default GrowthStageTimeline;
