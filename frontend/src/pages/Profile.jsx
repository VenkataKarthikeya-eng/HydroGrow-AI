import React, { useContext, useState } from 'react';
import { User, Shield, Sun, Moon, Download, Share2, Sparkles, CheckCircle2, History, Sprout } from 'lucide-react';
import { AppContext } from '../context/AppContext';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';

export default function Profile() {
  const { user, setUser, theme, toggleTheme, predictionResult } = useContext(AppContext);
  const [downloading, setDownloading] = useState(false);

  const mockHistory = [
    { id: 1, date: 'July 18, 2026', crop: 'Butterhead Lettuce', yieldGrams: '382.7g', confidence: '91%', health: 'Excellent', status: 'Optimized' },
    { id: 2, date: 'July 11, 2026', crop: 'Butterhead Lettuce', yieldGrams: '365.4g', confidence: '93%', health: 'Good', status: 'Optimized' },
    { id: 3, date: 'July 04, 2026', crop: 'Butterhead Lettuce', yieldGrams: '340.0g', confidence: '89%', health: 'Excellent', status: 'Optimized' },
  ];

  const handleExportPDF = () => {
    setDownloading(true);
    setTimeout(() => {
      setDownloading(false);
      window.print();
    }, 800);
  };

  return (
    <div className="max-w-5xl mx-auto space-y-8 animate-in fade-in duration-300">
      
      {/* Title */}
      <div className="border-b border-slate-200 dark:border-slate-800 pb-6">
        <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
          <User className="w-4 h-4" /> Grower Account & History
        </div>
        <h1 className="text-3xl font-black text-slate-900 dark:text-white mt-1">
          Profile & Farm Settings
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Manage farm credentials, system preferences, theme modes, and past diagnostic reports.
        </p>
      </div>

      {/* Profile Header Box */}
      <div className="saas-card p-6 sm:p-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-2xl bg-emerald-600 text-white text-2xl font-black flex items-center justify-center shadow-md">
            {user?.name ? user.name[0].toUpperCase() : 'K'}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-xl font-black text-slate-900 dark:text-white">{user?.name || 'Karthikeya Cherukuri'}</h2>
              <Badge variant="brand">Verified Grower</Badge>
              <Badge variant="optimized" className="text-[10px]">Founder / Developer</Badge>
            </div>
            <p className="text-sm text-slate-500 mt-1">
              Farm: <span className="font-bold text-slate-700 dark:text-slate-300">{user?.farmName || 'Demo Hydro Farm'}</span> • Role: <span className="font-bold text-emerald-600">{user?.role || 'Creator of HydroGrow AI'}</span>
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <Button variant="outline" onClick={toggleTheme} icon={theme === 'dark' ? Sun : Moon}>
            {theme === 'dark' ? 'Light Mode' : 'Dark Mode'}
          </Button>
          <Button variant="primary" onClick={handleExportPDF} isLoading={downloading} icon={Download}>
            Download PDF Report
          </Button>
        </div>
      </div>

      {/* Grid: Settings & Theme Preferences */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        <Card header="Farm Credentials">
          <div className="space-y-4 text-sm">
            <div>
              <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Grower Name</label>
              <input
                type="text"
                value={user?.name || 'Karthikeya'}
                onChange={(e) => setUser({ ...user, name: e.target.value })}
                className="w-full px-3 py-2 text-sm rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Farm Name</label>
              <input
                type="text"
                value={user?.farmName || 'Demo Hydro Farm'}
                onChange={(e) => setUser({ ...user, farmName: e.target.value })}
                className="w-full px-3 py-2 text-sm rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Registered Email</label>
              <input
                type="email"
                readOnly
                value={user?.email || 'karthikeya@hydrogrow.ai'}
                className="w-full px-3 py-2 text-sm rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 text-slate-500"
              />
            </div>
          </div>
        </Card>

        <Card header="System Preferences & Theme">
          <div className="space-y-4 text-sm">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
              <div>
                <div className="font-bold text-slate-900 dark:text-white">Appearance Theme</div>
                <div className="text-xs text-slate-500">Switch between light & dark SaaS UI</div>
              </div>
              <Badge variant="neutral">{theme === 'dark' ? '🌙 Dark Mode' : '☀ Light Mode'}</Badge>
            </div>
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
              <div>
                <div className="font-bold text-slate-900 dark:text-white">Automatic Dosing Telemetry</div>
                <div className="text-xs text-slate-500">Real-time MQTT sensor connection</div>
              </div>
              <Badge variant="optimized">Active</Badge>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <div className="font-bold text-slate-900 dark:text-white">AI Diagnostic Engine</div>
                <div className="text-xs text-slate-500">v2.4 Neural Crop Model</div>
              </div>
              <Badge variant="brand">216 Cycles Model</Badge>
            </div>
          </div>
        </Card>

      </div>

      {/* Prediction History Table */}
      <Card header="Historical Crop Predictions & Diagnostic Reports">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 text-xs font-bold text-slate-500 uppercase tracking-wider">
                <th className="pb-3">Date</th>
                <th className="pb-3">Crop</th>
                <th className="pb-3">Yield Prediction</th>
                <th className="pb-3">Confidence</th>
                <th className="pb-3">Health</th>
                <th className="pb-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {mockHistory.map((item) => (
                <tr key={item.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/40 transition-colors">
                  <td className="py-3.5 font-medium text-slate-900 dark:text-slate-100">{item.date}</td>
                  <td className="py-3.5 font-bold text-emerald-600 dark:text-emerald-400">{item.crop}</td>
                  <td className="py-3.5 font-black text-slate-900 dark:text-white">{item.yieldGrams}</td>
                  <td className="py-3.5 text-slate-600 dark:text-slate-400">{item.confidence}</td>
                  <td className="py-3.5">
                    <Badge variant={item.health === 'Excellent' ? 'optimized' : 'attention'}>
                      {item.health}
                    </Badge>
                  </td>
                  <td className="py-3.5 text-right">
                    <Button variant="ghost" size="sm" onClick={handleExportPDF} icon={Download}>
                      PDF Report
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

    </div>
  );
}
