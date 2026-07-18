import React from 'react';
import { CheckSquare } from 'lucide-react';

function RecommendationPanel({ recommendations }) {
  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-4">
      <div>
        <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">AI Crop Recovery Actions</h4>
        <p className="text-[10px] text-slate-500 font-semibold">Immediate adjustments suggested by the agronomic advisor</p>
      </div>

      <div className="space-y-3">
        {!recommendations || recommendations.length === 0 ? (
          <div className="p-4 text-center text-slate-500 text-xs font-semibold py-8 bg-slate-950/40 border border-slate-900 rounded-2xl">
            No recovery actions needed. Crop health is optimal!
          </div>
        ) : (
          recommendations.map((rec, index) => (
            <div key={index} className="flex gap-3 items-start p-3 bg-slate-950/40 border border-slate-900 rounded-2xl hover:border-slate-850 transition-colors">
              <CheckSquare className="h-4.5 w-4.5 text-emerald-400 mt-0.5 flex-shrink-0" />
              <p className="text-[10px] text-slate-300 font-semibold leading-normal">{rec}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default RecommendationPanel;
