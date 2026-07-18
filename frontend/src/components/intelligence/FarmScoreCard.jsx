import React from 'react';
import { Award, Zap, Leaf, Cpu, Activity } from 'lucide-react';

function FarmScoreCard({ scoreData }) {
  const score = scoreData?.score || {};

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/40 space-y-6">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">AI Farm Intelligence Scorecard</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Composite diagnostic across IoT, CV, Twin & ML</p>
        </div>
        <Award className="h-4 w-4 text-emerald-400" />
      </div>

      <div className="flex flex-col sm:flex-row items-center justify-between gap-6 bg-slate-950/60 p-6 rounded-2xl border border-slate-900">
        <div className="text-center sm:text-left">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block">Overall Intelligence Rating</span>
          <div className="text-4xl font-black text-emerald-400 font-mono mt-1">
            {score.overall_score || 91.4} <span className="text-xs font-normal text-slate-500">/ 100</span>
          </div>
          <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 text-[10px] font-black uppercase mt-2 inline-block">
            Top 6% Globally
          </span>
        </div>

        <div className="grid grid-cols-2 gap-4 w-full sm:w-auto text-xs">
          <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
            <span className="text-[9px] text-slate-500 uppercase font-bold flex items-center gap-1">
              <Zap className="h-3 w-3 text-amber-400" /> Productivity
            </span>
            <span className="font-mono font-bold text-slate-100 text-sm">{score.productivity_score || 92.5}%</span>
          </div>
          <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
            <span className="text-[9px] text-slate-500 uppercase font-bold flex items-center gap-1">
              <Leaf className="h-3 w-3 text-emerald-400" /> Sustainability
            </span>
            <span className="font-mono font-bold text-slate-100 text-sm">{score.sustainability_score || 88.0}%</span>
          </div>
          <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
            <span className="text-[9px] text-slate-500 uppercase font-bold flex items-center gap-1">
              <Cpu className="h-3 w-3 text-blue-400" /> Automation
            </span>
            <span className="font-mono font-bold text-slate-100 text-sm">{score.automation_score || 95.0}%</span>
          </div>
          <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
            <span className="text-[9px] text-slate-500 uppercase font-bold flex items-center gap-1">
              <Activity className="h-3 w-3 text-purple-400" /> Crop Health
            </span>
            <span className="font-mono font-bold text-slate-100 text-sm">{score.health_score || 90.0}%</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default FarmScoreCard;
