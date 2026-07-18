import React, { useState } from 'react';
import client from '../../api/client';
import { Send, Bot, User, Sparkles } from 'lucide-react';

function CopilotChatPanel() {
  const [messages, setMessages] = useState([
    {
      sender: 'ai',
      text: "👋 Hi! I'm your Autonomous Farm Copilot. Ask me to **analyze your farm**, **optimize greenhouse setpoints**, or **explain active crop issues**."
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const quickPrompts = [
    "Analyze my farm condition",
    "What should I do today?",
    "Optimize my greenhouse",
    "Why is yield decreasing?"
  ];

  const handleSend = async (queryText) => {
    const textToSend = queryText || input;
    if (!textToSend.trim() || loading) return;

    const userMsg = { sender: 'user', text: textToSend };
    setMessages(prev => [...prev, userMsg]);
    if (!queryText) setInput('');
    setLoading(true);

    try {
      const res = await client.post('/api/chat', { message: textToSend });
      const aiReply = res.data.response || res.data.message || "I've analyzed your request.";
      setMessages(prev => [...prev, { sender: 'ai', text: aiReply }]);
    } catch (err) {
      setMessages(prev => [...prev, { sender: 'ai', text: "Sorry, I encountered an issue analyzing your query." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl flex flex-col h-[480px]">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3 mb-3 shrink-0">
        <div className="flex items-center gap-2">
          <Bot className="h-4 w-4 text-emerald-400" />
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Copilot Assistant Dialogue</h4>
        </div>
        <Sparkles className="h-3.5 w-3.5 text-emerald-400 animate-pulse" />
      </div>

      <div className="flex-1 overflow-y-auto space-y-3 pr-1 scrollbar-thin mb-3">
        {messages.map((m, idx) => (
          <div key={idx} className={`flex gap-2.5 ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            {m.sender === 'ai' && (
              <div className="h-6 w-6 rounded-full bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 shrink-0 mt-0.5">
                <Bot className="h-3.5 w-3.5" />
              </div>
            )}
            <div className={`p-3 rounded-2xl text-xs leading-relaxed max-w-[85%] ${
              m.sender === 'user'
                ? 'bg-emerald-500 text-slate-950 font-bold rounded-tr-none'
                : 'bg-slate-950/60 border border-slate-900 text-slate-200 rounded-tl-none font-medium whitespace-pre-wrap'
            }`}>
              {m.text}
            </div>
            {m.sender === 'user' && (
              <div className="h-6 w-6 rounded-full bg-slate-800 flex items-center justify-center text-slate-400 shrink-0 mt-0.5">
                <User className="h-3.5 w-3.5" />
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="flex gap-2 text-xs text-slate-500 items-center">
            <Bot className="h-3.5 w-3.5 text-emerald-400 animate-spin" />
            Evaluating multi-agent telemetry...
          </div>
        )}
      </div>

      <div className="space-y-2 shrink-0 border-t border-slate-900 pt-3">
        <div className="flex flex-wrap gap-1.5">
          {quickPrompts.map((p, i) => (
            <button
              key={i}
              onClick={() => handleSend(p)}
              className="px-2 py-1 rounded-lg bg-slate-900 border border-slate-800 hover:bg-slate-850 text-slate-400 hover:text-slate-200 text-[9px] font-bold transition-all"
            >
              {p}
            </button>
          ))}
        </div>

        <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask your AI Farm Manager..."
            className="flex-grow bg-slate-950/80 border border-slate-900 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
          />
          <button
            type="submit"
            disabled={loading}
            className="px-3 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs transition-all flex items-center justify-center"
          >
            <Send className="h-3.5 w-3.5" />
          </button>
        </form>
      </div>
    </div>
  );
}

export default CopilotChatPanel;
