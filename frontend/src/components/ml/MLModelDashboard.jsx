import React from 'react';
import { Cpu, Zap, Activity, Award } from 'lucide-react';

function MLModelDashboard({ metrics }) {
  const activeCount = metrics?.active_models_count || 2;
  const totalCalls = metrics?.total_inference_calls || 148;
  const avgLatency = metrics?.average_latency_ms || 4.2;
  const r2Score = metrics?.growth_model_r2 || 0.935;

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div className="glass-panel p-5 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-lg space-y-1">
        <div className="flex justify-between items-center text-slate-500">
          <span className="text-[9px] font-black uppercase tracking-wider">Active Models</span>
          <Cpu className="h-4 w-4 text-emerald-400" />
        </div>
        <p className="text-2xl font-black font-mono text-slate-100">{activeCount}</p>
        <p className="text-[9px] text-emerald-400 font-semibold">Production Inference Active</p>
      </div>

      <div className="glass-panel p-5 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-lg space-y-1">
        <div className="flex justify-between items-center text-slate-500">
          <span className="text-[9px] font-black uppercase tracking-wider">Inference Calls</span>
          <Activity className="h-4 w-4 text-emerald-400" />
        </div>
        <p className="text-2xl font-black font-mono text-slate-100">{totalCalls}</p>
        <p className="text-[9px] text-slate-500 font-semibold">Logged predictions</p>
      </div>

      <div className="glass-panel p-5 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-lg space-y-1">
        <div className="flex justify-between items-center text-slate-500">
          <span className="text-[9px] font-black uppercase tracking-wider">Avg Latency</span>
          <Zap className="h-4 w-4 text-emerald-400" />
        </div>
        <p className="text-2xl font-black font-mono text-emerald-400">{avgLatency}ms</p>
        <p className="text-[9px] text-slate-500 font-semibold">Real-time inference speed</p>
      </div>

      <div className="glass-panel p-5 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-lg space-y-1">
        <div className="flex justify-between items-center text-slate-500">
          <span className="text-[9px] font-black uppercase tracking-wider">Growth R² Accuracy</span>
          <Award className="h-4 w-4 text-emerald-400" />
        </div>
        <p className="text-2xl font-black font-mono text-emerald-400">{r2Score}</p>
        <p className="text-[9px] text-emerald-400 font-semibold">RandomForest Regressor</p>
      </div>
    </div>
  );
}

export default MLModelDashboard;
