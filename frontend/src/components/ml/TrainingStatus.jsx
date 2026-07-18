import React, { useState } from 'react';
import client from '../../api/client';
import { Play, CheckCircle2, RotateCw, Cpu } from 'lucide-react';

function TrainingStatus({ onTrainingComplete }) {
  const [training, setTraining] = useState(false);
  const [msg, setMsg] = useState('');

  const handleStartTraining = async () => {
    setTraining(true);
    setMsg('Initiating background re-training pipeline...');
    try {
      const res = await client.post('/api/ml/train');
      setMsg(res.data.message || 'Training pipeline initiated successfully.');
      setTimeout(() => {
        setTraining(false);
        if (onTrainingComplete) onTrainingComplete();
      }, 2500);
    } catch (err) {
      setMsg('Failed to trigger training pipeline.');
      setTraining(false);
    }
  };

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-4">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Automated Background Training Pipeline</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Non-blocking background model re-training & hyperparameter fitting</p>
        </div>
        <Cpu className="h-4 w-4 text-emerald-400" />
      </div>

      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 p-4 rounded-2xl bg-slate-950/40 border border-slate-900">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className={`h-2 w-2 rounded-full ${training ? 'bg-amber-400 animate-ping' : 'bg-emerald-400'}`} />
            <span className="text-xs font-bold text-slate-200">
              {training ? 'Background Training Active' : 'Model Pipeline Ready'}
            </span>
          </div>
          <p className="text-[10px] text-slate-400">{msg || 'Click trigger to train a new model version on fresh telemetry.'}</p>
        </div>

        <button
          onClick={handleStartTraining}
          disabled={training}
          className="px-4 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase tracking-wider transition-all shadow-md active:scale-95 flex items-center gap-2 shrink-0 justify-center"
        >
          {training ? (
            <>
              <RotateCw className="h-4 w-4 animate-spin" />
              Training Model...
            </>
          ) : (
            <>
              <Play className="h-4 w-4 fill-current" />
              Train New Version
            </>
          )}
        </button>
      </div>
    </div>
  );
}

export default TrainingStatus;
