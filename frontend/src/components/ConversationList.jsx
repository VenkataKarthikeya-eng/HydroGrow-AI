import React from 'react';
import { MessageSquare, Plus, Trash2 } from 'lucide-react';

function ConversationList({ 
  conversations, 
  activeId, 
  onSelect, 
  onNewThread,
  onDelete
}) {
  const getCleanTitle = (title) => {
    return title || 'Untitled Thread';
  };

  return (
    <div className="flex flex-col h-full bg-slate-950/40 rounded-2xl border border-slate-900 overflow-hidden">
      {/* Header */}
      <div className="p-4 border-b border-slate-900 flex justify-between items-center bg-slate-950/60">
        <div>
          <h3 className="text-xs font-black uppercase text-slate-400 tracking-wider">Grower Logs</h3>
          <p className="text-[10px] text-slate-500 font-medium">Persisted memory threads</p>
        </div>
        <button
          onClick={() => onNewThread('New grow room query')}
          className="p-1.5 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/30 text-emerald-400 transition-all flex items-center justify-center"
          title="Start new thread"
        >
          <Plus className="h-4 w-4" />
        </button>
      </div>

      {/* List */}
      <div className="flex-grow overflow-y-auto p-2.5 space-y-1 scrollbar-thin">
        {conversations.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-48 text-center px-4 py-8">
            <MessageSquare className="h-8 w-8 text-slate-600 mb-2" />
            <p className="text-[11px] text-slate-500 font-semibold">No threads found</p>
            <p className="text-[9px] text-slate-600 mt-1 leading-relaxed">Start typing in the chat to create a memory log thread.</p>
          </div>
        ) : (
          conversations.map((conv) => {
            const isActive = conv.id === activeId;
            return (
              <div
                key={conv.id}
                className={`group flex items-center justify-between rounded-xl p-3 cursor-pointer border transition-all ${
                  isActive 
                    ? 'bg-slate-900 border-slate-800 text-white' 
                    : 'bg-transparent border-transparent hover:bg-slate-950 hover:border-slate-900 text-slate-400 hover:text-slate-200'
                }`}
                onClick={() => onSelect(conv.id)}
              >
                <div className="flex items-center space-x-2.5 min-w-0 flex-grow">
                  <MessageSquare className={`h-4 w-4 flex-shrink-0 ${isActive ? 'text-emerald-400' : 'text-slate-600 group-hover:text-slate-400'}`} />
                  <span className="text-[11px] font-semibold truncate leading-none">
                    {getCleanTitle(conv.title)}
                  </span>
                </div>
                {onDelete && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onDelete(conv.id);
                    }}
                    className="opacity-0 group-hover:opacity-100 p-1 rounded-md hover:bg-rose-950/20 text-slate-500 hover:text-rose-400 transition-all ml-2"
                    title="Delete thread"
                  >
                    <Trash2 className="h-3.5 w-3.5" />
                  </button>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

export default ConversationList;
