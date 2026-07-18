import React from 'react';
import { Weight, Award, Leaf } from 'lucide-react';

function PredictionCard({ prediction, validation }) {
  if (!prediction) return null;

  const { predicted_weight, growth_category } = prediction;
  const { was_adjusted, validation_message } = validation || {};

  // Clean category string (removing emojis if present for styling match)
  const cleanCategory = growth_category ? growth_category.replace(/[^a-zA-Z]/g, '').trim() : 'Unknown';
  
  // Choose badge color
  const getCategoryStyles = (cat) => {
    const name = cat.toLowerCase();
    if (name.includes('excellent')) return {
      bg: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
      text: 'text-emerald-400',
      fill: 'stroke-emerald-400'
    };
    if (name.includes('good') || name.includes('average')) return {
      bg: 'bg-blue-500/10 text-blue-400 border-blue-500/30',
      text: 'text-blue-400',
      fill: 'stroke-blue-400'
    };
    return {
      bg: 'bg-rose-500/10 text-rose-400 border-rose-500/30',
      text: 'text-rose-400',
      fill: 'stroke-rose-400'
    };
  };

  const style = getCategoryStyles(cleanCategory);

  // Compute percentage for a circular progress gauge (Max weight in dataset is ~412g)
  const maxWeight = 420;
  const percentage = Math.min(Math.round((predicted_weight / maxWeight) * 100), 100);
  const strokeDashoffset = 251.2 - (251.2 * percentage) / 100;

  return (
    <div className="glass-panel p-6 rounded-2xl border border-slate-800 relative overflow-hidden shadow-xl">
      {/* Decorative background glow */}
      <div className="absolute -top-12 -right-12 w-32 h-32 bg-emerald-500/10 rounded-full blur-2xl"></div>

      <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
        <Leaf className="h-5 w-5 text-emerald-400" />
        AI Growth Prediction
      </h3>

      <div className="flex flex-col md:flex-row items-center md:justify-around gap-6 py-2">
        {/* Circle Gauge */}
        <div className="relative flex items-center justify-center">
          <svg className="w-32 h-32 transform -rotate-90">
            {/* Background ring */}
            <circle
              cx="64"
              cy="64"
              r="40"
              className="stroke-slate-800"
              strokeWidth="8"
              fill="transparent"
            />
            {/* Foreground circle indicator */}
            <circle
              cx="64"
              cy="64"
              r="40"
              className="transition-all duration-1000 ease-out"
              strokeWidth="8"
              strokeDasharray="251.2"
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              fill="transparent"
              stroke={cleanCategory.toLowerCase().includes('excellent') ? '#34d399' : cleanCategory.toLowerCase().includes('good') || cleanCategory.toLowerCase().includes('average') ? '#60a5fa' : '#f87171'}
            />
          </svg>
          {/* Central label */}
          <div className="absolute text-center">
            <span className="text-2xl font-black text-white">{percentage}%</span>
            <span className="block text-[9px] text-slate-500 uppercase tracking-widest font-semibold">of max</span>
          </div>
        </div>

        {/* Labels & Categorization Details */}
        <div className="space-y-4 text-center md:text-left flex-grow">
          <div>
            <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold">Predicted Harvest Weight</span>
            <div className="flex items-baseline justify-center md:justify-start gap-1 mt-0.5">
              <span className="text-4xl font-extrabold tracking-tight text-white">
                {predicted_weight ? predicted_weight.toFixed(2) : '0.00'}
              </span>
              <span className="text-lg text-slate-400 font-medium">grams</span>
            </div>
          </div>

          <div className="flex flex-wrap items-center justify-center md:justify-start gap-2">
            <span className={`px-3 py-1 text-xs font-bold rounded-full border ${style.bg} flex items-center gap-1.5`}>
              <Award className="h-3.5 w-3.5" />
              {growth_category || 'Unknown Category'}
            </span>

            {was_adjusted && (
              <span className="px-2.5 py-0.5 text-[10px] font-bold rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/25">
                Clipped (P5/P95)
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Validation Message Notification */}
      {validation_message && (
        <div className="mt-4 pt-4 border-t border-slate-900 text-xs text-slate-400 flex items-start gap-1.5 bg-slate-950/40 p-2.5 rounded-lg border border-slate-900">
          <span className="text-emerald-400 font-bold shrink-0">Reliability Check:</span>
          <span>{validation_message}</span>
        </div>
      )}
    </div>
  );
}

export default PredictionCard;
