import React, { useState } from 'react';
import client from '../../api/client';
import { Cpu, CheckCircle2, RotateCcw, Award } from 'lucide-react';

function ModelCard({ model, onModelUpdated }) {
  const [activating, setActivating] = useState(false);
  const isActive = model.status === 'Active';

  const handleActivate = async () => {
    if (!model.id || isActive) return;
    setActivating(true);
    try {
      await client.post(`/api/ml/rollback/${model.id}`);
      if (onModelUpdated) onModelUpdated();
    } catch (err) {
      // handle error
    } finally {
      setActivating(false);
    }
  };

  return (
    <div className={`p-5 rounded-3xl border transition-all ${
      isActive 
        ? 'bg-emerald-950/10 border-emerald-500/30 shadow-emerald-950/10' 
        : 'bg-slate-950/30 border-slate-900'
    } shadow-lg space-y-3`}>
      <div className="flex justify-between items-start">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className={`px-2 py-0.5 rounded text-[8px] font-black uppercase tracking-wider ${
              isActive ? 'bg-emerald-500/20 text-emerald-400' : 'bg-slate-800 text-slate-400'
            }`}>
              {model.status}
            </span>
            <span className="text-[9px] font-black uppercase text-slate-500 tracking-wider">
              {model.model_type}
            </span>
          </div>
          <h4 className="text-sm font-extrabold text-slate-100">{model.model_name}</h4>
        </div>
        <div className="text-right">
          <span className="text-xs font-mono font-black text-emerald-400">{model.version}</span>
          <span className="text-[8px] uppercase tracking-wider text-slate-500 block font-bold">Version</span>
        </div>
      </div>

      <div className="space-y-2 text-xs">
        <div className="p-3 bg-slate-950/50 rounded-2xl border border-slate-900/60 flex justify-between items-center">
          <div>
            <p className="text-[9px] uppercase tracking-wider text-slate-500 font-black">Algorithm</p>
            <p className="font-bold text-slate-200">{model.algorithm}</p>
          </div>
          <div className="text-right">
            <p className="text-[9px] uppercase tracking-wider text-slate-500 font-black">R² / Accuracy Score</p>
            <p className="font-mono font-black text-emerald-400 flex items-center gap-1 justify-end">
              <Award className="h-3.5 w-3.5" />
              {model.accuracy_score}
            </p>
          </div>
        </div>

        <div className="p-2.5 bg-slate-950/30 rounded-xl text-[10px] text-slate-400 font-medium truncate">
          Dataset: {model.training_dataset}
        </div>
      </div>

      <div className="border-t border-slate-900/60 pt-3 flex justify-between items-center">
        <span className="text-[9px] font-mono text-slate-500">ID: #{model.id}</span>
        {isActive ? (
          <span className="text-[10px] font-black uppercase tracking-wider text-emerald-400 flex items-center gap-1">
            <CheckCircle2 className="h-3.5 w-3.5" /> Active Production Model
          </span>
        ) : (
          <button
            onClick={handleActivate}
            disabled={activating}
            className="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-850 text-slate-200 border border-slate-800 text-[10px] font-black uppercase tracking-wider transition-all flex items-center gap-1 active:scale-95"
          >
            <RotateCcw className="h-3 w-3 text-emerald-400" />
            {activating ? 'Activating...' : 'Activate Version'}
          </button>
        )}
      </div>
    </div>
  );
}

export default ModelCard;
