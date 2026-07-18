import React, { useState } from 'react';
import { Copy, RefreshCw, Eye, Check } from 'lucide-react';

function MessageActions({ text, onRegenerate, onViewSources, hasSources }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex items-center space-x-2 mt-2 text-[10px] text-slate-500 font-semibold select-none">
      <button
        onClick={handleCopy}
        className="flex items-center space-x-1 hover:text-white transition-all bg-slate-900 border border-slate-850 px-2.5 py-1 rounded-md"
        title="Copy response content"
      >
        {copied ? (
          <>
            <Check className="h-3 w-3 text-emerald-400" />
            <span>Copied!</span>
          </>
        ) : (
          <>
            <Copy className="h-3 w-3" />
            <span>Copy</span>
          </>
        )}
      </button>

      {onRegenerate && (
        <button
          onClick={onRegenerate}
          className="flex items-center space-x-1 hover:text-white transition-all bg-slate-900 border border-slate-850 px-2.5 py-1 rounded-md active:scale-95"
          title="Regenerate this response"
        >
          <RefreshCw className="h-3 w-3" />
          <span>Regenerate</span>
        </button>
      )}

      {hasSources && onViewSources && (
        <button
          onClick={onViewSources}
          className="flex items-center space-x-1 hover:text-emerald-400 text-emerald-500/80 transition-all bg-emerald-950/20 border border-emerald-900/30 px-2.5 py-1 rounded-md"
          title="View citation details"
        >
          <Eye className="h-3 w-3" />
          <span>Sources</span>
        </button>
      )}
    </div>
  );
}

export default MessageActions;
