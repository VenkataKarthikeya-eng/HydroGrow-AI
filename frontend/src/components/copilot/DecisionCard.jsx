import React, { useState } from 'react';
import client from '../../api/client';
import { ThumbsUp, ThumbsDown, CheckCircle2, Zap } from 'lucide-react';

function DecisionCard({ decision, onDecisionUpdated }) {
  const [executing, setExecuting] = useState(false);
  const [feedbacking, setFeedbacking] = useState(false);
  const [msg, setMsg] = useState('');

  const isCritical = decision.priority === "CRITICAL";
  const isHigh = decision.priority === "HIGH";

  const handleExecute = async () => {
    if (!decision.id) return;
    setExecuting(true);
    setMsg('');
    try {
      const res = await client.post(`/api/copilot/execute/${decision.id}`);
      setMsg(res.data.message || 'Action executed successfully.');
      if (onDecisionUpdated) onDecisionUpdated();
    } catch (err) {
      setMsg(err.response?.data?.detail || 'Failed to execute action.');
    } finally {
      setExecuting(false);
    }
  };

  const handleFeedback = async (feedbackType) => {
    if (!decision.id) return;
    setFeedbacking(true);
    try {
      await client.post('/api/copilot/feedback', {
        decision_id: decision.id,
        action_taken: `User submitted feedback: ${feedbackType}`,
        feedback: feedbackType
      });
      setMsg(`Feedback '${feedbackType}' saved.`);
      if (onDecisionUpdated) onDecisionUpdated();
    } catch (err) {
      setMsg('Failed to log feedback.');
    } finally {
      setFeedbacking(false);
    }
  };

  return (
    <div className={`p-5 rounded-3xl border transition-all ${
      isCritical 
        ? 'bg-rose-950/10 border-rose-500/20 shadow-rose-950/5' 
        : isHigh 
        ? 'bg-amber-950/10 border-amber-500/20 shadow-amber-950/5' 
        : 'bg-slate-950/30 border-slate-900'
    } shadow-lg space-y-3`}>
      <div className="flex justify-between items-start">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className={`px-2 py-0.5 rounded text-[8px] font-black uppercase tracking-wider ${
              isCritical ? 'bg-rose-500/20 text-rose-400' : isHigh ? 'bg-amber-500/20 text-amber-400' : 'bg-emerald-500/10 text-emerald-400'
            }`}>
              {decision.priority}
            </span>
            <span className="text-[9px] font-black uppercase text-slate-500 tracking-wider">
              {decision.decision_type}
            </span>
          </div>
          <h4 className="text-sm font-extrabold text-slate-100 leading-snug">{decision.title}</h4>
        </div>
        <div className="text-right">
          <span className="text-xs font-mono font-black text-emerald-400">{decision.confidence_score}%</span>
          <span className="text-[8px] uppercase tracking-wider text-slate-500 block font-bold">Confidence</span>
        </div>
      </div>

      <div className="space-y-2 text-xs">
        <div className="p-3 bg-slate-950/50 rounded-2xl border border-slate-900/60 text-slate-300 space-y-1">
          <p className="text-[9px] uppercase tracking-wider text-slate-500 font-black">AI Diagnosis</p>
          <p className="font-semibold leading-relaxed text-slate-300">{decision.analysis}</p>
        </div>

        <div className="p-3 bg-emerald-500/5 rounded-2xl border border-emerald-500/10 text-emerald-400 space-y-1">
          <p className="text-[9px] uppercase tracking-wider text-emerald-500/60 font-black">Recommended Action</p>
          <p className="font-bold leading-relaxed">{decision.recommended_action}</p>
        </div>
      </div>

      {msg && <p className="text-[10px] font-bold text-emerald-400">{msg}</p>}

      <div className="flex flex-wrap items-center justify-between gap-2 border-t border-slate-900/60 pt-3">
        <div className="flex gap-1.5">
          <button
            onClick={() => handleFeedback('Helpful')}
            disabled={feedbacking}
            className="p-2 rounded-xl bg-slate-900 border border-slate-800 hover:bg-slate-850 text-slate-300 text-xs font-bold transition-all active:scale-95 flex items-center gap-1"
            title="Helpful recommendation"
          >
            <ThumbsUp className="h-3.5 w-3.5 text-emerald-400" />
            <span className="text-[10px]">Helpful</span>
          </button>
          <button
            onClick={() => handleFeedback('Not Helpful')}
            disabled={feedbacking}
            className="p-2 rounded-xl bg-slate-900 border border-slate-800 hover:bg-slate-850 text-slate-300 text-xs font-bold transition-all active:scale-95 flex items-center gap-1"
            title="Not helpful"
          >
            <ThumbsDown className="h-3.5 w-3.5 text-rose-400" />
          </button>
        </div>

        <button
          onClick={handleExecute}
          disabled={executing || decision.status === 'Executed'}
          className={`px-4 py-2 rounded-xl text-xs font-black uppercase tracking-wider transition-all shadow-md active:scale-95 flex items-center gap-1.5 ${
            decision.status === 'Executed'
              ? 'bg-slate-900 text-slate-500 border border-slate-800 cursor-default'
              : 'bg-emerald-500 hover:bg-emerald-400 text-slate-950'
          }`}
        >
          {decision.status === 'Executed' ? (
            <>
              <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" />
              Executed
            </>
          ) : (
            <>
              <Zap className="h-3.5 w-3.5 fill-current" />
              {executing ? 'Executing...' : 'Execute Action'}
            </>
          )}
        </button>
      </div>
    </div>
  );
}

export default DecisionCard;
