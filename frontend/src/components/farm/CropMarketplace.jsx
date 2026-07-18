import React, { useState, useEffect } from 'react';
import client from '../../api/client';
import { ShoppingBag, Sprout, Sparkles } from 'lucide-react';

function CropMarketplace() {
  const [templates, setTemplates] = useState([]);

  useEffect(() => {
    client.get('/api/marketplace/templates')
      .then(res => setTemplates(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-6">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Crop Configuration Marketplace</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Community-verified optimal hydroponic recipes & growth curves</p>
        </div>
        <ShoppingBag className="h-4 w-4 text-emerald-400" />
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {templates.map((t) => (
          <div key={t.id} className="p-4 rounded-2xl bg-slate-950/40 border border-slate-900 space-y-3">
            <div className="flex justify-between items-start">
              <div>
                <h5 className="font-extrabold text-slate-100 text-sm">{t.name}</h5>
                <span className="text-[10px] text-slate-500">{t.crop_type} • {t.growth_duration} Days Cycle</span>
              </div>
              <Sparkles className="h-4 w-4 text-emerald-400" />
            </div>

            <div className="grid grid-cols-3 gap-2 text-center text-xs p-2 rounded-xl bg-slate-900/60">
              <div>
                <span className="text-[9px] text-slate-500 block uppercase">Temp</span>
                <span className="font-mono font-bold text-slate-200">{t.optimal_temperature}°C</span>
              </div>
              <div>
                <span className="text-[9px] text-slate-500 block uppercase">pH Target</span>
                <span className="font-mono font-bold text-slate-200">{t.optimal_ph}</span>
              </div>
              <div>
                <span className="text-[9px] text-slate-500 block uppercase">EC Target</span>
                <span className="font-mono font-bold text-slate-200">{t.optimal_ec} mS</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default CropMarketplace;
