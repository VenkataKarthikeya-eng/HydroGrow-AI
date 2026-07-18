import React from 'react';
import { Cpu, Play, CheckCircle2, TrendingUp, AlertTriangle } from 'lucide-react';

function MLOpsDashboard({ mlopsData, onRetrainTriggered }) {
  const data = mlopsData || {
    total_inference_calls: 124,
    average_confidence: 94.2,
    average_latency_ms: 1.85,
    accuracy_drift_detected: false,
    drift_score: 0.02
  };

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-4">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">MLOps Lifecycle & Data Drift Monitor</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Automated retraining triggers & accuracy monitoring</p>
        </div>
        <Cpu className="h-4 w-4 text-emerald-400" />
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div className="p-3 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1">
          <span className="text-[9px] font-black uppercase text-slate-500 block">Avg Confidence</span>
          <span className="text-sm font-mono font-black text-emerald-400">{data.average_confidence}%</span>
        </div>

        <div className="p-3 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1">
          <span className="text-[9px] font-black uppercase text-slate-500 block">Inference Latency</span>
          <span className="text-sm font-mono font-black text-emerald-400">{data.average_latency_ms} ms</span>
        </div>

        <div className="p-3 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1">
          <span className="text-[9px] font-black uppercase text-slate-500 block">Data Drift Score</span>
          <span className="text-sm font-mono font-black text-emerald-400">{data.drift_score}</span>
        </div>

        <div className="p-3 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1">
          <span className="text-[9px] font-black uppercase text-slate-500 block">Drift Alert</span>
          <span className="text-xs font-bold text-emerald-400">
            {data.accuracy_drift_detected ? "Alert Active" : "Nominal (No Drift)"}
          </span>
        </div>
      </div>
    </div>
  );
}

export default MLOpsDashboard;
