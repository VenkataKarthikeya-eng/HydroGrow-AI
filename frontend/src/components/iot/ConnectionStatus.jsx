import React from 'react';
import { Wifi, WifiOff } from 'lucide-react';

function ConnectionStatus({ status }) {
  const isOnline = status === 'connected';
  const isConnecting = status === 'connecting';

  return (
    <div className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-slate-900 bg-slate-950/40 text-[10px] font-black uppercase tracking-wider select-none">
      {isOnline ? (
        <>
          <Wifi className="h-3.5 w-3.5 text-emerald-400 animate-pulse" />
          <span className="text-emerald-400">WebSocket Live</span>
        </>
      ) : isConnecting ? (
        <>
          <div className="h-1.5 w-1.5 rounded-full bg-amber-500 animate-ping" />
          <span className="text-amber-500">Connecting</span>
        </>
      ) : (
        <>
          <WifiOff className="h-3.5 w-3.5 text-rose-500" />
          <span className="text-rose-500">Offline</span>
        </>
      )}
    </div>
  );
}

export default ConnectionStatus;
