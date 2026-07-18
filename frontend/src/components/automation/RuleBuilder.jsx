import React, { useState } from 'react';
import client from '../../api/client';
import { PlusCircle } from 'lucide-react';

function RuleBuilder({ onRuleCreated }) {
  const [ruleName, setRuleName] = useState('');
  const [parameter, setParameter] = useState('water_ph');
  const [condition, setCondition] = useState('above');
  const [thresholdValue, setThresholdValue] = useState('');
  const [actionType, setActionType] = useState('activate');
  const [actionValue, setActionValue] = useState('pH Controller');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const parameterOptions = [
    { value: 'water_ph', label: 'Water pH' },
    { value: 'water_ec', label: 'Water EC' },
    { value: 'temperature', label: 'Air Temperature' },
    { value: 'humidity', label: 'Air Humidity' },
    { value: 'co2', label: 'CO2 Level' }
  ];

  const deviceOptions = [
    'pH Controller',
    'Nutrient Pump',
    'Cooling Fan',
    'Water Pump',
    'Grow Lights',
    'Ventilation System'
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!ruleName.trim() || !thresholdValue) {
      setError('Please fill in all fields.');
      return;
    }
    
    setLoading(true);
    setError('');
    try {
      await client.post('/api/automation/rules', {
        rule_name: ruleName,
        parameter,
        condition,
        threshold_value: parseFloat(thresholdValue),
        action_type: actionType,
        action_value: actionValue,
        enabled: true
      });
      setRuleName('');
      setThresholdValue('');
      if (onRuleCreated) onRuleCreated();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create rule.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel p-6 rounded-2xl border border-slate-900 bg-slate-950/20 shadow-lg">
      <div className="border-b border-slate-900 pb-3 mb-4">
        <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Rule Builder</h4>
        <p className="text-[10px] text-slate-500">Establish conditional trigger conditions for smart relays</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4 text-xs">
        {error && <div className="p-2 rounded bg-rose-500/10 border border-rose-500/20 text-rose-400">{error}</div>}

        <div className="space-y-1">
          <label className="text-slate-400 font-bold uppercase tracking-wider text-[9px]">Rule Name</label>
          <input
            type="text"
            value={ruleName}
            onChange={(e) => setRuleName(e.target.value)}
            placeholder="e.g. Critical Water pH Correction"
            className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-900 text-slate-200 focus:outline-none focus:border-slate-800 font-semibold"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-1">
            <label className="text-slate-400 font-bold uppercase tracking-wider text-[9px]">If Parameter</label>
            <select
              value={parameter}
              onChange={(e) => setParameter(e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-900 text-slate-300 focus:outline-none font-bold"
            >
              {parameterOptions.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
            </select>
          </div>

          <div className="space-y-1">
            <label className="text-slate-400 font-bold uppercase tracking-wider text-[9px]">Is Condition</label>
            <select
              value={condition}
              onChange={(e) => setCondition(e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-900 text-slate-350 focus:outline-none font-bold"
            >
              <option value="above">Above</option>
              <option value="below">Below</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-1">
            <label className="text-slate-400 font-bold uppercase tracking-wider text-[9px]">Threshold Target</label>
            <input
              type="number"
              step="0.01"
              value={thresholdValue}
              onChange={(e) => setThresholdValue(e.target.value)}
              placeholder="e.g. 6.5"
              className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-900 text-slate-200 focus:outline-none focus:border-slate-800 font-semibold"
            />
          </div>

          <div className="space-y-1">
            <label className="text-slate-400 font-bold uppercase tracking-wider text-[9px]">Then Action</label>
            <select
              value={actionType}
              onChange={(e) => setActionType(e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-900 text-slate-350 focus:outline-none font-bold"
            >
              <option value="activate">Activate</option>
              <option value="deactivate">Deactivate</option>
            </select>
          </div>
        </div>

        <div className="space-y-1">
          <label className="text-slate-400 font-bold uppercase tracking-wider text-[9px]">Actuator Target Asset</label>
          <select
            value={actionValue}
            onChange={(e) => setActionValue(e.target.value)}
            className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-900 text-slate-350 focus:outline-none font-bold"
          >
            {deviceOptions.map(d => <option key={d} value={d}>{d}</option>)}
          </select>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 rounded-xl font-black uppercase tracking-wider flex items-center justify-center gap-1.5 transition-colors disabled:opacity-55"
        >
          <PlusCircle className="h-4 w-4" />
          {loading ? 'Creating...' : 'Establish Automation Rule'}
        </button>
      </form>
    </div>
  );
}

export default RuleBuilder;
