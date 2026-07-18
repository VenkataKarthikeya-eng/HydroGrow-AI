import React, { useRef, useEffect } from 'react';
import { Send } from 'lucide-react';

function ChatInput({ value, onChange, onSubmit, disabled, placeholder }) {
  const textareaRef = useRef(null);

  // Auto resize textarea height based on content size
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`;
    }
  }, [value]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSubmit(e);
    }
  };

  return (
    <form onSubmit={onSubmit} className="shrink-0 pt-2 border-t border-slate-900 flex gap-3 items-end w-full">
      <div className="flex-grow relative bg-slate-900 border border-slate-800 rounded-xl overflow-hidden focus-within:border-emerald-500/65 transition-all">
        <textarea
          ref={textareaRef}
          rows={1}
          value={value}
          onChange={onChange}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          placeholder={placeholder}
          className="w-full bg-transparent py-3.5 pl-4 pr-12 text-xs text-white placeholder-slate-500 focus:outline-none resize-none max-h-[120px] scrollbar-none min-h-[44px]"
          style={{ boxSizing: 'border-box' }}
        />
      </div>
      <button
        type="submit"
        disabled={!value.trim() || disabled}
        className="p-3 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 disabled:opacity-50 text-white rounded-xl shadow-lg transition-all active:scale-95 shrink-0 flex items-center justify-center h-[48px] w-[48px]"
      >
        <Send className="h-4 w-4" />
      </button>
    </form>
  );
}

export default ChatInput;
