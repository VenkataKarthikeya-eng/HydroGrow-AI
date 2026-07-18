import React, { useState } from 'react';
import client from '../../api/client';
import { Sprout, Calendar, RefreshCw } from 'lucide-react';

function CropLifecycleCard({ crop, onCropUpdated }) {
  const [cropName, setCropName] = useState('');
  const [expectedDays, setExpectedDays] = useState(30);
  const [loading, setLoading] = useState(false);

  const handleStartCycle = async (e) => {
    e.preventDefault();
    if (!cropName.trim()) return;

    setLoading(true);
    try {
      await client.post('/api/crops', {
        crop_name: cropName,
        expected_harvest_days: parseInt(expectedDays)
      });
      setCropName('');
      if (onCropUpdated) onCropUpdated();
    } catch (err) {
      console.error('Failed to create crop cycle', err);
    } finally {
      setLoading(false);
    }
  };

  const handleNextStage = async () => {
    if (!crop) return;
    const stages = ['Seedling', 'Vegetative', 'Maturity', 'Harvest'];
    const currIndex = stages.indexOf(crop.current_stage);
    if (currIndex === -1 || currIndex === stages.length - 1) return;
    
    const nextStage = stages[currIndex + 1];
    try {
      await client.put(`/api/crops/${crop.id}`, {
        current_stage: nextStage
      });
      if (onCropUpdated) onCropUpdated();
    } catch (err) {
      console.error('Failed to update stage', err);
    }
  };

  const hasActiveCrop = crop && Object.keys(crop).length > 0;

  return (
    <div className="glass-panel p-6 rounded-2xl border border-slate-900 bg-slate-950/20 shadow-lg space-y-4">
      <div className="border-b border-slate-900 pb-3">
        <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Crop Lifecycle Management</h4>
        <p className="text-[10px] text-slate-500">Track and advance active hydroponic growth periods</p>
      </div>

      {!hasActiveCrop ? (
        <form onSubmit={handleStartCycle} className="space-y-3 text-xs">
          <span className="text-[10px] text-slate-400 font-extrabold uppercase tracking-wider block">Start Growth Period</span>
          <div className="grid grid-cols-2 gap-3">
            <input
              type="text"
              value={cropName}
              onChange={(e) => setCropName(e.target.value)}
              placeholder="e.g. Butterhead Lettuce"
              className="px-3 py-2 rounded-xl bg-slate-950 border border-slate-900 text-slate-200 focus:outline-none focus:border-slate-800 font-semibold"
            />
            <input
              type="number"
              value={expectedDays}
              onChange={(e) => setExpectedDays(e.target.value)}
              placeholder="Expected Days (e.g. 30)"
              className="px-3 py-2 rounded-xl bg-slate-950 border border-slate-900 text-slate-200 focus:outline-none focus:border-slate-800 font-semibold"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full py-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black uppercase rounded-xl transition-all"
          >
            {loading ? 'Starting...' : 'Initiate Crop Cycle'}
          </button>
        </form>
      ) : (
        <div className="space-y-4">
          <div className="flex justify-between items-center bg-slate-950/40 border border-slate-900 p-3 rounded-xl">
            <div className="flex items-center gap-2">
              <Sprout className="h-5 w-5 text-emerald-400" />
              <div>
                <span className="text-[11px] font-black text-white uppercase block leading-tight">{crop.crop_name}</span>
                <span className="text-[8px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-bold uppercase tracking-wider inline-block mt-0.5">
                  Stage: {crop.current_stage}
                </span>
              </div>
            </div>
            
            {crop.current_stage !== 'Harvest' && (
              <button
                onClick={handleNextStage}
                className="flex items-center gap-1 px-3 py-1.5 bg-slate-900 hover:bg-slate-850 border border-slate-800 text-[10px] text-slate-300 font-bold uppercase rounded-lg active:scale-95 transition-all"
              >
                <RefreshCw className="h-3 w-3 text-emerald-450" /> Next Stage
              </button>
            )}
          </div>

          <div className="space-y-1">
            <div className="flex justify-between text-[10px] text-slate-400 font-bold">
              <span>Growth Progress</span>
              <span className="font-mono">{crop.growth_progress}%</span>
            </div>
            <div className="h-2 rounded-full bg-slate-900 border border-slate-850 overflow-hidden relative">
              <div 
                className="h-full bg-gradient-to-r from-emerald-500 to-teal-600 rounded-full transition-all duration-500" 
                style={{ width: `${crop.growth_progress}%` }} 
              />
            </div>
          </div>

          <div className="flex gap-4 text-slate-400 text-xs">
            <div className="flex items-center gap-1.5">
              <Calendar className="h-4 w-4 text-emerald-400" />
              <div>
                <span className="text-[8px] text-slate-500 uppercase font-black block">Days Remaining</span>
                <span className="font-bold text-slate-200">{crop.days_remaining} days</span>
              </div>
            </div>
            <div className="flex items-center gap-1.5 border-l border-slate-900 pl-4">
              <div className="p-1 rounded bg-slate-950 border border-slate-900 text-[10px] font-mono text-slate-300">
                {crop.current_stage === 'Harvest' ? 'Completed' : 'Active'}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default CropLifecycleCard;
