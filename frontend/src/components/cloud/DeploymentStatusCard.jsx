import React from 'react';
import { Cloud, Database, Cpu, Radio, ShieldCheck } from 'lucide-react';

function DeploymentStatusCard({ statusData }) {
  const status = statusData || {
    status: "online",
    services: {
      api_backend: "online",
      database: "online",
      cloud_storage: "active (AWS S3)",
      mqtt_broker: "connected"
    },
    active_devices_count: 3,
    region: "us-east-1 / AWS Cloud compatible"
  };

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-4">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Cloud Deployment Status & Gateway</h4>
          <p className="text-[10px] text-slate-500 font-semibold">{status.region}</p>
        </div>
        <Cloud className="h-4 w-4 text-emerald-400" />
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div className="p-3 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1">
          <span className="text-[9px] font-black uppercase text-slate-500 block">FastAPI Backend</span>
          <div className="flex items-center gap-1.5">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-xs font-bold text-slate-200 capitalize">{status.services?.api_backend || "online"}</span>
          </div>
        </div>

        <div className="p-3 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1">
          <span className="text-[9px] font-black uppercase text-slate-500 block">Managed DB</span>
          <div className="flex items-center gap-1.5">
            <span className="h-2 w-2 rounded-full bg-emerald-400" />
            <span className="text-xs font-bold text-slate-200 capitalize">{status.services?.database || "online"}</span>
          </div>
        </div>

        <div className="p-3 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1">
          <span className="text-[9px] font-black uppercase text-slate-500 block">Cloud Storage</span>
          <div className="flex items-center gap-1.5">
            <span className="h-2 w-2 rounded-full bg-emerald-400" />
            <span className="text-xs font-bold text-slate-200 truncate">{status.services?.cloud_storage || "active"}</span>
          </div>
        </div>

        <div className="p-3 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1">
          <span className="text-[9px] font-black uppercase text-slate-500 block">MQTT Broker</span>
          <div className="flex items-center gap-1.5">
            <span className="h-2 w-2 rounded-full bg-emerald-400" />
            <span className="text-xs font-bold text-slate-200 truncate">{status.services?.mqtt_broker || "connected"}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DeploymentStatusCard;
