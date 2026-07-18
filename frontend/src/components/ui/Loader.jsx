import React from 'react';
import { Loader2, Sprout } from 'lucide-react';

export default function Loader({
  message = 'HydroGrow AI processing...',
  steps = [],
  currentStep = 0,
}) {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-center space-y-4">
      <div className="relative flex items-center justify-center">
        <div className="w-16 h-16 rounded-full border-4 border-emerald-100 dark:border-emerald-950 border-t-emerald-600 dark:border-t-emerald-400 animate-spin" />
        <Sprout className="w-6 h-6 text-emerald-600 dark:text-emerald-400 absolute" />
      </div>
      
      <div>
        <h4 className="text-base font-bold text-slate-900 dark:text-slate-100">{message}</h4>
        {steps.length > 0 && (
          <div className="mt-4 space-y-2 max-w-sm mx-auto">
            {steps.map((stepText, idx) => {
              const isDone = idx < currentStep;
              const isCurrent = idx === currentStep;
              return (
                <div
                  key={idx}
                  className={`flex items-center gap-2 text-xs font-medium px-3 py-1.5 rounded-md transition-all ${
                    isDone
                      ? 'text-emerald-700 dark:text-emerald-300 bg-emerald-50 dark:bg-emerald-950/40'
                      : isCurrent
                      ? 'text-emerald-600 dark:text-emerald-400 bg-emerald-100/60 dark:bg-emerald-900/40 font-bold animate-pulse'
                      : 'text-slate-400 dark:text-slate-600'
                  }`}
                >
                  {isCurrent ? (
                    <Loader2 className="w-3.5 h-3.5 animate-spin text-emerald-600" />
                  ) : isDone ? (
                    <span className="text-emerald-600 font-bold">✓</span>
                  ) : (
                    <span className="w-3.5 h-3.5 inline-block rounded-full bg-slate-200 dark:bg-slate-700" />
                  )}
                  <span>{stepText}</span>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
