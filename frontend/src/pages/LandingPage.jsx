import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { 
  Sprout, Bot, ArrowRight, CheckCircle2, Sparkles, Cpu, Activity, 
  ShieldCheck, BarChart3, Sliders, Zap, Award, ChevronRight
} from 'lucide-react';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';
import Badge from '../components/ui/Badge';

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="bg-white dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors">
      
      {/* SaaS Hero Section */}
      <section className="py-20 sm:py-28 px-4 max-w-7xl mx-auto">
        <div className="text-center max-w-4xl mx-auto space-y-8">
          
          {/* Top Pill Announcement */}
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-emerald-50 dark:bg-emerald-950/80 border border-emerald-200 dark:border-emerald-800 text-emerald-800 dark:text-emerald-300 text-xs font-bold uppercase tracking-wider shadow-2xs">
            <Sparkles className="h-4 w-4 text-emerald-600 dark:text-emerald-400" />
            Next-Generation Hydroponic Agritech AI
          </div>

          {/* Main Headline */}
          <h1 className="text-4xl sm:text-6xl md:text-7xl font-black tracking-tight leading-[1.08] text-slate-900 dark:text-white">
            Harvest Higher Yields with <br />
            <span className="bg-gradient-to-r from-emerald-600 via-teal-600 to-emerald-500 bg-clip-text text-transparent">
              Precision Agritech AI
            </span>
          </h1>

          {/* Subtitle */}
          <p className="text-lg sm:text-xl font-normal text-slate-600 dark:text-slate-400 max-w-3xl mx-auto leading-relaxed">
            HydroGrow AI empowers commercial hydroponic farms and growers to accurately predict crop yields, diagnose plant health in real time, and optimize water and nutrient fertigation.
          </p>

          {/* Feature Bullet Strip */}
          <div className="flex flex-wrap items-center justify-center gap-x-8 gap-y-3 text-sm font-semibold text-slate-700 dark:text-slate-300 pt-2">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0" />
              <span>3-Step ML Yield Wizard</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0" />
              <span>Computer Vision Leaf Scanner</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0" />
              <span>Digital Twin Simulator</span>
            </div>
          </div>

          {/* Action CTAs */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
            <Button variant="primary" size="lg" onClick={() => navigate('/prediction')} icon={Sparkles} className="w-full sm:w-auto shadow-md">
              Start Free Yield Prediction
            </Button>
            <Button variant="outline" size="lg" onClick={() => navigate('/dashboard')} icon={ArrowRight} className="w-full sm:w-auto">
              Explore Live Platform
            </Button>
          </div>

        </div>

        {/* Live Interactive Product Preview Mockup */}
        <div className="mt-16 max-w-5xl mx-auto saas-card p-6 sm:p-8 bg-slate-900 text-white rounded-3xl shadow-2xl border border-slate-800 relative overflow-hidden">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-red-500 inline-block" />
              <span className="w-3 h-3 rounded-full bg-amber-500 inline-block" />
              <span className="w-3 h-3 rounded-full bg-emerald-500 inline-block" />
              <span className="text-xs font-mono text-slate-400 ml-2">app.hydrogrow.ai/dashboard</span>
            </div>
            <Badge variant="brand">Live Telemetry Active</Badge>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
            <div className="bg-slate-950 p-5 rounded-2xl border border-slate-800">
              <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">Target Crop</div>
              <div className="text-2xl font-black text-white mt-1">Butterhead Lettuce</div>
              <div className="text-xs text-emerald-400 font-semibold mt-2">Vegetative Flush • Day 18</div>
            </div>

            <div className="bg-slate-950 p-5 rounded-2xl border border-slate-800">
              <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">AI Yield Forecast</div>
              <div className="text-2xl font-black text-emerald-400 mt-1">382.7g / plant</div>
              <div className="text-xs text-slate-400 font-semibold mt-2">91% Model Confidence</div>
            </div>

            <div className="bg-slate-950 p-5 rounded-2xl border border-slate-800">
              <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">Plant Doctor Status</div>
              <div className="text-2xl font-black text-white mt-1">99% Health Index</div>
              <div className="text-xs text-emerald-400 font-semibold mt-2">Zero Pathogens Detected</div>
            </div>
          </div>
        </div>

        {/* Commercial Trust & Statistics Bar */}
        <div className="mt-20 pt-12 border-t border-slate-200 dark:border-slate-800 text-center">
          <p className="text-xs font-bold uppercase tracking-widest text-slate-400 mb-8">
            Engineered for Commercial Hydroponic Excellence
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto">
            <div>
              <div className="text-3xl sm:text-4xl font-black text-slate-900 dark:text-white">99.4%</div>
              <div className="text-xs text-slate-500 dark:text-slate-400 font-semibold mt-1">Model Accuracy Score</div>
            </div>
            <div>
              <div className="text-3xl sm:text-4xl font-black text-emerald-600 dark:text-emerald-400">216+</div>
              <div className="text-xs text-slate-500 dark:text-slate-400 font-semibold mt-1">Growth Cycles Trained</div>
            </div>
            <div>
              <div className="text-3xl sm:text-4xl font-black text-slate-900 dark:text-white">90%</div>
              <div className="text-xs text-slate-500 dark:text-slate-400 font-semibold mt-1">Water Saved vs Soil</div>
            </div>
            <div>
              <div className="text-3xl sm:text-4xl font-black text-emerald-600 dark:text-emerald-400">+18%</div>
              <div className="text-xs text-slate-500 dark:text-slate-400 font-semibold mt-1">Average Yield Increase</div>
            </div>
          </div>
        </div>

      </section>

      {/* Commercial Feature Pillars */}
      <section className="py-20 bg-slate-50 dark:bg-slate-900/50 border-t border-slate-200 dark:border-slate-800">
        <div className="max-w-7xl mx-auto px-4 space-y-12">
          
          <div className="text-center max-w-3xl mx-auto space-y-3">
            <h2 className="text-3xl sm:text-4xl font-black text-slate-900 dark:text-white tracking-tight">
              An End-to-End Agritech Platform Built for Scale
            </h2>
            <p className="text-base text-slate-600 dark:text-slate-400">
              Transform your commercial farm operations with dynamic predictions, pathology scanning, and automated dosing intelligence.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            
            <Card className="hover:border-emerald-500 transition-all" padding="p-8 sm:p-10" header="AI Yield Prediction Wizard">
              <p className="text-sm text-slate-600 dark:text-slate-400 mb-6 leading-relaxed">
                Configure ambient temperature, humidity, pH, and EC parameters to forecast harvest weight with precision confidence scores.
              </p>
              <Link to="/prediction" className="inline-flex items-center gap-1.5 text-sm font-bold text-emerald-600 hover:text-emerald-700 dark:text-emerald-400">
                Launch Yield Wizard <ChevronRight className="w-4 h-4" />
              </Link>
            </Card>

            <Card className="hover:border-emerald-500 transition-all" padding="p-8 sm:p-10" header="Computer Vision Plant Doctor">
              <p className="text-sm text-slate-600 dark:text-slate-400 mb-6 leading-relaxed">
                Upload leaf samples to diagnose early-stage pathogens, fungal mildew, and micro-nutrient deficiencies before crop stress spreads.
              </p>
              <Link to="/plant-doctor" className="inline-flex items-center gap-1.5 text-sm font-bold text-emerald-600 hover:text-emerald-700 dark:text-emerald-400">
                Scan Plant Leaf <ChevronRight className="w-4 h-4" />
              </Link>
            </Card>

            <Card className="hover:border-emerald-500 transition-all" padding="p-8 sm:p-10" header="Digital Twin Simulation Lab">
              <p className="text-sm text-slate-600 dark:text-slate-400 mb-6 leading-relaxed">
                Test virtual climate variations and nutrient dosing adjustments on digital twin models to optimize growth trajectories safely.
              </p>
              <Link to="/simulation-lab" className="inline-flex items-center gap-1.5 text-sm font-bold text-emerald-600 hover:text-emerald-700 dark:text-emerald-400">
                Open Crop Simulator <ChevronRight className="w-4 h-4" />
              </Link>
            </Card>

          </div>

        </div>
      </section>

      {/* Creator Attribution Section (Elegant & Startup Founder Credit) */}
      <section className="py-16 px-4 max-w-4xl mx-auto text-center border-t border-slate-200 dark:border-slate-800">
        <div className="saas-card p-8 sm:p-10 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl space-y-4 shadow-sm">
          <Badge variant="brand" className="text-xs font-bold px-3 py-1">
            Founder & Platform Creator
          </Badge>
          <h3 className="text-2xl font-black text-slate-900 dark:text-white tracking-tight">
            Created by Karthikeya Cherukuri
          </h3>
          <p className="text-sm text-slate-600 dark:text-slate-400 max-w-2xl mx-auto leading-relaxed">
            HydroGrow AI combines Machine Learning, Computer Vision, IoT Monitoring, and Digital Twin technology to build intelligent hydroponic farming solutions.
          </p>
        </div>
      </section>

    </div>
  );
}
