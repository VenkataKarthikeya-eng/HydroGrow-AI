import React from 'react';
import { Sprout, ChevronDown, Check } from 'lucide-react';

function FarmSwitcher({ farms, activeFarm, onSelectFarm }) {
  const [open, setOpen] = React.useState(false);

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-xs font-bold text-slate-200 transition-all"
      >
        <Sprout className="h-4 w-4 text-emerald-400" />
        <span>{activeFarm?.farm_name || "Select Farm"}</span>
        <ChevronDown className="h-3.5 w-3.5 text-slate-400" />
      </button>

      {open && (
        <div className="absolute top-full left-0 mt-2 w-56 rounded-2xl bg-slate-950 border border-slate-800 shadow-2xl p-2 z-50 space-y-1">
          <span className="text-[9px] font-black uppercase text-slate-500 px-2 py-1 block">My Farms</span>
          {farms?.map((f) => (
            <button
              key={f.id}
              onClick={() => {
                onSelectFarm(f);
                setOpen(false);
              }}
              className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-semibold transition-all ${
                activeFarm?.id === f.id
                  ? 'bg-emerald-500/10 text-emerald-400 font-extrabold'
                  : 'text-slate-300 hover:bg-slate-900'
              }`}
            >
              <span>{f.farm_name}</span>
              {activeFarm?.id === f.id && <Check className="h-3.5 w-3.5 text-emerald-400" />}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default FarmSwitcher;
