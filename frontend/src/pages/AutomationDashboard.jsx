import React, { useState } from 'react';
import { Sliders, Zap, CheckCircle2, ShieldCheck, Plus, RefreshCw, Trash2 } from 'lucide-react';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';

export default function AutomationDashboard() {
  const [rules, setRules] = useState([
    { id: 1, name: 'Auto Dosing Rule #1', trigger: 'Water pH > 6.5', action: 'Inject 10ml pH Down Buffer', status: 'Active' },
    { id: 2, name: 'Canopy Misting Rule #2', trigger: 'Air Temp > 25.0°C', action: 'Trigger 30s High Pressure Misting', status: 'Active' },
    { id: 3, name: 'EC Boost Rule #3', trigger: 'EC < 1.6 mS/cm', action: 'Inject 20ml Macro Solution A+B', status: 'Active' },
  ]);

  const [ruleName, setRuleName] = useState('');
  const [trigger, setTrigger] = useState('');
  const [action, setAction] = useState('');

  const handleAddRule = (e) => {
    e.preventDefault();
    if (!ruleName || !trigger) return;
    const newRule = {
      id: Date.now(),
      name: ruleName,
      trigger,
      action: action || 'Trigger Alert Notification',
      status: 'Active'
    };
    setRules([newRule, ...rules]);
    setRuleName('');
    setTrigger('');
    setAction('');
  };

  const handleDeleteRule = (id) => {
    setRules(rules.filter(r => r.id !== id));
  };

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-300">
      
      {/* Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
            <Sliders className="w-4 h-4" /> Dosing & Climate Automation
          </div>
          <h1 className="text-3xl font-black text-slate-900 dark:text-white mt-1">
            Automation Control Center
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Define automated rules for fertigation dosing pumps, misting solenoids, and climate actuators.
          </p>
        </div>

        <Badge variant="brand" className="px-3 py-1.5 text-xs">
          Auto Engine Active
        </Badge>
      </div>

      {/* Add New Rule Card */}
      <Card padding="p-8" header="Create New Automation Rule">
        <form onSubmit={handleAddRule} className="grid grid-cols-1 sm:grid-cols-4 gap-4">
          <div>
            <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Rule Name</label>
            <input
              type="text"
              required
              placeholder="e.g. Night Temp Guard"
              value={ruleName}
              onChange={(e) => setRuleName(e.target.value)}
              className="w-full px-3 py-2 text-sm rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Trigger Condition</label>
            <input
              type="text"
              required
              placeholder="e.g. Air Temp < 18°C"
              value={trigger}
              onChange={(e) => setTrigger(e.target.value)}
              className="w-full px-3 py-2 text-sm rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Actuator Action</label>
            <input
              type="text"
              required
              placeholder="e.g. Turn On Heater"
              value={action}
              onChange={(e) => setAction(e.target.value)}
              className="w-full px-3 py-2 text-sm rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100"
            />
          </div>

          <div className="flex items-end">
            <Button variant="primary" type="submit" icon={Plus} className="w-full">
              Add Rule
            </Button>
          </div>
        </form>
      </Card>

      {/* Rules Table Card */}
      <Card padding="p-8" header="Active Greenhouse Rules">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 text-xs font-bold text-slate-500 uppercase tracking-wider">
                <th className="pb-3">Rule Name</th>
                <th className="pb-3">Trigger Condition</th>
                <th className="pb-3">Action Executed</th>
                <th className="pb-3">Status</th>
                <th className="pb-3 text-right">Delete</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {rules.map((r) => (
                <tr key={r.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/40 transition-colors">
                  <td className="py-4 font-bold text-slate-900 dark:text-white">{r.name}</td>
                  <td className="py-4 font-semibold text-emerald-600 dark:text-emerald-400">{r.trigger}</td>
                  <td className="py-4 text-slate-600 dark:text-slate-300">{r.action}</td>
                  <td className="py-4">
                    <Badge variant="optimized">{r.status}</Badge>
                  </td>
                  <td className="py-4 text-right">
                    <Button variant="ghost" size="sm" onClick={() => handleDeleteRule(r.id)} icon={Trash2} className="text-red-500 hover:text-red-700">
                      Remove
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

    </div>
  );
}
