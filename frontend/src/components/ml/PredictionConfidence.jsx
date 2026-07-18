import React from 'react';
import { ShieldCheck } from 'lucide-react';

function PredictionConfidence({ metrics }) {
  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-4">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Production Confidence Index</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Model certainty rating across active inference predictors</p>
        </div>
        <ShieldCheck className="h-4 w-4 text-emerald-400" />
      </div>

      <div className="space-y-3">
        <div className="flex justify-between items-center text-xs">
          <span className="font-bold text-slate-300">Growth Biomass Predictor Confidence</span>
          <span className="font-mono font-black text-emerald-400">93.5%</span>
        </div>
        <div className="w-full h-2 rounded-full bg-slate-900 overflow-hidden">
          <div className="h-full bg-emerald-500 rounded-full transition-all duration-1000" style={{ width: '93.5%' }} />
        </div>

        <div className="flex justify-between items-center text-xs pt-1">
          <span className="font-bold text-slate-300">Pathology Disease Classifier Certainty</span>
          <span className="font-mono font-black text-emerald-400">96.0%</span>
        </div>
        <div className="w-full h-2 rounded-full bg-slate-900 overflow-hidden">
          <div className="h-full bg-emerald-500 rounded-full transition-all duration-1000" style={{ width: '96.0%' }} />
        </div>
      </div>
    </div>
  );
}

export default PredictionConfidence;
