import React from 'react';
import { Cloud, Server, Database, ShieldCheck } from 'lucide-react';
import Card from '../components/ui/Card';
import Badge from '../components/ui/Badge';

export default function CloudDashboard() {
  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-300">
      <div className="border-b border-slate-200 dark:border-slate-800 pb-6">
        <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
          <Cloud className="w-4 h-4" /> Cloud & Edge Infrastructure
        </div>
        <h1 className="text-3xl font-black text-slate-900 dark:text-white mt-1">
          Cloud Operations & Edge Nodes
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Status of high-availability cloud endpoints, local greenhouse gateway nodes, and PostgreSQL databases.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card padding="p-8" header="API Gateway Node">
          <div className="space-y-2">
            <div className="text-2xl font-black text-emerald-600">99.99% Uptime</div>
            <p className="text-xs text-slate-500">Latency: 14ms average HTTP response time.</p>
          </div>
        </Card>

        <Card padding="p-8" header="Greenhouse Edge Gateway">
          <div className="space-y-2">
            <div className="text-2xl font-black text-slate-900 dark:text-white">Connected</div>
            <p className="text-xs text-slate-500">Hardware Node #01: Streaming telemetry via MQTT.</p>
          </div>
        </Card>

        <Card padding="p-8" header="PostgreSQL Storage">
          <div className="space-y-2">
            <div className="text-2xl font-black text-slate-900 dark:text-white">Healthy</div>
            <p className="text-xs text-slate-500">Encrypted backups synced every 6 hours.</p>
          </div>
        </Card>
      </div>
    </div>
  );
}
