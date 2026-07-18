import React, { useState } from 'react';
import client from '../../api/client';
import { Cpu, Plus, Key, Radio, CheckCircle2 } from 'lucide-react';

function DeviceManagement({ devices, onDeviceRegistered }) {
  const [deviceId, setDeviceId] = useState('');
  const [deviceType, setDeviceType] = useState('ESP32');
  const [location, setLocation] = useState('Zone 1 - Hydroponics');
  const [newKey, setNewKey] = useState('');
  const [msg, setMsg] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();
    if (!deviceId) return;
    try {
      const res = await client.post('/api/devices/register', {
        device_id: deviceId,
        device_type: deviceType,
        location
      });
      setNewKey(res.data.api_key);
      setMsg(`Device '${res.data.device_id}' registered successfully.`);
      setDeviceId('');
      if (onDeviceRegistered) onDeviceRegistered();
    } catch (err) {
      setMsg('Failed to register device.');
    }
  };

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-6">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Hardware Device Management & Registration</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Provision ESP32, Raspberry Pi & Arduino sensor nodes</p>
        </div>
        <Cpu className="h-4 w-4 text-emerald-400" />
      </div>

      {/* Registration Form */}
      <form onSubmit={handleRegister} className="grid grid-cols-1 sm:grid-cols-4 gap-3 bg-slate-950/40 p-4 rounded-2xl border border-slate-900">
        <input
          type="text"
          placeholder="Device ID (e.g. ESP32_001)"
          value={deviceId}
          onChange={(e) => setDeviceId(e.target.value)}
          className="px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs font-mono text-slate-100 focus:outline-none focus:border-emerald-500"
          required
        />
        <select
          value={deviceType}
          onChange={(e) => setDeviceType(e.target.value)}
          className="px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
        >
          <option value="ESP32">ESP32 Microcontroller</option>
          <option value="Raspberry Pi">Raspberry Pi Gateway</option>
          <option value="Arduino">Arduino Sensor Node</option>
        </select>
        <input
          type="text"
          placeholder="Location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          className="px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-100 focus:outline-none focus:border-emerald-500"
        />
        <button
          type="submit"
          className="px-4 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase tracking-wider transition-all flex items-center justify-center gap-1.5"
        >
          <Plus className="h-4 w-4" /> Provision Device
        </button>
      </form>

      {newKey && (
        <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-xs space-y-1">
          <div className="flex items-center gap-2 text-emerald-400 font-bold">
            <Key className="h-4 w-4" /> Hardware API Access Key Generated (Save Now):
          </div>
          <code className="block p-2 bg-slate-950 rounded border border-slate-800 font-mono text-emerald-300 select-all">
            {newKey}
          </code>
        </div>
      )}

      {/* Device List */}
      <div className="space-y-2">
        <span className="text-[9px] font-black uppercase text-slate-500 tracking-wider block">Registered Hardware Nodes ({devices?.length || 0})</span>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {devices?.map((d) => (
            <div key={d.id} className="p-3.5 rounded-2xl bg-slate-950/40 border border-slate-900 flex justify-between items-center">
              <div className="space-y-0.5">
                <div className="flex items-center gap-2">
                  <span className="h-2 w-2 rounded-full bg-emerald-400" />
                  <span className="font-mono font-bold text-xs text-slate-100">{d.device_id}</span>
                  <span className="px-1.5 py-0.5 rounded bg-slate-900 text-[9px] font-semibold text-slate-400">{d.device_type}</span>
                </div>
                <p className="text-[10px] text-slate-500">{d.location}</p>
              </div>
              <span className="px-2 py-0.5 rounded text-[9px] font-black uppercase bg-emerald-500/10 text-emerald-400">
                {d.status}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default DeviceManagement;
