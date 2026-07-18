import React from 'react';
import { Bot, User, FileText, Sparkles } from 'lucide-react';
import MessageActions from './chat/MessageActions';

function ChatMessage({ message, onRegenerate, onViewSources }) {
  const { role, content, sources, timestamp, isError } = message;
  const isUser = role === 'user';

  // Inline markdown parser
  const parseInline = (text) => {
    const parts = [];
    const regex = /(\*\*.*?\*\*|`.*?`)/g;
    const matches = text.split(regex);
    
    matches.forEach((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        parts.push(<strong key={i} className="font-bold text-white">{part.slice(2, -2)}</strong>);
      } else if (part.startsWith('`') && part.endsWith('`')) {
        parts.push(
          <code key={i} className="bg-slate-950 text-emerald-400 px-1.5 py-0.5 rounded text-[10px] font-mono border border-slate-900">
            {part.slice(1, -1)}
          </code>
        );
      } else {
        parts.push(part);
      }
    });
    
    return parts;
  };

  // Block markdown parser
  const renderMarkdown = (text) => {
    if (!text) return null;
    
    const lines = text.split('\n');
    let codeContent = [];
    let inCode = false;
    const renderedElements = [];

    lines.forEach((line, index) => {
      // Code Block check
      if (line.trim().startsWith('```')) {
        if (inCode) {
          renderedElements.push(
            <pre key={`code-${index}`} className="bg-slate-950 border border-slate-900 p-3 rounded-lg overflow-x-auto text-emerald-400 font-mono text-[10px] my-2 select-text">
              <code>{codeContent.join('\n')}</code>
            </pre>
          );
          codeContent = [];
          inCode = false;
        } else {
          inCode = true;
        }
        return;
      }

      if (inCode) {
        codeContent.push(line);
        return;
      }

      // Headers check
      if (line.startsWith('#')) {
        const match = line.match(/^(#{1,6})\s+(.*)$/);
        if (match) {
          const level = match[1].length;
          const inlineContent = parseInline(match[2]);
          if (level === 1) {
            renderedElements.push(<h1 key={index} className="text-base font-bold text-white mt-3 mb-2 border-b border-slate-900 pb-1">{inlineContent}</h1>);
          } else if (level === 2) {
            renderedElements.push(<h2 key={index} className="text-sm font-bold text-slate-100 mt-3 mb-2">{inlineContent}</h2>);
          } else {
            renderedElements.push(<h3 key={index} className="text-xs font-bold text-emerald-400 mt-2.5 mb-1 uppercase tracking-wide">{inlineContent}</h3>);
          }
          return;
        }
      }

      // Bullet List check
      if (line.trim().startsWith('-') || line.trim().startsWith('*')) {
        const match = line.match(/^[-*]\s+(.*)$/);
        if (match) {
          renderedElements.push(
            <li key={index} className="ml-4 list-disc text-slate-300 text-xs my-0.5 leading-relaxed">
              {parseInline(match[1])}
            </li>
          );
          return;
        }
      }

      // Numeric List check
      if (line.match(/^\d+\.\s+/)) {
        const match = line.match(/^\d+\.\s+(.*)$/);
        if (match) {
          renderedElements.push(
            <li key={index} className="ml-4 list-decimal text-slate-300 text-xs my-0.5 leading-relaxed">
              {parseInline(match[1])}
            </li>
          );
          return;
        }
      }

      // Paragraph / Empty line check
      if (line.trim() === '') {
        renderedElements.push(<div key={index} className="h-1.5"></div>);
      } else {
        renderedElements.push(
          <p key={index} className="text-slate-300 text-xs leading-relaxed my-1">
            {parseInline(line)}
          </p>
        );
      }
    });

    return renderedElements;
  };

  return (
    <div className={`flex gap-3 my-4 max-w-3xl ${isUser ? 'ml-auto justify-end' : 'mr-auto'}`}>
      {/* Icon Area */}
      {!isUser && (
        <div className={`p-2 h-fit rounded-lg shrink-0 border ${isError ? 'bg-rose-500/10 border-rose-500/20 text-rose-400' : 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'}`}>
          <Bot className="h-4 w-4" />
        </div>
      )}

      {/* Bubble Container */}
      <div className={`flex flex-col gap-1.5 select-text ${isUser ? 'items-end' : 'items-start'}`}>
        <div className={`px-4 py-3 rounded-2xl border text-xs shadow-md ${
          isUser 
            ? 'bg-slate-900 border-slate-800 text-slate-200 rounded-tr-none' 
            : isError 
              ? 'bg-rose-950/20 border-rose-500/20 text-rose-300 rounded-tl-none'
              : 'glass-panel text-slate-300 border-slate-800/80 rounded-tl-none'
        }`}>
          {renderMarkdown(content)}

          {/* Sources panel */}
          {sources && sources.length > 0 && (
            <div className="mt-3 pt-2.5 border-t border-slate-900 flex flex-col gap-1.5">
              <span className="text-[10px] text-slate-500 font-extrabold uppercase tracking-wider flex items-center gap-1">
                <FileText className="h-3 w-3" /> Referenced Knowledge Sources
              </span>
              <div className="flex flex-wrap gap-1">
                {sources.map((source, i) => (
                  <span key={i} className="bg-slate-950 px-2 py-0.5 rounded border border-slate-900 text-[10px] text-slate-400 font-mono flex items-center gap-1">
                    <Sparkles className="h-2.5 w-2.5 text-emerald-500/70" />
                    {source.replace(/_/g, ' ')}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Action buttons (only for assistant and if content exists) */}
          {!isUser && content && (
            <MessageActions
              text={content}
              onRegenerate={onRegenerate}
              onViewSources={onViewSources ? () => onViewSources(sources) : null}
              hasSources={sources && sources.length > 0}
            />
          )}
        </div>
        
        {/* Timestamp */}
        <span className="text-[9px] text-slate-600 px-1 font-mono">{timestamp}</span>
      </div>

      {isUser && (
        <div className="p-2 h-fit rounded-lg shrink-0 border bg-slate-900 border-slate-800 text-slate-400">
          <User className="h-4 w-4" />
        </div>
      )}
    </div>
  );
}

export default ChatMessage;
