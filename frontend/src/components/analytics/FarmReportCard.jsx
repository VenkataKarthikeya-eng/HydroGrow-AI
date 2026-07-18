import React from 'react';
import { Bot, CheckCircle, AlertTriangle, Lightbulb } from 'lucide-react';

function FarmReportCard({ report }) {
  if (!report) return null;

  const getSection = (title) => {
    const lines = report.split('\n');
    let content = [];
    let start = false;
    
    for (const line of lines) {
      if (line.includes(title)) {
        start = true;
        continue;
      }
      if (start) {
        if (line.startsWith('###') || line.includes('🌱 **Analysis:**') || line.includes('📊 **Evidence:**') || line.includes('💡 **Recommendation:**')) {
          break;
        }
        content.push(line);
      }
    }
    return content.join('\n').trim();
  };

  const analysis = getSection('🌱 **Analysis:**');
  const evidence = getSection('📊 **Evidence:**');
  const recommendation = getSection('💡 **Recommendation:**');

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-6">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div className="flex items-center space-x-2">
          <Bot className="h-5 w-5 text-emerald-400" />
          <h3 className="text-xs font-black uppercase text-white tracking-wider">AI Farm Advisor Report</h3>
        </div>
      </div>

      <div className="space-y-4">
        {analysis && (
          <div className="space-y-1.5">
            <span className="text-[9px] text-slate-500 font-extrabold uppercase tracking-wider block">Executive Summary</span>
            <p className="text-slate-300 text-xs leading-relaxed font-medium">{analysis}</p>
          </div>
        )}

        {evidence && (
          <div className="p-4 rounded-2xl bg-slate-950/40 border border-slate-900 space-y-2">
            <span className="text-[9px] text-slate-500 font-extrabold uppercase tracking-wider block">Diagnostics & Factors</span>
            <div className="text-slate-300 text-xs space-y-2 font-medium">
              {evidence.split('\n').map((line, i) => {
                if (line.trim().startsWith('-')) {
                  const contentText = line.replace(/^-/, '').trim();
                  const isIssue = line.toLowerCase().includes('issue') || line.toLowerCase().includes('detected');
                  return (
                    <div key={i} className="flex items-start gap-2">
                      {isIssue ? (
                        <AlertTriangle className="h-4 w-4 text-amber-500 shrink-0 mt-0.5" />
                      ) : (
                        <CheckCircle className="h-4 w-4 text-emerald-500 shrink-0 mt-0.5" />
                      )}
                      <span>{contentText}</span>
                    </div>
                  );
                }
                return <p key={i} className="leading-relaxed">{line}</p>;
              })}
            </div>
          </div>
        )}

        {recommendation && (
          <div className="p-4 rounded-2xl bg-emerald-500/5 border border-emerald-500/10 space-y-2">
            <span className="text-[9px] text-emerald-400 font-extrabold uppercase tracking-wider block flex items-center gap-1">
              <Lightbulb className="h-3.5 w-3.5" /> Action Plan & Optimization
            </span>
            <div className="text-slate-300 text-xs space-y-1.5 font-semibold">
              {recommendation.split('\n').map((line, i) => (
                <p key={i} className="leading-relaxed">{line}</p>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default FarmReportCard;
