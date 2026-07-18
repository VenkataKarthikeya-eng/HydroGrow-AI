import React, { useState, useEffect } from 'react';
import client from '../../api/client';
import { Layers, Plus, Activity, CheckCircle2 } from 'lucide-react';

function GreenhouseDashboard({ activeFarm }) {
  const [greenhouses, setGreenhouses] = useState([]);
  const [name, setName] = useState('');

  const fetchGreenhouses = async () => {
    if (!activeFarm?.id) return;
    try {
      const res = await client.get(`/api/greenhouses?farm_id=${activeFarm.id}`);
      setGreenhouses(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchGreenhouses();
  }, [activeFarm]);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!name || !activeFarm?.id) return;
    try {
      await client.post('/api/greenhouses/create', {
        farm_id: activeFarm.id,
        name,
        area_size: 60.0
      });
      setName('');
      fetchGreenhouses();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-6">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Greenhouse Zones & Growing Environments</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Active growing channels, environmental control & automation</p>
        </div>
        <Layers className="h-4 w-4 text-emerald-400" />
      </div>

      <form onSubmit={handleCreate} className="flex gap-3 bg-slate-950/40 p-4 rounded-2xl border border-slate-900">
        <input
          type="text"
          placeholder="Greenhouse Name (e.g. Zone 2 - Aeroponics)"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="flex-grow px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-100 focus:outline-none focus:border-emerald-500"
          required
        />
        <button
          type="submit"
          className="px-4 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase tracking-wider transition-all flex items-center gap-1.5"
        >
          <Plus className="h-4 w-4" /> Add Greenhouse Zone
        </button>
      </form>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {greenhouses.map((g) => (
          <div key={g.id} className="p-4 rounded-2xl bg-slate-950/40 border border-slate-900 space-y-2">
            <div className="flex justify-between items-start">
              <h5 className="font-bold text-slate-100 text-sm">{g.name}</h5>
              <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 text-[9px] font-black">
                Optimal
              </span>
            </div>
            <p className="text-[11px] text-slate-400">{g.environment_type} • {g.area_size} m²</p>
            <div className="flex items-center gap-2 pt-1">
              <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" />
              <span className="text-[10px] text-slate-300">Automation Engine Active</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default GreenhouseDashboard;
