import React, { useState, useEffect } from 'react';
import client from '../../api/client';
import { BookOpen, Sparkles } from 'lucide-react';

function KnowledgeCenter() {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    client.get('/api/marketplace/knowledge-base')
      .then(res => setArticles(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-6">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Agricultural Knowledge Center</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Agronomic research, diagnostic guides, and solution chemistry articles</p>
        </div>
        <BookOpen className="h-4 w-4 text-emerald-400" />
      </div>

      <div className="space-y-4">
        {articles.map((a) => (
          <div key={a.id} className="p-4 rounded-2xl bg-slate-950/40 border border-slate-900 space-y-2">
            <div className="flex justify-between items-start">
              <h5 className="font-extrabold text-slate-100 text-sm">{a.title}</h5>
              <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 text-[9px] font-mono font-bold">
                {a.category}
              </span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">{a.content}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default KnowledgeCenter;
