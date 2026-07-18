import React from 'react';
import { Sprout, Building, Plus, CheckCircle2 } from 'lucide-react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Badge from '../../components/ui/Badge';

export default function FarmDashboard() {
  const farms = [
    { name: 'Demo Hydro Farm (Main)', location: 'Greenhouse Alpha', batches: 4, status: 'Active', crops: 'Butterhead Lettuce NFT Bay' },
    { name: 'Research Lab Facility #02', location: 'Vertical Bay Beta', batches: 2, status: 'Active', crops: 'Butterhead Lettuce DWC Bay' },
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-300">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
            <Building className="w-4 h-4" /> Multi-Farm Management
          </div>
          <h1 className="text-3xl font-black text-slate-900 dark:text-white mt-1">
            Registered Farm Facilities
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Overview of multi-tenant greenhouse locations, active crop batches, and yield targets.
          </p>
        </div>

        <Button variant="primary" size="sm" icon={Plus}>
          Add Farm Facility
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {farms.map((farm, idx) => (
          <Card key={idx} padding="p-8" className="space-y-4 hover:border-emerald-500 transition-colors">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-white">{farm.name}</h3>
                <p className="text-xs text-slate-500">{farm.location}</p>
              </div>
              <Badge variant="optimized">{farm.status}</Badge>
            </div>
            <div className="pt-2 text-xs text-slate-600 dark:text-slate-300 space-y-1">
              <div><span className="font-bold">Active Batches:</span> {farm.batches} Grow Bays</div>
              <div><span className="font-bold">Crops Grown:</span> {farm.crops}</div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
