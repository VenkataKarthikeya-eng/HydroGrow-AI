import React from 'react';
import { Calendar, Thermometer, Droplets, FlaskConical, Zap, ArrowUpRight, Trash2 } from 'lucide-react';

function PredictionHistoryCard({ record, onReload, onDelete }) {
  const { id, created_at, predicted_weight, growth_category, input_parameters } = record;

  const formattedDate = new Date(created_at).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });

  const getCategoryColor = (cat) => {
    const name = cat.toLowerCase();
    if (name.includes('excellent')) return 'text-emerald-400 border-emerald-500/20 bg-emerald-500/5';
    if (name.includes('good') || name.includes('average')) return 'text-blue-400 border-blue-500/20 bg-blue-500/5';
    return 'text-rose-400 border-rose-500/20 bg-rose-500/5';
  };

  return (
    <div className="glass-panel p-5 rounded-2xl border border-slate-800 flex flex-col justify-between relative overflow-hidden group shadow-lg">
      <div className="space-y-4">
        {/* Header */}
        <div className="flex justify-between items-start gap-2 border-b border-slate-900 pb-3">
          <div className="flex items-center gap-1.5 text-slate-500 text-[10px] font-mono">
            <Calendar className="h-3.5 w-3.5" />
            <span>{formattedDate}</span>
          </div>
          <span className={`px-2 py-0.5 text-[10px] font-bold rounded-full border ${getCategoryColor(growth_category)}`}>
            {growth_category}
          </span>
        </div>

        {/* Prediction summary */}
        <div>
          <span className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold block">Predicted weight</span>
          <span className="text-2xl font-black text-white">{predicted_weight.toFixed(2)} g</span>
        </div>

        {/* Core inputs parameters grid */}
        <div className="grid grid-cols-2 gap-3 text-[10px] text-slate-400 bg-slate-950/40 p-2.5 rounded-lg border border-slate-900">
          <div className="flex items-center gap-1">
            <Thermometer className="h-3.5 w-3.5 text-emerald-400" />
            <span>Air: {input_parameters.air_temperature}°C</span>
          </div>
          <div className="flex items-center gap-1">
            <Droplets className="h-3.5 w-3.5 text-blue-400" />
            <span>RH: {input_parameters.humidity}%</span>
          </div>
          <div className="flex items-center gap-1">
            <FlaskConical className="h-3.5 w-3.5 text-purple-400" />
            <span>pH: {input_parameters.water_ph}</span>
          </div>
          <div className="flex items-center gap-1">
            <Zap className="h-3.5 w-3.5 text-amber-400" />
            <span>EC: {input_parameters.water_ec}</span>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-2 mt-5 pt-3 border-t border-slate-900">
        <button
          onClick={() => onReload(input_parameters)}
          className="flex-grow py-2 px-3 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/20 text-emerald-400 text-xs font-semibold flex items-center justify-center gap-1 transition-all active:scale-[0.98]"
        >
          Reload params
          <ArrowUpRight className="h-3.5 w-3.5" />
        </button>
        
        {onDelete && (
          <button
            onClick={() => onDelete(id)}
            className="p-2 rounded-lg bg-slate-900 hover:bg-rose-950/20 border border-slate-800 hover:border-rose-500/30 text-slate-400 hover:text-rose-400 transition-all"
            title="Delete prediction log"
          >
            <Trash2 className="h-4 w-4" />
          </button>
        )}
      </div>
    </div>
  );
}

export default PredictionHistoryCard;
