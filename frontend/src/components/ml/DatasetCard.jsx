import React from 'react';
import { Database, Layers } from 'lucide-react';

function DatasetCard({ datasets }) {
  const ds = datasets && datasets.length > 0 ? datasets[0] : {
    dataset_name: "HydroGrow Lettuce Agronomic Dataset v1",
    dataset_type: "Agronomic Predictors",
    source: "Greenhouse Sensors & Lab Calibrations",
    sample_count: 600,
    features: ["air_temperature", "humidity", "co2", "water_ph", "water_ec", "water_temperature", "nutrient_solution", "water_consumption", "seedling_height", "seedling_weight", "root_length"],
    description: "Synthesized agronomic predictor vectors for lettuce biomass expansion."
  };

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-4">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Training Dataset Repository</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Configurable training data matrices & features</p>
        </div>
        <Database className="h-4 w-4 text-emerald-400" />
      </div>

      <div className="space-y-3 text-xs">
        <div className="flex justify-between items-start">
          <div>
            <h5 className="font-extrabold text-slate-100">{ds.dataset_name}</h5>
            <span className="text-[9px] font-black uppercase text-slate-500">{ds.dataset_type} • {ds.source}</span>
          </div>
          <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 text-[9px] font-mono font-black">
            {ds.sample_count} Samples
          </span>
        </div>

        <p className="text-[11px] text-slate-400 leading-relaxed">{ds.description}</p>

        <div>
          <span className="text-[9px] font-black uppercase tracking-wider text-slate-500 block mb-1.5">Feature Vector ({ds.features?.length || 11}):</span>
          <div className="flex flex-wrap gap-1">
            {ds.features?.map((f, idx) => (
              <span key={idx} className="px-2 py-0.5 rounded-md bg-slate-900 border border-slate-800 text-slate-300 font-mono text-[9px]">
                {f}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default DatasetCard;
