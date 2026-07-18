import React from 'react';
import { Cpu, CheckCircle2, AlertTriangle, ShieldAlert } from 'lucide-react';

function AgentStatusCard({ statuses }) {
  const agentsList = [
    { name: "CropAgent", label: "Crop Lifecycle Agent", desc: "Vigor & Biomass" },
    { name: "ClimateAgent", label: "Climate & Stress Agent", desc: "Heat & Transpiration" },
    { name: "DiseaseAgent", label: "Disease Pathology Agent", desc: "Leaf Scans Diagnostic" },
    { name: "NutritionAgent", label: "Nutrition Dosing Agent", desc: "EC & pH Drift" },
    { name: "OptimizationAgent", label: "Yield Optimization Agent", desc: "Energy & Harvest" }
  ];

  const getStatus = (name) => {
    if (!statuses) return { status: "Active", priority: "LOW" };
    const match = statuses.find(s => s.agent_name === name);
    return match || { status: "Active", priority: "LOW" };
  };

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-4">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Multi-Agent Subsystem Grid</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Active autonomous AI decision agents</p>
        </div>
        <Cpu className="h-4 w-4 text-emerald-400" />
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
        {agentsList.map(agent => {
          const st = getStatus(agent.name);
          const isCritical = st.priority === "CRITICAL";
          const isHigh = st.priority === "HIGH";
          const isMedium = st.priority === "MEDIUM";

          return (
            <div 
              key={agent.name}
              className={`p-3 rounded-2xl border transition-all ${
                isCritical 
                  ? 'bg-rose-500/5 border-rose-500/20 text-rose-400' 
                  : isHigh 
                  ? 'bg-amber-500/5 border-amber-500/20 text-amber-400' 
                  : isMedium 
                  ? 'bg-yellow-500/5 border-yellow-500/20 text-yellow-400' 
                  : 'bg-slate-950/40 border-slate-900 text-slate-300'
              }`}
            >
              <div className="flex justify-between items-center mb-1">
                <span className="text-[9px] font-black uppercase tracking-wider text-slate-400 truncate">{agent.name}</span>
                {isCritical ? (
                  <ShieldAlert className="h-3.5 w-3.5 text-rose-500 animate-pulse shrink-0" />
                ) : isHigh || isMedium ? (
                  <AlertTriangle className="h-3.5 w-3.5 text-amber-400 shrink-0" />
                ) : (
                  <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400 shrink-0" />
                )}
              </div>
              <p className="text-[11px] font-black leading-tight text-slate-200">{agent.label}</p>
              <p className="text-[8px] text-slate-500 font-semibold mt-0.5">{agent.desc}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default AgentStatusCard;
