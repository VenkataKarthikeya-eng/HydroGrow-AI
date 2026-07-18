import React from 'react';
import { Cpu, Activity, Database, CheckCircle2 } from 'lucide-react';
import Card from '../components/ui/Card';
import Badge from '../components/ui/Badge';

export default function MLModelCenter() {
  const models = [
    { name: 'Yield Prediction Neural Core', version: 'v2.4.1', accuracy: '99.4%', status: 'Production', cycles: '216 Cycles' },
    { name: 'Computer Vision Leaf Pathology CNN', version: 'v1.8.0', accuracy: '98.2%', status: 'Production', cycles: '45,000 Samples' },
    { name: 'Digital Twin Growth Curve Simulator', version: 'v3.1.0', accuracy: '97.6%', status: 'Production', cycles: '180 Simulations' },
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-300">
      
      <div className="border-b border-slate-200 dark:border-slate-800 pb-6">
        <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
          <Cpu className="w-4 h-4" /> MLOps Model Center
        </div>
        <h1 className="text-3xl font-black text-slate-900 dark:text-white mt-1">
          ML Model Repository & Metrics
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Deployed machine learning models, validation loss curves, and training cycle metadata.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {models.map((m, i) => (
          <Card key={i} padding="p-8" className="space-y-4">
            <div className="flex justify-between items-start">
              <Badge variant="brand">{m.status}</Badge>
              <span className="text-xs text-slate-400 font-mono">{m.version}</span>
            </div>
            <div>
              <h3 className="text-base font-bold text-slate-900 dark:text-white">{m.name}</h3>
              <div className="text-2xl font-black text-emerald-600 dark:text-emerald-400 mt-2">{m.accuracy}</div>
              <div className="text-xs text-slate-500 mt-1">Validation Accuracy Score</div>
            </div>
            <div className="pt-3 border-t border-slate-100 dark:border-slate-800 text-xs text-slate-500 flex justify-between">
              <span>Training Dataset:</span>
              <span className="font-semibold text-slate-700 dark:text-slate-300">{m.cycles}</span>
            </div>
          </Card>
        ))}
      </div>

    </div>
  );
}
