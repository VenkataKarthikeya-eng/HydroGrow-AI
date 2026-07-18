import React from 'react';
import { Activity, Radio, Droplets, Thermometer, Wind } from 'lucide-react';

function LiveTelemetry({ telemetry }) {
  const data = telemetry || {
    device: "ESP32_001",
    data: {
      water_ph: 6.15,
      water_ec: 1.85,
      temperature: 24.2,
      humidity: 68.0,
      co2: 450,
      nutrient_level: 85
    }
  };

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-4">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Live Hardware Telemetry Stream</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Real-time ESP32/Raspberry Pi MQTT & WebSocket broadcast</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="h-2 w-2 rounded-full bg-emerald-400 animate-ping" />
          <span className="text-[10px] font-mono font-bold text-emerald-400">{data.device || "ESP32_001"}</span>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
        <div className="p-3 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1">
          <span className="text-[9px] font-black uppercase text-slate-500 block">Water pH</span>
          <span className="text-sm font-mono font-black text-emerald-400">{data.data?.water_ph || 6.1} pH</span>
        </div>

        <div className="p-3 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1">
          <span className="text-[9px] font-black uppercase text-slate-500 block">Water EC</span>
          <span className="text-sm font-mono font-black text-emerald-400">{data.data?.water_ec || 1.8} mS/cm</span>
        </div>

        <div className="p-3 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1">
          <span className="text-[9px] font-black uppercase text-slate-500 block">Air Temp</span>
          <span className="text-sm font-mono font-black text-emerald-400">{data.data?.temperature || 24.5} °C</span>
        </div>

        <div className="p-3 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1">
          <span className="text-[9px] font-black uppercase text-slate-500 block">Humidity</span>
          <span className="text-sm font-mono font-black text-emerald-400">{data.data?.humidity || 68} %</span>
        </div>

        <div className="p-3 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1">
          <span className="text-[9px] font-black uppercase text-slate-500 block">CO2 Level</span>
          <span className="text-sm font-mono font-black text-emerald-400">{data.data?.co2 || 450} ppm</span>
        </div>

        <div className="p-3 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-1">
          <span className="text-[9px] font-black uppercase text-slate-500 block">Nutrient Level</span>
          <span className="text-sm font-mono font-black text-emerald-400">{data.data?.nutrient_level || 85} %</span>
        </div>
      </div>
    </div>
  );
}

export default LiveTelemetry;
