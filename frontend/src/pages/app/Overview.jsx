import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Sprout, Sparkles, Camera, ArrowRight, 
  History, FileText, ChevronRight
} from 'lucide-react';
import { AppContext } from '../../context/AppContext';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Badge from '../../components/ui/Badge';

export default function Overview() {
  const { user } = useContext(AppContext);
  const navigate = useNavigate();

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-300 py-2">
      
      {/* Top Greeting Header */}
      <div className="space-y-1 border-b border-slate-200 dark:border-slate-800 pb-6">
        <h1 className="text-3xl sm:text-4xl font-black text-slate-900 dark:text-white tracking-tight flex items-center gap-2">
          Welcome back{user?.name ? `, ${user.name}` : ''}! <span className="inline-block">👋</span>
        </h1>
        <p className="text-base text-slate-600 dark:text-slate-400 font-medium">
          Hydroponic lettuce leaf diagnostics and harvest yield predictions.
        </p>
      </div>

      {/* Main 2-Column Dashboard Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left Column: Primary Tools Quick Links */}
        <div className="lg:col-span-5 space-y-4">
          <h2 className="text-lg font-black text-slate-900 dark:text-white tracking-tight flex items-center gap-2">
            <FileText className="w-5 h-5 text-emerald-600" />
            Product Tools
          </h2>

          <div className="space-y-3">
            
            {/* Tool 1: Plant Doctor */}
            <div
              onClick={() => navigate('/plant-doctor')}
              className="saas-card p-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl hover:border-emerald-500 hover:shadow-lg transition-all cursor-pointer group flex items-start justify-between gap-3"
            >
              <div className="flex items-start gap-3">
                <div className="p-2.5 rounded-xl bg-emerald-50 dark:bg-emerald-950 text-emerald-600 shrink-0 mt-0.5">
                  <Camera className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900 dark:text-white group-hover:text-emerald-600 transition-colors">
                    Plant Doctor Leaf Scanner
                  </h3>
                  <p className="text-xs text-slate-500 mt-1">Diagnose growth stage, day, and nutrient health from leaf photos</p>
                </div>
              </div>
              <ChevronRight className="w-5 h-5 text-slate-400 group-hover:text-emerald-600 group-hover:translate-x-1 transition-all shrink-0 mt-1" />
            </div>

            {/* Tool 2: Yield Predictor */}
            <div
              onClick={() => navigate('/prediction')}
              className="saas-card p-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl hover:border-emerald-500 hover:shadow-lg transition-all cursor-pointer group flex items-start justify-between gap-3"
            >
              <div className="flex items-start gap-3">
                <div className="p-2.5 rounded-xl bg-teal-50 dark:bg-teal-950 text-teal-600 shrink-0 mt-0.5">
                  <Sparkles className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900 dark:text-white group-hover:text-emerald-600 transition-colors">
                    Yield Predictor
                  </h3>
                  <p className="text-xs text-slate-500 mt-1">Forecast fresh weight yield based on hydroponic environment telemetry</p>
                </div>
              </div>
              <ChevronRight className="w-5 h-5 text-slate-400 group-hover:text-emerald-600 group-hover:translate-x-1 transition-all shrink-0 mt-1" />
            </div>

            {/* Tool 3: Scan History */}
            <div
              onClick={() => navigate('/history/predictions')}
              className="saas-card p-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl hover:border-emerald-500 hover:shadow-lg transition-all cursor-pointer group flex items-start justify-between gap-3"
            >
              <div className="flex items-start gap-3">
                <div className="p-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 shrink-0 mt-0.5">
                  <History className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900 dark:text-white group-hover:text-emerald-600 transition-colors">
                    Scan History
                  </h3>
                  <p className="text-xs text-slate-500 mt-1">Review past leaf diagnosis scans and recorded predictions</p>
                </div>
              </div>
              <ChevronRight className="w-5 h-5 text-slate-400 group-hover:text-emerald-600 group-hover:translate-x-1 transition-all shrink-0 mt-1" />
            </div>

          </div>

          {/* Supported Crop Widget */}
          <div className="saas-card p-5 bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-2xl space-y-3">
            <div className="flex items-center justify-between text-xs">
              <span className="font-bold text-slate-700 dark:text-slate-300">Model Focus</span>
              <Badge variant="optimized">Hydroponic Lettuce</Badge>
            </div>
            <div className="text-sm font-bold text-slate-900 dark:text-white">
              Butterhead Lettuce (Lactuca sativa)
            </div>
            <p className="text-xs text-slate-500 leading-relaxed">
              Models are trained on hydroponic lettuce datasets for growth stage tracking, deficiency diagnosis, and yield estimation.
            </p>
          </div>
        </div>

        {/* Right Column: Featured Cards */}
        <div className="lg:col-span-7 space-y-6">
          
          {/* Card 1: Plant Doctor Hero */}
          <Card padding="p-8" className="bg-gradient-to-br from-emerald-700 via-teal-700 to-slate-900 text-white rounded-3xl shadow-lg border-none">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="px-3 py-1 rounded-full bg-white/20 backdrop-blur-md text-xs font-bold uppercase tracking-wider text-white">
                  Pathology Scanner
                </span>
                <Badge variant="brand" className="bg-white text-slate-900 font-bold border-none">
                  Leaf Scanner
                </Badge>
              </div>

              <div className="space-y-2">
                <h3 className="text-2xl sm:text-3xl font-black tracking-tight">Plant Doctor</h3>
                <p className="text-sm text-emerald-100 leading-relaxed max-w-lg">
                  Upload a photo of a single hydroponic lettuce leaf to get an instant diagnosis of growth stage, growth day, and nutrient deficiencies.
                </p>
              </div>

              <div className="pt-2">
                <Link to="/plant-doctor">
                  <Button variant="secondary" size="md" icon={ArrowRight} className="bg-white text-slate-900 hover:bg-emerald-50">
                    Scan Leaf Now
                  </Button>
                </Link>
              </div>
            </div>
          </Card>

          {/* Card 2: Yield Predictor Hero */}
          <Card padding="p-8" className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">
                Harvest Forecast
              </span>
              <Badge variant="optimized">Tabular Model</Badge>
            </div>

            <div className="space-y-2">
              <h3 className="text-2xl font-black text-slate-900 dark:text-white">Yield Predictor</h3>
              <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
                Input your system's temperature, pH, EC, and lighting parameters to forecast fresh weight yield in grams per plant.
              </p>
            </div>

            <div>
              <Link to="/prediction">
                <Button variant="primary" size="md" icon={ArrowRight}>
                  Calculate Yield
                </Button>
              </Link>
            </div>
          </Card>

        </div>

      </div>

    </div>
  );
}
