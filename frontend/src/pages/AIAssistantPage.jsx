import React, { useContext, useState, useRef, useEffect } from 'react';
import { AppContext } from '../context/AppContext';
import { Bot, Send, Trash2, Sparkles, HelpCircle, ShieldCheck, ArrowRight, User, BookOpen, ArrowDown, ArrowUp } from 'lucide-react';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';

const QUICK_QUESTIONS = [
  { text: "Why is my lettuce yield prediction lower than expected?", icon: "📉" },
  { text: "How can I prevent root rot (Pythium) in hydroponics?", icon: "🌱" },
  { text: "What is the optimal water pH and EC range for lettuce?", icon: "🧪" },
  { text: "How to fix tip-burn on inner leaves?", icon: "🥬" }
];

function renderFormattedMessage(text) {
  if (!text) return null;

  const lines = text.split('\n');
  return lines.map((line, lineIdx) => {
    const parts = line.split(/(\*\*.*?\*\*)/g);
    const formattedLine = parts.map((part, partIdx) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return (
          <strong key={partIdx} className="font-extrabold text-emerald-600 dark:text-emerald-400">
            {part.slice(2, -2)}
          </strong>
        );
      }
      return part;
    });

    return (
      <React.Fragment key={lineIdx}>
        {formattedLine}
        {lineIdx < lines.length - 1 && <br />}
      </React.Fragment>
    );
  });
}

