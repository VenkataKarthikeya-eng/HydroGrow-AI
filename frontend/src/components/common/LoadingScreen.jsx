import React from 'react';
import { Sprout, Activity } from 'lucide-react';

function LoadingScreen({ message = "Initializing HydroGrow AI Intelligence Deck..." }) {
  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-6 text-center text-slate-100">
      <div className="relative flex items-center justify-center mb-6">
        <div className="absolute h-20 w-20 rounded-full bg-emerald-500/10 animate-ping" />
        <div className="p-5 rounded-3xl bg-slate-900 border border-slate-800 text-emerald-400 shadow-2xl relative">
          <Sprout className="h-10 w-10 animate-pulse" />
        </div>
      </div>
      <h3 className="text-lg font-black text-slate-100 mb-1 tracking-tight">HydroGrow AI</h3>
      <p className="text-xs text-slate-400 max-w-xs font-medium flex items-center justify-center gap-2">
        <Activity className="h-3.5 w-3.5 text-emerald-400 animate-spin" />
        {message}
      </p>
    </div>
  );
}

export default LoadingScreen;
