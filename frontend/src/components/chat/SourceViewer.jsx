import React from 'react';
import { X, FileText } from 'lucide-react';

function SourceViewer({ sources, onClose }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm select-none">
      <div onClick={onClose} className="absolute inset-0"></div>
      
      <div className="w-full max-w-lg glass-panel p-6 rounded-3xl border border-slate-800 bg-slate-950 relative z-10 shadow-2xl space-y-4">
        <div className="flex justify-between items-center border-b border-slate-900 pb-3">
          <div className="flex items-center space-x-2">
            <FileText className="h-5 w-5 text-emerald-400" />
            <h3 className="text-sm font-black uppercase text-white tracking-wider">Agronomic References</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-400 hover:text-white transition-all active:scale-95"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <div className="space-y-3 overflow-y-auto max-h-[300px] pr-1 scrollbar-thin">
          {sources.map((src, i) => (
            <div key={i} className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-900 flex items-start space-x-3">
              <div className="p-2 rounded-lg bg-emerald-500/5 text-emerald-400 border border-emerald-500/10 shrink-0">
                <FileText className="h-4 w-4" />
              </div>
              <div className="space-y-1">
                <span className="text-[10px] text-slate-500 font-mono block">Source Document</span>
                <span className="text-slate-200 text-xs font-semibold block">{src}</span>
                <p className="text-[10px] text-slate-400 leading-relaxed font-medium mt-1">
                  Validated against the HydroGrow Localized Knowledge Base protocols and grower-guideline specifications.
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default SourceViewer;
