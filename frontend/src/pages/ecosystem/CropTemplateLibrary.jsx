import React from 'react';
import { Sprout, BookOpen, Download, Sparkles } from 'lucide-react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Badge from '../../components/ui/Badge';

export default function CropTemplateLibrary() {
  const templates = [
    { title: 'Commercial Butterhead Lettuce NFT Template', days: '30 Days', ph: '6.0 - 6.2', ec: '1.8 - 2.2 mS/cm', yieldEst: '380g / plant' },
    { title: 'Deep Water Culture (DWC) Lettuce Recipe', days: '28 Days', ph: '6.0 - 6.4', ec: '2.0 - 2.2 mS/cm', yieldEst: '365g / plant' },
    { title: 'Vertical Tower Hydroponics Lettuce Recipe', days: '25 Days', ph: '6.0 - 6.3', ec: '1.8 - 2.0 mS/cm', yieldEst: '350g / plant' },
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-300">
      <div className="border-b border-slate-200 dark:border-slate-800 pb-6">
        <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
          <BookOpen className="w-4 h-4" /> Validated Crop Recipes
        </div>
        <h1 className="text-3xl font-black text-slate-900 dark:text-white mt-1">
          Crop Template & Recipe Library
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Pre-validated hydroponic growth templates with optimal fertigation curves, light spectrum schedules, and target yields.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {templates.map((t, idx) => (
          <Card key={idx} padding="p-8" className="space-y-4 flex flex-col justify-between hover:border-emerald-500 transition-colors">
            <div>
              <div className="flex justify-between items-start mb-2">
                <Badge variant="brand">Verified Recipe</Badge>
                <span className="text-xs font-bold text-slate-500">{t.days}</span>
              </div>
              <h3 className="text-base font-bold text-slate-900 dark:text-white mt-2">{t.title}</h3>
              <div className="mt-3 text-xs space-y-1 text-slate-600 dark:text-slate-300">
                <div><span className="font-bold">Target pH:</span> {t.ph}</div>
                <div><span className="font-bold">Target EC:</span> {t.ec}</div>
                <div><span className="font-bold">Est. Harvest Yield:</span> {t.yieldEst}</div>
              </div>
            </div>

            <div className="pt-4 border-t border-slate-100 dark:border-slate-800 flex justify-between items-center">
              <span className="text-xs text-slate-400">Free SaaS Template</span>
              <Button variant="primary" size="sm" icon={Sparkles}>
                Apply to Batch
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
