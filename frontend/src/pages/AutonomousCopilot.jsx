import React from 'react';
import { Bot, Sparkles, CheckCircle2, ShieldCheck, Activity } from 'lucide-react';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';

export default function AutonomousCopilot() {
  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-300">
      
      {/* Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
            <Bot className="w-4 h-4" /> Autonomous Farm Copilot
          </div>
          <h1 className="text-3xl font-black text-slate-900 dark:text-white mt-1">
            Autonomous Copilot Agent
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Autonomous decision-making engine monitoring crop health, predicting yield anomalies, and auto-correcting fertigation.
          </p>
        </div>

        <Badge variant="brand" className="px-3 py-1.5 text-xs">
          Agent Active (Autonomous Mode)
        </Badge>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        <Card padding="p-8" header="Agent Status" className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-500 font-bold uppercase">Decision Loop</span>
            <Badge variant="optimized">Active (10s Cycle)</Badge>
          </div>
          <div className="text-3xl font-black text-slate-900 dark:text-white">99.8%</div>
          <div className="text-xs text-slate-500">Autonomous Execution Stability Index</div>
        </Card>

        <Card padding="p-8" header="Last Auto Correction" className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-500 font-bold uppercase">Action Log</span>
            <Badge variant="neutral">14 Mins Ago</Badge>
          </div>
          <div className="text-base font-bold text-slate-900 dark:text-white">Adjusted pH Injector Buffer</div>
          <div className="text-xs text-slate-500">Corrected drift from 6.6 to 6.1 pH</div>
        </Card>

        <Card padding="p-8" header="Safety Constraints" className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-500 font-bold uppercase">Boundary Check</span>
            <Badge variant="optimized">Verified Safe</Badge>
          </div>
          <div className="text-base font-bold text-slate-900 dark:text-white">Max Dosing Safeguard</div>
          <div className="text-xs text-slate-500">Hard limit: Max 50ml buffer per 24h</div>
        </Card>

      </div>

    </div>
  );
}
