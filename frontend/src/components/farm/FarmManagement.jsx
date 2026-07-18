import React, { useState } from 'react';
import client from '../../api/client';
import { Sprout, Plus, Building, MapPin, Layers } from 'lucide-react';

function FarmManagement({ farms, onFarmUpdated }) {
  const [farmName, setFarmName] = useState('');
  const [location, setLocation] = useState('Main Hydroponics Site');
  const [farmSize, setFarmSize] = useState('100');
  const [farmType, setFarmType] = useState('Hydroponic NFT');
  const [msg, setMsg] = useState('');

  const handleCreateFarm = async (e) => {
    e.preventDefault();
    if (!farmName) return;
    try {
      const res = await client.post('/api/farms/create', {
        farm_name: farmName,
        location,
        farm_size: parseFloat(farmSize),
        farm_type: farmType
      });
      setMsg(res.data.message);
      setFarmName('');
      if (onFarmUpdated) onFarmUpdated();
    } catch (err) {
      setMsg(err.response?.data?.detail || 'Failed to create farm.');
    }
  };

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-6">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Multi-Farm SaaS Management & Provisioning</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Provision & manage multi-tenant farming sites</p>
        </div>
        <Building className="h-4 w-4 text-emerald-400" />
      </div>

      {/* Creation Form */}
      <form onSubmit={handleCreateFarm} className="grid grid-cols-1 sm:grid-cols-4 gap-3 bg-slate-950/40 p-4 rounded-2xl border border-slate-900">
        <input
          type="text"
          placeholder="Farm Name (e.g. HydroGrow Facility A)"
          value={farmName}
          onChange={(e) => setFarmName(e.target.value)}
          className="px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-100 focus:outline-none focus:border-emerald-500"
          required
        />
        <input
          type="text"
          placeholder="Location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          className="px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-100 focus:outline-none focus:border-emerald-500"
        />
        <select
          value={farmType}
          onChange={(e) => setFarmType(e.target.value)}
          className="px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
        >
          <option value="Hydroponic NFT">Hydroponic NFT</option>
          <option value="Deep Water Culture (DWC)">Deep Water Culture (DWC)</option>
          <option value="Aeroponics Vertical">Aeroponics Vertical</option>
        </select>
        <button
          type="submit"
          className="px-4 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase tracking-wider transition-all flex items-center justify-center gap-1.5"
        >
          <Plus className="h-4 w-4" /> Provision Farm
        </button>
      </form>

      {msg && <p className="text-xs text-emerald-400 font-semibold">{msg}</p>}

      {/* Farms Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {farms?.map((f) => (
          <div key={f.id} className="p-4 rounded-2xl bg-slate-950/40 border border-slate-900 space-y-2">
            <div className="flex justify-between items-start">
              <div>
                <h5 className="font-extrabold text-slate-100 text-sm">{f.farm_name}</h5>
                <span className="text-[10px] text-slate-500">{f.location}</span>
              </div>
              <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 text-[9px] font-black uppercase">
                {f.is_owner ? "OWNER" : "MEMBER"}
              </span>
            </div>
            <p className="text-[11px] text-slate-400">{f.farm_type} • {f.farm_size} m²</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default FarmManagement;
