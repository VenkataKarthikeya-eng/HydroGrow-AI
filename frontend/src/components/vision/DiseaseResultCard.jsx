import React from 'react';
import { Activity, ShieldAlert, CheckCircle } from 'lucide-react';

function DiseaseResultCard({ disease, confidence, severity }) {
  const getDiseaseDescription = (name) => {
    switch (name) {
      case 'Tip Burn':
        return 'Leaf tip necrosis caused by localized calcium deficiency during rapid growth phases. Often driven by inadequate humidity levels or excessive salt concentration (EC).';
      case 'Nutrient Deficiency':
        return 'General chlorosis or leaf yellowing indicating macro or micro nutrient lockout. Recalibrate reservoir pH and check EC levels.';
      case 'Root Rot Symptoms':
        return 'Pythium root decay leading to darkened, slimy root tissue and extreme transpiration lockout. Requires immediate sanitization flush.';
      case 'Leaf Spot':
        return 'Fungal or bacterial spore infestation on leaf surface. Usually triggered by water logging or poor ventilation.';
      case 'Yellow Leaves':
        return 'Chlorophyll degradation often indicating nitrogen deficit or light height burn stress.';
      case 'Fungal Stress':
        return 'Mildew or white mold growth due to excessive relative humidity and stale air pocketing.';
      default:
        return 'No pathogens or developmental anomalies detected. Leaf transpiration, turgidity, and coloration are within healthy ranges.';
    }
  };

  const isHealthy = disease === 'Healthy';

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-4">
      <div className="border-b border-slate-900 pb-3 flex justify-between items-center">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">AI Pathogen Diagnostic</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Lettuce anomalies and classification results</p>
        </div>
        {isHealthy ? (
          <CheckCircle className="h-5 w-5 text-emerald-400" />
        ) : (
          <ShieldAlert className="h-5 w-5 text-rose-400" />
        )}
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="p-3.5 bg-slate-950/40 border border-slate-900 rounded-2xl">
          <span className="text-[8px] text-slate-500 uppercase font-black block">Anomalies Detected</span>
          <span className="text-xs font-black text-white uppercase block mt-1">{disease}</span>
        </div>

        <div className="p-3.5 bg-slate-950/40 border border-slate-900 rounded-2xl">
          <span className="text-[8px] text-slate-500 uppercase font-black block">Confidence Match</span>
          <span className="text-xs font-black text-white block mt-1">{(confidence * 100).toFixed(0)}%</span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="p-3.5 bg-slate-950/40 border border-slate-900 rounded-2xl">
          <span className="text-[8px] text-slate-500 uppercase font-black block">Stress Severity</span>
          <span className={`text-xs font-black uppercase block mt-1 ${
            severity === 'High' ? 'text-rose-400' : severity === 'Medium' ? 'text-amber-400' : 'text-emerald-400'
          }`}>{severity}</span>
        </div>
        <div className="p-3.5 bg-slate-950/40 border border-slate-900 rounded-2xl flex items-center justify-center">
          <div className="flex items-center gap-1">
            <Activity className="h-4 w-4 text-emerald-450" />
            <span className="text-[9px] text-slate-400 font-extrabold uppercase tracking-wide">Scanner Active</span>
          </div>
        </div>
      </div>

      <div className="p-4 rounded-2xl border border-slate-900 bg-slate-950/40 space-y-1">
        <span className="text-[8px] text-slate-500 uppercase font-black block">Anatomical Analysis</span>
        <p className="text-[10px] text-slate-350 leading-relaxed font-semibold">{getDiseaseDescription(disease)}</p>
      </div>
    </div>
  );
}

export default DiseaseResultCard;
