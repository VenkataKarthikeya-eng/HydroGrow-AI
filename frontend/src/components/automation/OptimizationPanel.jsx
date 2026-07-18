import React from 'react';
import { Lightbulb, Droplets, Zap, Bot } from 'lucide-react';

function OptimizationPanel({ recommendations }) {
  const hasData = recommendations && Object.keys(recommendations).length > 0;

  if (!hasData) {
    return (
      <div className="glass-panel p-6 rounded-2xl border border-slate-900 bg-slate-950/20 shadow-lg text-center text-slate-500 text-xs font-semibold py-12">
        No suggestions resolved yet.
      </div>
    );
  }

  const renderSection = (title, items, Icon, colorClass) => {
    return (
      <div className="space-y-2">
        <span className={`text-[9px] font-black uppercase tracking-wider flex items-center gap-1 ${colorClass}`}>
          <Icon className="h-3.5 w-3.5" /> {title}
        </span>
        <div className="space-y-2">
          {items.map((it, idx) => (
            <div key={idx} className="p-3 bg-slate-950/40 border border-slate-900 rounded-xl hover:border-slate-850 transition-colors">
              <span className="text-[11px] font-semibold text-slate-200 block leading-tight">{it.suggestion}</span>
              <span className="text-[9px] text-slate-500 font-bold block mt-1 uppercase tracking-wide">Impact: {it.impact}</span>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-lg space-y-6 h-full">
      <div className="flex items-center gap-2 border-b border-slate-900 pb-3">
        <Bot className="h-5 w-5 text-emerald-400" />
        <div>
          <h4 className="text-xs font-black uppercase text-white tracking-wider">AI Copilot Recommendations</h4>
          <p className="text-[10px] text-slate-500">Real-time suggestions calculated from current crops telemetry</p>
        </div>
      </div>

      <div className="space-y-5">
        {recommendations.yield_improvement?.length > 0 && 
          renderSection('Yield Enhancements', recommendations.yield_improvement, Lightbulb, 'text-emerald-400')
        }
        {recommendations.nutrient_optimization?.length > 0 && 
          renderSection('Nutrient Recipes', recommendations.nutrient_optimization, Zap, 'text-teal-400')
        }
        {recommendations.water_saving?.length > 0 && 
          renderSection('Water Operations', recommendations.water_saving, Droplets, 'text-sky-400')
        }
      </div>
    </div>
  );
}

export default OptimizationPanel;
