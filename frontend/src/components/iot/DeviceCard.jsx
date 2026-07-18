import React from 'react';
import { Cpu, MapPin } from 'lucide-react';

function DeviceCard({ device }) {
  if (!device) return null;

  return (
    <div className="glass-panel p-5 rounded-2xl border border-slate-900 bg-slate-950/20 shadow-md flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="p-2.5 bg-emerald-500/5 border border-emerald-500/10 text-emerald-400 rounded-xl">
          <Cpu className="h-5 w-5 animate-pulse" />
        </div>
        <div>
          <span className="text-[11px] font-black text-white uppercase tracking-wider block leading-tight">
            {device.device_name}
          </span>
          <span className="text-[9px] text-slate-500 font-bold uppercase block tracking-wider mt-0.5">
            ID: {device.id} • {device.device_type}
          </span>
        </div>
      </div>

      <div className="text-right">
        <span className="text-[9px] text-slate-500 font-bold uppercase tracking-wider flex items-center gap-1 justify-end">
          <MapPin className="h-3 w-3 text-emerald-400" /> {device.location}
        </span>
        <span className="text-[8px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-bold uppercase tracking-wider mt-1.5 inline-block">
          {device.status || 'active'}
        </span>
      </div>
    </div>
  );
}

export default DeviceCard;
