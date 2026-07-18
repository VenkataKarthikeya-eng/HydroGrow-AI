import React from 'react';
import { Award, ShieldAlert, Sparkles } from 'lucide-react';

function HealthScoreCard({ score }) {
  const getCategoryInfo = (val) => {
    if (val >= 85) {
      return {
        label: 'Excellent',
        desc: 'Highly active leaf transpiration and optimal nutrient absorption.',
        color: 'text-emerald-400 border-emerald-500/20 bg-emerald-500/5',
        icon: Sparkles
      };
    } else if (val >= 70) {
      return {
        label: 'Good',
        desc: 'Minor developmental stress. Check parameter tolerances.',
        color: 'text-teal-400 border-teal-500/20 bg-teal-500/5',
        icon: Award
      };
    } else if (val >= 50) {
      return {
        label: 'Warning',
        desc: 'Moderate leaf chlorosis or nutrient imbalance detected.',
        color: 'text-amber-400 border-amber-500/20 bg-amber-500/5',
        icon: ShieldAlert
      };
    } else {
      return {
        label: 'Critical',
        desc: 'Severe disease detection. Automation system has triggered mitigation safety overrides.',
        color: 'text-rose-400 border-rose-500/20 bg-rose-500/5',
        icon: ShieldAlert
      };
    }
  };

  const info = getCategoryInfo(score);
  const IconComponent = info.icon;

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-6 flex flex-col justify-between h-full">
      <div>
        <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Health Index Score</h4>
        <p className="text-[10px] text-slate-500 font-semibold">Consolidated crop health diagnostic analysis</p>
      </div>

      <div className="flex flex-col items-center justify-center space-y-4">
        <div className="relative flex items-center justify-center h-32 w-32 rounded-full border border-slate-900 bg-slate-950/40 shadow-inner">
          <svg className="absolute w-full h-full transform -rotate-90">
            <circle
              cx="64"
              cy="64"
              r="52"
              stroke="#0f172a"
              strokeWidth="6"
              fill="transparent"
            />
            <circle
              cx="64"
              cy="64"
              r="52"
              stroke={score >= 85 ? "#34d399" : score >= 70 ? "#2dd4bf" : score >= 50 ? "#fbbf24" : "#f87171"}
              strokeWidth="7"
              fill="transparent"
              strokeDasharray={2 * Math.PI * 52}
              strokeDashoffset={2 * Math.PI * 52 * (1 - score / 100)}
              className="transition-all duration-1000 ease-out"
            />
          </svg>
          <div className="text-center space-y-0.5">
            <span className="text-2xl font-black text-white leading-none">{score}%</span>
            <span className="text-[8px] text-slate-500 uppercase font-black tracking-wider block">Health Rating</span>
          </div>
        </div>

        <div className={`w-full p-3.5 border rounded-2xl flex gap-2.5 items-start ${info.color}`}>
          <IconComponent className="h-5 w-5 flex-shrink-0 mt-0.5" />
          <div className="space-y-0.5">
            <span className="text-[10px] uppercase font-black block tracking-wider leading-none">{info.label}</span>
            <p className="text-[10px] text-slate-355 leading-relaxed font-semibold">{info.desc}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HealthScoreCard;
