import React, { useState, useEffect } from 'react';
import client from '../../api/client';
import { Users, UserPlus, Shield, Trash2 } from 'lucide-react';

function TeamManagement({ activeFarm }) {
  const [members, setMembers] = useState([]);
  const [email, setEmail] = useState('');
  const [role, setRole] = useState('WORKER');
  const [msg, setMsg] = useState('');

  const fetchMembers = async () => {
    if (!activeFarm?.id) return;
    try {
      const res = await client.get(`/api/farms/${activeFarm.id}/members`);
      setMembers(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchMembers();
  }, [activeFarm]);

  const handleAddMember = async (e) => {
    e.preventDefault();
    if (!email || !activeFarm?.id) return;
    try {
      const res = await client.post(`/api/farms/${activeFarm.id}/members/add`, {
        email,
        role
      });
      setMsg(res.data.message);
      setEmail('');
      fetchMembers();
    } catch (err) {
      setMsg(err.response?.data?.detail || 'Failed to add member.');
    }
  };

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-6">
      <div className="flex justify-between items-center border-b border-slate-900 pb-3">
        <div>
          <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Farmer Team Collaboration & RBAC</h4>
          <p className="text-[10px] text-slate-500 font-semibold">Assign OWNER, MANAGER, WORKER & VIEWER roles</p>
        </div>
        <Users className="h-4 w-4 text-emerald-400" />
      </div>

      <form onSubmit={handleAddMember} className="flex flex-col sm:flex-row gap-3 bg-slate-950/40 p-4 rounded-2xl border border-slate-900">
        <input
          type="email"
          placeholder="Member Email Address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="flex-grow px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-100 focus:outline-none focus:border-emerald-500"
          required
        />
        <select
          value={role}
          onChange={(e) => setRole(e.target.value)}
          className="px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
        >
          <option value="MANAGER">MANAGER</option>
          <option value="WORKER">WORKER</option>
          <option value="VIEWER">VIEWER</option>
        </select>
        <button
          type="submit"
          className="px-4 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase tracking-wider transition-all flex items-center justify-center gap-1.5"
        >
          <UserPlus className="h-4 w-4" /> Invite Member
        </button>
      </form>

      {msg && <p className="text-xs text-emerald-400 font-semibold">{msg}</p>}

      <div className="space-y-2">
        {members.map((m) => (
          <div key={m.id} className="p-3.5 rounded-2xl bg-slate-950/40 border border-slate-900 flex justify-between items-center text-xs">
            <div>
              <span className="font-bold text-slate-100 block">{m.username}</span>
              <span className="text-[10px] text-slate-500">{m.email}</span>
            </div>
            <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono font-black text-[9px]">
              {m.role}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default TeamManagement;
