import React from 'react';

function LiveGauge({ ph, ec }) {
  const getPHPercentage = () => {
    if (!ph) return 50;
    const val = ((ph - 4) / 4) * 100;
    return Math.max(0, Math.min(100, val));
  };

  const getECPercentage = () => {
    if (!ec) return 50;
    const val = (ec / 4) * 100;
    return Math.max(0, Math.min(100, val));
  };

  return (
    <div className="glass-panel p-6 rounded-2xl border border-slate-900 bg-slate-950/20 shadow-lg space-y-4">
      <div>
        <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Solution Chemistry Index</h4>
        <p className="text-[10px] text-slate-500">Live calibration offsets for pH and nutrient concentration</p>
      </div>

      <div className="space-y-4">
        {/* pH Bar */}
        <div className="space-y-1">
          <div className="flex justify-between items-center text-[10px]">
            <span className="font-bold text-slate-300">Water pH Balance</span>
            <span className="font-mono font-black text-emerald-400">{ph ? ph.toFixed(2) : '--'} pH</span>
          </div>
          <div className="h-2 rounded-full bg-slate-900 border border-slate-850 relative overflow-hidden">
            <div className="absolute left-[37.5%] w-[25%] h-full bg-emerald-500/20" />
            <div 
              className="absolute h-full w-2 bg-gradient-to-r from-emerald-400 to-teal-500 rounded-full transition-all duration-300"
              style={{ left: `${getPHPercentage()}%` }}
            />
          </div>
          <div className="flex justify-between text-[8px] text-slate-600 font-bold uppercase tracking-wider">
            <span>Acidic (4.0)</span>
            <span className="text-emerald-500/60">Target (5.5-6.5)</span>
            <span>Alkaline (8.0)</span>
          </div>
        </div>

        {/* EC Bar */}
        <div className="space-y-1">
          <div className="flex justify-between items-center text-[10px]">
            <span className="font-bold text-slate-300">Electrical Conductivity</span>
            <span className="font-mono font-black text-teal-400">{ec ? ec.toFixed(2) : '--'} mS/cm</span>
          </div>
          <div className="h-2 rounded-full bg-slate-900 border border-slate-850 relative overflow-hidden">
            <div className="absolute left-[37.5%] w-[17.5%] h-full bg-teal-500/20" />
            <div 
              className="absolute h-full w-2 bg-gradient-to-r from-teal-400 to-cyan-500 rounded-full transition-all duration-300"
              style={{ left: `${getECPercentage()}%` }}
            />
          </div>
          <div className="flex justify-between text-[8px] text-slate-600 font-bold uppercase tracking-wider">
            <span>Water (0.0)</span>
            <span className="text-teal-500/60">Target (1.5-2.2)</span>
            <span>Strong (4.0)</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LiveGauge;
