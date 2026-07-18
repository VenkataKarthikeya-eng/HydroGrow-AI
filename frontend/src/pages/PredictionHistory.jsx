import React, { useContext, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { AppContext } from '../context/AppContext';
import { History, Sparkles, Download, Search, ArrowLeft, RefreshCw, FileText } from 'lucide-react';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';

export default function PredictionHistory() {
  const { savedPredictions, setPredictionInputs } = useContext(AppContext);
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');

  const mockHistoryData = [
    { id: 101, label: 'Batch #214 - Vegetative Flush', date: 'July 18, 2026', crop: 'Butterhead Lettuce', yieldGrams: 382.7, confidence: '91%', status: 'Optimized', airTemp: 22.0, pH: 6.2, ec: 2.0 },
    { id: 102, label: 'Batch #213 - Canopy Expansion Run', date: 'July 11, 2026', crop: 'Butterhead Lettuce', yieldGrams: 365.4, confidence: '93%', status: 'Optimized', airTemp: 22.5, pH: 6.0, ec: 2.1 },
    { id: 103, label: 'Batch #212 - EC Tuning Trial', date: 'July 04, 2026', crop: 'Butterhead Lettuce', yieldGrams: 340.0, confidence: '89%', status: 'Optimized', airTemp: 21.5, pH: 6.1, ec: 2.2 },
  ];

  const allRecords = savedPredictions.length > 0 ? savedPredictions : mockHistoryData;

  const filteredRecords = allRecords.filter(r => 
    (r.label || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
    (r.crop || '').toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleReload = (record) => {
    if (record.inputs) {
      setPredictionInputs(record.inputs);
    }
    navigate('/prediction');
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in duration-300">
      
      {/* Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
            <History className="w-4 h-4" /> Diagnostic Logs
          </div>
          <h1 className="text-3xl font-black text-slate-900 dark:text-white mt-1">
            Prediction History & Reports
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Historical log of machine learning yield forecasts, parameter runs, and downloadable PDF reports.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm" onClick={handlePrint} icon={Download}>
            Print / Export PDF
          </Button>
          <Link to="/prediction">
            <Button variant="primary" size="sm" icon={Sparkles}>
              New Prediction
            </Button>
          </Link>
        </div>
      </div>

      {/* Main Table Card */}
      <Card padding="p-6 sm:p-8" header="Saved Run History">
        
        {/* Search & Filter Bar */}
        <div className="mb-6 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="relative w-full sm:w-80">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search batch or crop..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-4 py-2 text-sm rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-950 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-emerald-500 focus:outline-none"
            />
          </div>
          <div className="text-xs text-slate-500 font-medium">
            Showing {filteredRecords.length} historical run(s)
          </div>
        </div>

        {/* Records Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 text-xs font-bold text-slate-500 uppercase tracking-wider">
                <th className="pb-3">Batch Run Label</th>
                <th className="pb-3">Date</th>
                <th className="pb-3">Crop Type</th>
                <th className="pb-3">Forecast Yield</th>
                <th className="pb-3">Status</th>
                <th className="pb-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {filteredRecords.map((item, idx) => (
                <tr key={idx} className="hover:bg-slate-50 dark:hover:bg-slate-800/40 transition-colors">
                  <td className="py-4 font-bold text-slate-900 dark:text-white flex items-center gap-2">
                    <FileText className="w-4 h-4 text-emerald-600 shrink-0" />
                    <span>{item.label || item.crop || 'Batch Run'}</span>
                  </td>
                  <td className="py-4 text-slate-500">{item.timestamp || item.date}</td>
                  <td className="py-4 font-semibold text-emerald-600 dark:text-emerald-400">{item.crop || 'Butterhead Lettuce'}</td>
                  <td className="py-4 font-black text-slate-900 dark:text-white">
                    {typeof item.predicted_weight === 'number' ? `${item.predicted_weight.toFixed(1)}g` : item.yieldGrams || '382.7g'}
                  </td>
                  <td className="py-4">
                    <Badge variant={item.status === 'Optimized' ? 'optimized' : 'attention'}>
                      {item.status || 'Verified'}
                    </Badge>
                  </td>
                  <td className="py-4 text-right space-x-2">
                    <Button variant="ghost" size="sm" onClick={() => handleReload(item)} icon={RefreshCw}>
                      Reload Inputs
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
