import React from 'react';

function AnalyticsLoader() {
  return (
    <div className="space-y-6 animate-pulse select-none">
      {/* KPI Cards Skeleton */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="glass-panel p-5 rounded-2xl border border-slate-900 bg-slate-950/20 h-28 flex flex-col justify-between">
            <div className="w-12 h-2.5 bg-slate-800 rounded"></div>
            <div className="w-20 h-6 bg-slate-850 rounded"></div>
            <div className="w-16 h-2 bg-slate-900 rounded"></div>
          </div>
        ))}
      </div>

      {/* Grid Skeleton */}
      <div className="grid md:grid-cols-3 gap-6">
        {/* Main Chart Skeleton */}
        <div className="md:col-span-2 glass-panel p-6 rounded-2xl border border-slate-900 bg-slate-950/20 h-[360px] flex flex-col justify-between">
          <div className="w-48 h-3.5 bg-slate-800 rounded"></div>
          <div className="flex-grow w-full bg-slate-950/40 rounded-xl my-4 flex items-end justify-around p-4">
            {[30, 45, 60, 40, 70, 90, 85].map((h, i) => (
              <div key={i} className="w-8 bg-slate-900 rounded-t-lg" style={{ height: `${h}%` }}></div>
            ))}
          </div>
          <div className="w-full flex justify-between">
            <div className="w-16 h-2.5 bg-slate-850 rounded"></div>
            <div className="w-16 h-2.5 bg-slate-850 rounded"></div>
          </div>
        </div>

        {/* Small Card Skeleton */}
        <div className="glass-panel p-6 rounded-2xl border border-slate-900 bg-slate-950/20 h-[360px] flex flex-col justify-between">
          <div className="w-36 h-3.5 bg-slate-800 rounded"></div>
          <div className="flex-grow w-full bg-slate-950/40 rounded-xl my-4 flex items-center justify-center">
            <div className="w-32 h-32 rounded-full border-8 border-slate-900 animate-spin"></div>
          </div>
          <div className="w-24 h-2.5 bg-slate-850 rounded mx-auto"></div>
        </div>
      </div>
    </div>
  );
}

export default AnalyticsLoader;
