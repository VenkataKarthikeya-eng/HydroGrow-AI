import React from 'react';
import { Bot } from 'lucide-react';

function TypingIndicator({ message = "HydroGrow AI is typing..." }) {
  return (
    <div className="flex gap-3 my-4 mr-auto max-w-lg items-center animate-pulse">
      <div className="p-2 h-fit rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
        <Bot className="h-4 w-4 animate-spin" />
      </div>
      <div className="glass-panel text-slate-400 border-slate-850 px-4 py-2.5 rounded-2xl rounded-tl-none text-xs flex items-center gap-2">
        <span>{message}</span>
        <div className="flex space-x-1 ml-1">
          <div className="w-1 h-1 bg-emerald-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
          <div className="w-1 h-1 bg-emerald-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
          <div className="w-1 h-1 bg-emerald-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
        </div>
      </div>
    </div>
  );
}

export default TypingIndicator;
