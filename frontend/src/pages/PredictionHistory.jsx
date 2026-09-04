import React, { useContext, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { AppContext } from '../context/AppContext';
import { 
  History, Sparkles, Download, Search, RefreshCw, FileText, 
  Camera, Trash2, CheckCircle2, AlertTriangle, ArrowRight, ShieldCheck, Sprout, TestTube
} from 'lucide-react';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';

export default function PredictionHistory() {
  const { 
    savedPredictions, 
    plantDoctorScans, 
    deleteSavedPrediction, 
    deletePlantDoctorScan, 
    setPredictionInputs 
  } = useContext(AppContext);

  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('yield'); // 'yield' | 'plant-doctor'
  const [searchTerm, setSearchTerm] = useState('');

  // 1. Format Yield Predictions List
  const formattedYieldRecords = (savedPredictions || []).map((item, idx) => {
    const rawWeight = item.predicted_weight ?? item.yieldGrams ?? 382.7;
    const numWeight = typeof rawWeight === 'number' ? rawWeight : parseFloat(rawWeight) || 382.7;
    const rawConf = item.confidence_score ?? 0.91;
    const normConf = rawConf <= 1.0 ? rawConf * 100 : rawConf;

    return {
      id: item.id || `yield-${idx}`,
      label: item.label || `Batch #${idx + 215} - Lettuce Forecast`,
      date: item.timestamp || (item.created_at ? new Date(item.created_at).toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' }) : 'Today'),
      crop: item.crop || 'Butterhead Lettuce',
      yieldGrams: `${numWeight.toFixed(1)}g`,
      confidence: `${Math.round(normConf)}%`,
      growthCategory: item.growth_category || '🌟 Excellent',
      status: item.status || (item.growth_category && (item.growth_category.includes('Poor') || item.growth_category.includes('Attention')) ? 'Attention' : 'Optimized'),
      inputs: item.inputs || item.input_parameters || null
    };
  });

  // 2. Format Plant Doctor Scans List
  const formattedDoctorRecords = (plantDoctorScans || []).map((item, idx) => {
    const rawConf = item.confidence ?? 0.95;
    const normConf = rawConf <= 1.0 ? rawConf * 100 : rawConf;

    return {
      id: item.id || `scan-${idx}`,
      label: item.label || `Leaf Scan #${idx + 101} - ${item.condition || 'Healthy'}`,
      date: item.timestamp || (item.created_at ? new Date(item.created_at).toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' }) : 'Today'),
      crop: item.crop || 'Butterhead Lettuce',
      condition: item.condition || 'Healthy',
      stage: item.stage || 'Vegetative',
      growth_day: item.growth_day ?? 15,
      confidence: `${Math.round(normConf)}%`,
      status: item.status || (item.condition === 'Healthy' ? 'Optimized' : 'Attention'),
      recommendation: item.recommendation || 'Standard fertigation protocol recommended.'
    };
  });

  // Filtering
  const filteredYieldRecords = formattedYieldRecords.filter(r => 
    (r.label || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
    (r.crop || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
    (r.growthCategory || '').toLowerCase().includes(searchTerm.toLowerCase())
  );

  const filteredDoctorRecords = formattedDoctorRecords.filter(r => 
    (r.label || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
    (r.crop || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
    (r.condition || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
    (r.stage || '').toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleReloadYieldInputs = (record) => {
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
      
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
            <History className="w-4 h-4" /> Comprehensive Scan History
          </div>
          <h1 className="text-3xl font-black text-slate-900 dark:text-white mt-1">
            Scan History & Harvest Logs
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Recorded history of ML harvest yield forecasts, leaf pathology scans, and cultivation reports.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm" onClick={handlePrint} icon={Download}>
            Print / Export PDF
          </Button>
          {activeTab === 'yield' ? (
            <Link to="/prediction">
              <Button variant="primary" size="sm" icon={Sparkles}>
                New Yield Forecast
              </Button>
            </Link>
          ) : (
            <Link to="/plant-doctor">
              <Button variant="primary" size="sm" icon={Camera}>
                Scan New Leaf
              </Button>
            </Link>
          )}
        </div>
      </div>

      {/* Tab Selector Bar */}
      <div className="flex items-center gap-3 border-b border-slate-200 dark:border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab('yield')}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold transition-all ${
            activeTab === 'yield'
              ? 'bg-emerald-600 text-white shadow-sm'
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800'
          }`}
        >
          <Sparkles className="w-4 h-4" />
          <span>Yield Predictions</span>
          <span className={`text-xs px-2 py-0.5 rounded-full font-bold ${
            activeTab === 'yield' ? 'bg-white/20 text-white' : 'bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300'
          }`}>
            {formattedYieldRecords.length}
          </span>
        </button>

        <button
          onClick={() => setActiveTab('plant-doctor')}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold transition-all ${
            activeTab === 'plant-doctor'
              ? 'bg-emerald-600 text-white shadow-sm'
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800'
          }`}
        >
          <Camera className="w-4 h-4" />
          <span>Plant Doctor Scans</span>
          <span className={`text-xs px-2 py-0.5 rounded-full font-bold ${
            activeTab === 'plant-doctor' ? 'bg-white/20 text-white' : 'bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300'
          }`}>
            {formattedDoctorRecords.length}
          </span>
        </button>
      </div>

      {/* TAB 1: YIELD PREDICTIONS */}
      {activeTab === 'yield' && (
        <Card padding="p-6 sm:p-8" header="Saved Yield Prediction Runs">
          
          {/* Search & Filter */}
          <div className="mb-6 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="relative w-full sm:w-80">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Search yield runs or crop..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-9 pr-4 py-2 text-sm rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-950 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>
            <div className="text-xs text-slate-500 font-medium">
              Showing {filteredYieldRecords.length} recorded prediction(s)
            </div>
          </div>

          {/* Records Table */}
          {filteredYieldRecords.length === 0 ? (
            <div className="py-12 text-center text-slate-500 space-y-3">
              <Sparkles className="w-8 h-8 text-slate-400 mx-auto" />
              <p className="text-sm font-medium">No saved yield predictions match your criteria.</p>
              <Link to="/prediction">
                <Button variant="outline" size="sm">
                  Run a Yield Prediction Now
                </Button>
              </Link>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="border-b border-slate-200 dark:border-slate-800 text-xs font-bold text-slate-500 uppercase tracking-wider">
                    <th className="pb-3">Batch Run Label</th>
                    <th className="pb-3">Date</th>
                    <th className="pb-3">Crop Type</th>
                    <th className="pb-3">Forecast Yield</th>
                    <th className="pb-3">Confidence</th>
                    <th className="pb-3">Status</th>
                    <th className="pb-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                  {filteredYieldRecords.map((item) => (
                    <tr key={item.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/40 transition-colors">
                      <td className="py-4 font-bold text-slate-900 dark:text-white flex items-center gap-2">
                        <FileText className="w-4 h-4 text-emerald-600 shrink-0" />
                        <div>
                          <div>{item.label}</div>
                          {item.inputs && (
                            <div className="text-[11px] font-normal text-slate-500 dark:text-slate-400">
                              Temp: {item.inputs.air_temperature}°C | pH: {item.inputs.water_ph} | EC: {item.inputs.water_ec} mS/cm
                            </div>
                          )}
                        </div>
                      </td>
                      <td className="py-4 text-slate-500 whitespace-nowrap">{item.date}</td>
                      <td className="py-4 font-semibold text-emerald-600 dark:text-emerald-400 whitespace-nowrap">{item.crop}</td>
                      <td className="py-4 font-black text-slate-900 dark:text-white whitespace-nowrap">
                        {item.yieldGrams} <span className="text-xs font-normal text-slate-500">/ plant</span>
                      </td>
                      <td className="py-4 font-bold text-slate-700 dark:text-slate-300">{item.confidence}</td>
                      <td className="py-4">
                        <Badge variant={item.status === 'Optimized' ? 'optimized' : 'attention'}>
                          {item.status}
                        </Badge>
                      </td>
                      <td className="py-4 text-right whitespace-nowrap space-x-2">
                        <Button variant="ghost" size="sm" onClick={() => handleReloadYieldInputs(item)} icon={RefreshCw}>
                          Reload Inputs
                        </Button>
                        <button
                          onClick={() => deleteSavedPrediction(item.id)}
                          title="Delete record"
                          aria-label={`Delete batch ${item.label}`}
                          className="p-1.5 rounded-lg text-slate-400 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-950/50 transition-colors"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

        </Card>
      )}

      {/* TAB 2: PLANT DOCTOR SCANS */}
      {activeTab === 'plant-doctor' && (
        <Card padding="p-6 sm:p-8" header="Saved Plant Doctor Leaf Scans">
          
          {/* Search & Filter */}
          <div className="mb-6 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="relative w-full sm:w-80">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Search leaf diagnosis or status..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-9 pr-4 py-2 text-sm rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-950 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>
            <div className="text-xs text-slate-500 font-medium">
              Showing {filteredDoctorRecords.length} leaf scan(s)
            </div>
          </div>

          {/* Records Table */}
          {filteredDoctorRecords.length === 0 ? (
            <div className="py-12 text-center text-slate-500 space-y-3">
              <Camera className="w-8 h-8 text-slate-400 mx-auto" />
              <p className="text-sm font-medium">No saved plant doctor scans match your criteria.</p>
              <Link to="/plant-doctor">
                <Button variant="outline" size="sm">
                  Scan a Leaf Now
                </Button>
              </Link>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="border-b border-slate-200 dark:border-slate-800 text-xs font-bold text-slate-500 uppercase tracking-wider">
                    <th className="pb-3">Scan Label</th>
                    <th className="pb-3">Date</th>
                    <th className="pb-3">Nutrient Status</th>
                    <th className="pb-3">Growth Stage</th>
                    <th className="pb-3">Confidence</th>
                    <th className="pb-3">Status</th>
                    <th className="pb-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                  {filteredDoctorRecords.map((item) => (
                    <tr key={item.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/40 transition-colors">
                      <td className="py-4 font-bold text-slate-900 dark:text-white flex items-center gap-2">
                        <Camera className="w-4 h-4 text-emerald-600 shrink-0" />
                        <div>
                          <div>{item.label}</div>
                          <div className="text-[11px] font-normal text-slate-500 dark:text-slate-400 max-w-sm truncate">
                            {item.recommendation}
                          </div>
                        </div>
                      </td>
                      <td className="py-4 text-slate-500 whitespace-nowrap">{item.date}</td>
                      <td className="py-4 font-bold text-slate-900 dark:text-white whitespace-nowrap">
                        {item.condition}
                      </td>
                      <td className="py-4 font-semibold text-emerald-600 dark:text-emerald-400 whitespace-nowrap">
                        {item.stage} (Day {item.growth_day})
                      </td>
                      <td className="py-4 font-bold text-slate-700 dark:text-slate-300">{item.confidence}</td>
                      <td className="py-4">
                        <Badge variant={item.status === 'Optimized' ? 'optimized' : 'attention'}>
                          {item.status}
                        </Badge>
                      </td>
                      <td className="py-4 text-right whitespace-nowrap space-x-2">
                        <Link to="/plant-doctor">
                          <Button variant="ghost" size="sm" icon={Camera}>
                            Scan Leaf
                          </Button>
                        </Link>
                        <button
                          onClick={() => deletePlantDoctorScan(item.id)}
                          title="Delete scan"
                          aria-label={`Delete scan ${item.label}`}
                          className="p-1.5 rounded-lg text-slate-400 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-950/50 transition-colors"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

        </Card>
      )}

    </div>
  );
}