export default function AIAssistantPage() {
  const {
    chatHistory,
    isChatting,
    sendChatMessage,
    clearChat,
    user
  } = useContext(AppContext);

  const [input, setInput] = useState('');
  const [showScrollBottom, setShowScrollBottom] = useState(false);

  const chatContainerRef = useRef(null);
  const messagesEndRef = useRef(null);

  // Auto-scroll to newest message whenever history changes or AI starts typing
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleScroll = () => {
    if (!chatContainerRef.current) return;
    const { scrollTop, scrollHeight, clientHeight } = chatContainerRef.current;
    
    // Show scroll down button if user scrolled away from bottom (more than 60px)
    const scrolledAway = scrollHeight - scrollTop - clientHeight > 60;
    setShowScrollBottom(scrolledAway);
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory, isChatting]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isChatting) return;
    const msgText = input;
    setInput('');
    await sendChatMessage(msgText);
  };

  const handleQuickQuestion = async (question) => {
    if (isChatting) return;
    await sendChatMessage(question);
  };

  return (
    <div className="chat-wrapper max-w-5xl mx-auto w-full animate-in fade-in duration-300 overflow-hidden">
      
      {/* 1. Agronomist Copilot Header (Fixed Top) */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-3 mb-3 shrink-0">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
            <Bot className="w-4 h-4" /> RAG Agronomist Assistant
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white tracking-tight mt-0.5">
            Agronomist Copilot
          </h1>
        </div>

        <div className="flex items-center gap-3">
          <Badge variant="optimized" className="px-3 py-1 text-xs">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" /> RAG Engine Active
          </Badge>
          {chatHistory.length > 0 && (
            <Button variant="outline" size="sm" onClick={clearChat} icon={Trash2}>
              Clear Chat
            </Button>
          )}
        </div>
      </div>

      {/* 2. ChatGPT-Style Fixed Container */}
      <Card padding="p-0" className="flex-1 min-h-0 flex flex-col bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-lg relative overflow-hidden">
        
        {/* 3. Scrollable Conversation Area (.chat-messages) */}
        <div 
          ref={chatContainerRef}
          onScroll={handleScroll}
          className="chat-messages custom-scrollbar p-4 sm:p-6 space-y-6 pr-3"
        >
          
          {/* Welcome Screen when Chat is Empty */}
          {chatHistory.length === 0 && (
            <div className="text-center py-8 px-4 space-y-6 max-w-lg mx-auto">
              <div className="w-14 h-14 rounded-2xl bg-emerald-50 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400 mx-auto flex items-center justify-center border border-emerald-100 dark:border-emerald-900 shadow-xs">
                <Bot className="w-7 h-7" />
              </div>
              <div className="space-y-1.5">
                <h3 className="text-lg font-bold text-slate-900 dark:text-white">Ask Anything About Your Hydroponic Crop</h3>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  Connected to our specialized crop science RAG index loaded with hydroponics research manuals and pathology guides.
                </p>
              </div>

              {/* Quick Questions Chips */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-left pt-2">
                {QUICK_QUESTIONS.map((q, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleQuickQuestion(q.text)}
                    className="p-3 rounded-xl border border-slate-200 dark:border-slate-800 hover:border-emerald-500 bg-slate-50 dark:bg-slate-800/50 hover:bg-emerald-50/50 text-xs text-slate-700 dark:text-slate-200 transition-all font-medium flex items-center gap-2 group"
                  >
                    <span className="text-base">{q.icon}</span>
                    <span className="group-hover:text-emerald-600 transition-colors">{q.text}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Chat Messages */}
          {chatHistory.map((msg) => {
            const isUser = msg.role === 'user';
            return (
              <div
                key={msg.id}
                className={`flex items-start gap-3 ${isUser ? 'flex-row-reverse' : ''}`}
              >
                {/* User / AI Avatar */}
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-extrabold shrink-0 shadow-xs ${
                    isUser
                      ? 'bg-slate-900 text-white dark:bg-slate-100 dark:text-slate-900'
                      : 'bg-emerald-600 text-white'
                  }`}
                >
                  {isUser ? (user?.name ? user.name[0].toUpperCase() : 'K') : <Bot className="w-4.5 h-4.5" />}
                </div>

                {/* Message Bubble Container (.message-bubble) */}
                <div className={`message-bubble space-y-2 ${isUser ? 'text-right' : 'text-left'}`}>
                  <div
                    className={`p-4 rounded-2xl text-sm font-normal leading-relaxed inline-block break-words ${
                      isUser
                        ? 'bg-emerald-600 text-white rounded-tr-none shadow-xs'
                        : 'bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-100 border border-slate-200/80 dark:border-slate-700/80 rounded-tl-none'
                    }`}
                  >
                    {renderFormattedMessage(msg.content) || (isChatting && !isUser ? 'Typing agronomist response...' : '')}
                  </div>

                  {/* Sources Citation Pill */}
                  {msg.sources && msg.sources.length > 0 && (
                    <div className="flex flex-wrap items-center gap-2 text-xs pt-1">
                      <span className="text-slate-400 font-bold text-[11px] uppercase tracking-wider">Sources:</span>
                      {msg.sources.map((src, i) => (
                        <span key={i} className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md bg-emerald-50 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-300 text-[11px] font-semibold border border-emerald-200/50 dark:border-emerald-900/50">
                          <BookOpen className="w-3 h-3 text-emerald-600" /> {src.title} ({src.page})
                        </span>
                      ))}
                    </div>
                  )}

                </div>
              </div>
            );
          })}

          <div ref={messagesEndRef} />
        </div>

        {/* 4. Floating Scroll to Latest Button */}
        {showScrollBottom && (
          <div className="absolute right-6 bottom-20 z-20">
            <button
              onClick={scrollToBottom}
              title="Scroll to Latest Message"
              className="p-2.5 rounded-full bg-emerald-600 text-white border border-emerald-500 shadow-xl hover:bg-emerald-500 transition-all transform hover:scale-105 flex items-center gap-1.5 text-xs font-bold px-4 py-2"
            >
              <ArrowDown className="w-4 h-4" />
              <span>↓ Scroll to latest</span>
            </button>
          </div>
        )}

        {/* 5. Fixed Bottom Message Input Box (Shrink-0) */}
        <form onSubmit={handleSend} className="p-4 bg-slate-50 dark:bg-slate-900/95 border-t border-slate-200 dark:border-slate-800 flex items-center gap-3 shrink-0">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isChatting}
            placeholder="Ask about pH, EC, Pythium, or yield optimization..."
            className="flex-1 px-4 py-3 text-sm rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-950 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-emerald-500 focus:outline-none font-medium"
          />
          <Button variant="primary" type="submit" isLoading={isChatting} icon={Send} className="shrink-0 shadow-sm">
            Send
          </Button>
        </form>

      </Card>
    </div>
  );
}
