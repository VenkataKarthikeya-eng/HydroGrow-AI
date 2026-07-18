import React, { useState } from 'react';
import client from '../../api/client';
import { Play, Sliders } from 'lucide-react';

function FarmSimulator({ onSimulationComplete }) {
  const [scenarioName, setScenarioName] = useState('Nutrient Optimization Run');
  const [durationDays, setDurationDays] = useState(35);
  
  const [temp, setTemp] = useState(22);
  const [humidity, setHumidity] = useState(60);
  const [co2, setCo2] = useState(450);
  const [ec, setEc] = useState(2.0);
  const [ph, setPh] = useState(6.0);
  const [lightHours, setLightHours] = useState(16);
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!scenarioName.trim()) {
      setError('Please fill in scenario name.');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      const res = await client.post('/api/twin/simulate', {
        scenario_name: scenarioName,
        duration_days: parseInt(durationDays),
        overrides: {
          temperature: parseFloat(temp),
          humidity: parseFloat(humidity),
          co2: parseFloat(co2),
          water_ec: parseFloat(ec),
          water_ph: parseFloat(ph),
          light_hours: parseFloat(lightHours)
        }
      });
      if (onSimulationComplete) onSimulationComplete(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to trigger simulation.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-4">
      <div className="border-b border-slate-900 pb-3 flex justify-between items-center">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Crop Simulation Panel</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Adjust environmental overrides relative to farm baseline</p>
        </div>
        <Sliders className="h-4 w-4 text-emerald-400" />
      </div>

      <form onSubmit={handleSubmit} className="space-y-4 text-xs font-semibold">
        {error && <div className="p-2.5 rounded bg-rose-500/10 border border-rose-500/20 text-rose-400">{error}</div>}

        <div className="space-y-1">
          <label className="text-[9px] uppercase tracking-wider text-slate-400 font-black">Scenario Name</label>
          <input
            type="text"
            value={scenarioName}
            onChange={(e) => setScenarioName(e.target.value)}
            placeholder="e.g. Nutrient Boost Run"
            className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-900 text-slate-200 focus:outline-none focus:border-slate-800 font-bold"
          />
        </div>

        <div className="space-y-1.5">
          <div className="flex justify-between font-bold text-[9px] uppercase tracking-wider text-slate-400">
            <span>Simulation Period</span>
            <span className="font-mono text-emerald-400">{durationDays} days</span>
          </div>
          <input
            type="range"
            min="5"
            max="60"
            value={durationDays}
            onChange={(e) => setDurationDays(e.target.value)}
            className="w-full h-1 bg-slate-900 accent-emerald-500 rounded-lg cursor-pointer"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-1.5">
            <div className="flex justify-between font-bold text-[9px] uppercase tracking-wider text-slate-400">
              <span>Air Temperature</span>
              <span className="font-mono text-emerald-400">{temp}°C</span>
            </div>
            <input
              type="range"
              min="15"
              max="35"
              value={temp}
              onChange={(e) => setTemp(e.target.value)}
              className="w-full h-1 bg-slate-900 accent-emerald-500 rounded-lg cursor-pointer"
            />
          </div>

          <div className="space-y-1.5">
            <div className="flex justify-between font-bold text-[9px] uppercase tracking-wider text-slate-400">
              <span>Humidity</span>
              <span className="font-mono text-emerald-400">{humidity}%</span>
            </div>
            <input
              type="range"
              min="30"
              max="90"
              value={humidity}
              onChange={(e) => setHumidity(e.target.value)}
              className="w-full h-1 bg-slate-900 accent-emerald-500 rounded-lg cursor-pointer"
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-1.5">
            <div className="flex justify-between font-bold text-[9px] uppercase tracking-wider text-slate-400">
              <span>CO2 Level</span>
              <span className="font-mono text-emerald-400">{co2} ppm</span>
            </div>
            <input
              type="range"
              min="300"
              max="1500"
              step="50"
              value={co2}
              onChange={(e) => setCo2(e.target.value)}
              className="w-full h-1 bg-slate-900 accent-emerald-500 rounded-lg cursor-pointer"
            />
          </div>

          <div className="space-y-1.5">
            <div className="flex justify-between font-bold text-[9px] uppercase tracking-wider text-slate-400">
              <span>Water EC</span>
              <span className="font-mono text-emerald-400">{ec} mS</span>
            </div>
            <input
              type="range"
              min="1.0"
              max="3.5"
              step="0.1"
              value={ec}
              onChange={(e) => setEc(e.target.value)}
              className="w-full h-1 bg-slate-900 accent-emerald-500 rounded-lg cursor-pointer"
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-1.5">
            <div className="flex justify-between font-bold text-[9px] uppercase tracking-wider text-slate-400">
              <span>Water pH</span>
              <span className="font-mono text-emerald-400">{ph}</span>
            </div>
            <input
              type="range"
              min="4.5"
              max="7.5"
              step="0.1"
              value={ph}
              onChange={(e) => setPh(e.target.value)}
              className="w-full h-1 bg-slate-900 accent-emerald-500 rounded-lg cursor-pointer"
            />
          </div>

          <div className="space-y-1.5">
            <div className="flex justify-between font-bold text-[9px] uppercase tracking-wider text-slate-400">
              <span>Light Hours</span>
              <span className="font-mono text-emerald-400">{lightHours} hrs</span>
            </div>
            <input
              type="range"
              min="8"
              max="24"
              value={lightHours}
              onChange={(e) => setLightHours(e.target.value)}
              className="w-full h-1 bg-slate-900 accent-emerald-500 rounded-lg cursor-pointer"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black uppercase tracking-wider rounded-xl transition-all shadow-lg active:scale-95 flex items-center justify-center gap-1.5"
        >
          <Play className="h-4 w-4 fill-current" />
          {loading ? 'Initializing Simulation Twin...' : 'Execute Digital Twin Simulation'}
        </button>
      </form>
    </div>
  );
}

export default FarmSimulator;
