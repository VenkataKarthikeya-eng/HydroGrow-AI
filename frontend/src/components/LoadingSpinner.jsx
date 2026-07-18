import React from 'react';
import { Sprout } from 'lucide-react';

function LoadingSpinner({ message = 'Loading AI diagnostics...' }) {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 text-center">
      <div className="relative flex items-center justify-center mb-4">
        {/* Pulse Ring */}
        <div className="absolute w-16 h-16 rounded-full border-4 border-emerald-500/20 animate-ping"></div>
        {/* Spinner ring */}
        <div className="w-14 h-14 rounded-full border-4 border-t-emerald-500 border-r-transparent border-b-slate-800 border-l-slate-800 animate-spin"></div>
        {/* Icon in center */}
        <Sprout className="absolute h-6 w-6 text-emerald-400 animate-bounce" />
      </div>
      <p className="text-slate-400 text-sm font-medium animate-pulse">{message}</p>
    </div>
  );
}

export default LoadingSpinner;
