import React, { useState } from 'react';
import { Cpu, Sliders, TrendingUp, RefreshCw, Zap, CheckCircle2, Sparkles, HelpCircle, Info } from 'lucide-react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Badge from '../../components/ui/Badge';
import ChartContainer from '../../components/ui/ChartContainer';

export default function SimulationLab() {
  // Retained simulation state & formulas
  const [temp, setTemp] = useState(22.5);
  const [humidity, setHumidity] = useState(65);
  const [ec, setEc] = useState(2.0);
  const [ph, setPh] = useState(6.0);

  const tempDiff = Math.abs(temp - 22.0);
  const ecDiff = Math.abs(ec - 2.2);
  const phDiff = Math.abs(ph - 6.2);
  
  const yieldGain = Math.max(0, Math.round(22 - (tempDiff * 2 + ecDiff * 5 + phDiff * 4)));

  const baselineCurve = [15, 25, 45, 70, 110, 160, 220, 290, 380];

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-300">
      
      {/* Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
            <Cpu className="w-4 h-4" /> Digital Twin Crop Simulator
          </div>
          <h1 className="text-3xl font-black text-slate-900 dark:text-white mt-1">
            Crop Simulation Lab
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Simulate climate variations and fertigation dosing adjustments on digital twin models to project growth curves safely.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Badge variant="brand" className="px-3 py-1.5 text-xs">
            Digital Twin Model v3.1
          </Badge>
        </div>
      </div>

      {/* Main 2-Column Grid Layout (Spacious & Compact) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left Column: Simulator Sliders (4 cols) */}
        <div className="lg:col-span-4 space-y-6">
          
          <Card padding="p-6 sm:p-8" header="Simulation Parameters" subtitle="Adjust virtual greenhouse variables">
            <div className="space-y-6">
              
              {/* Temperature Slider */}
              <div>
                <div className="flex justify-between items-center text-xs font-bold mb-2">
                  <span className="text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                    🌡️ Air Temp (°C)
                  </span>
                  <span className="text-emerald-600 dark:text-emerald-400 font-extrabold text-sm">{temp}°C</span>
                </div>
                <input
                  type="range"
                  min="16"
                  max="32"
                  step="0.5"
                  value={temp}
                  onChange={(e) => setTemp(parseFloat(e.target.value))}
                  className="w-full accent-emerald-600 cursor-pointer"
                />
                <div className="flex justify-between text-[10px] text-slate-400 mt-1 font-medium">
                  <span>16°C (Cool)</span>
                  <span>22°C (Optimal)</span>
                  <span>32°C (Hot)</span>
                </div>
              </div>

              {/* Humidity Slider */}
              <div>
                <div className="flex justify-between items-center text-xs font-bold mb-2">
                  <span className="text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                    💧 Relative Humidity (%)
                  </span>
                  <span className="text-emerald-600 dark:text-emerald-400 font-extrabold text-sm">{humidity}%</span>
                </div>
                <input
                  type="range"
                  min="40"
                  max="90"
                  step="1"
                  value={humidity}
                  onChange={(e) => setHumidity(parseInt(e.target.value))}
                  className="w-full accent-emerald-600 cursor-pointer"
                />
                <div className="flex justify-between text-[10px] text-slate-400 mt-1 font-medium">
                  <span>40% (Dry)</span>
                  <span>65% (Optimal)</span>
                  <span>90% (Humid)</span>
                </div>
              </div>

              {/* EC Slider */}
              <div>
                <div className="flex justify-between items-center text-xs font-bold mb-2">
                  <span className="text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                    ⚡ Nutrient EC (mS/cm)
                  </span>
                  <span className="text-emerald-600 dark:text-emerald-400 font-extrabold text-sm">{ec}</span>
                </div>
                <input
                  type="range"
                  min="1.0"
                  max="3.2"
                  step="0.1"
                  value={ec}
                  onChange={(e) => setEc(parseFloat(e.target.value))}
                  className="w-full accent-emerald-600 cursor-pointer"
                />
                <div className="flex justify-between text-[10px] text-slate-400 mt-1 font-medium">
                  <span>1.0 (Low)</span>
                  <span>2.2 (Optimal)</span>
                  <span>3.2 (High)</span>
                </div>
              </div>

              {/* pH Slider */}
              <div>
                <div className="flex justify-between items-center text-xs font-bold mb-2">
                  <span className="text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                    🧪 Solution pH
                  </span>
                  <span className="text-emerald-600 dark:text-emerald-400 font-extrabold text-sm">{ph}</span>
                </div>
                <input
                  type="range"
                  min="5.0"
                  max="7.5"
                  step="0.1"
                  value={ph}
                  onChange={(e) => setPh(parseFloat(e.target.value))}
                  className="w-full accent-emerald-600 cursor-pointer"
                />
                <div className="flex justify-between text-[10px] text-slate-400 mt-1 font-medium">
                  <span>5.0 (Acidic)</span>
                  <span>6.2 (Optimal)</span>
                  <span>7.5 (Alkaline)</span>
                </div>
              </div>

              {/* Preset Buttons */}
              <div className="pt-2 space-y-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => { setTemp(22.0); setHumidity(65); setEc(2.2); setPh(6.2); }}
                  icon={RefreshCw}
                  className="w-full justify-center"
                >
                  Reset Optimal Baseline
                </Button>
              </div>

            </div>
          </Card>

        </div>

        {/* Right Column: High-Impact Output + Growth Chart + AI Insights (8 cols) */}
        <div className="lg:col-span-8 space-y-6">
          
          {/* Yield Gain Header Card */}
          <div className="saas-card p-6 sm:p-8 bg-gradient-to-r from-emerald-600 via-teal-600 to-slate-900 text-white rounded-2xl shadow-xl flex items-center justify-between gap-6">
            <div>
              <div className="text-xs uppercase font-bold text-emerald-100 tracking-wider flex items-center gap-1.5">
                <Sparkles className="w-4 h-4 text-amber-300" /> Projected Yield Improvement
              </div>
              <div className="text-4xl sm:text-5xl font-black mt-1 tracking-tight">
                +{yieldGain}% <span className="text-xl font-semibold text-emerald-200">Yield Increase</span>
              </div>
              <p className="text-xs text-emerald-100 mt-1">
                Estimated harvest weight boost compared to standard unoptimized hydroponic cycles.
              </p>
            </div>
            
            <div className="hidden sm:flex p-4 bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 items-center justify-center shrink-0">
              <Zap className="w-10 h-10 text-amber-300" />
            </div>
          </div>

          {/* High Visibility 30-Day Growth Curve Chart Container */}
          <Card padding="p-6 sm:p-8" header="Projected 30-Day Crop Growth Curve" subtitle="Baseline vs Simulated Environmental Trajectory">
            
            <div className="h-64 flex items-end justify-between gap-2.5 pt-10 pb-4 px-2 border-b border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/40 rounded-xl">
              {baselineCurve.map((baseVal, idx) => {
                const simulatedVal = Math.round(baseVal * (1 + yieldGain / 100));
                const baseHeightPercent = Math.min(100, Math.round((baseVal / 450) * 100));
                const simHeightPercent = Math.min(100, Math.round((simulatedVal / 450) * 100));
                
                return (
                  <div key={idx} className="flex-1 flex flex-col items-center gap-1.5 group relative h-full justify-end">
                    
                    {/* Tooltip Hover Value */}
                    <div className="text-[11px] font-extrabold text-emerald-600 dark:text-emerald-400 opacity-90 group-hover:scale-110 transition-all">
                      {simulatedVal}g
                    </div>

                    {/* Dual Bars: Baseline vs Simulated */}
                    <div className="w-full flex items-end justify-center gap-1 h-full">
                      {/* Baseline Bar */}
                      <div
                        style={{ height: `${baseHeightPercent}%` }}
                        className="w-1.5 sm:w-2 bg-slate-300 dark:bg-slate-700 rounded-t-sm"
                        title={`Baseline: ${baseVal}g`}
                      />
                      {/* Simulated Bar */}
                      <div
                        style={{ height: `${simHeightPercent}%` }}
                        className="w-3 sm:w-4 bg-gradient-to-t from-emerald-600 to-teal-400 rounded-t-md transition-all duration-300 shadow-xs group-hover:from-emerald-500 group-hover:to-teal-300"
                        title={`Simulated: ${simulatedVal}g`}
                      />
                    </div>

                    <span className="text-[10px] font-bold text-slate-500 dark:text-slate-400 mt-1">
                      Day {(idx + 1) * 3}
                    </span>
                  </div>
                );
              })}
            </div>

            {/* Legend & Stats Footer */}
            <div className="flex flex-wrap items-center justify-between gap-4 text-xs text-slate-600 dark:text-slate-400 mt-4 pt-2">
              <div className="flex items-center gap-4">
                <span className="flex items-center gap-1.5 font-medium">
                  <span className="w-3 h-3 bg-emerald-600 rounded-sm" /> Simulated Trajectory ({Math.round(380 * (1 + yieldGain / 100))}g)
                </span>
                <span className="flex items-center gap-1.5 font-medium">
                  <span className="w-3 h-3 bg-slate-300 dark:bg-slate-700 rounded-sm" /> Baseline (380g)
                </span>
              </div>
              <span className="font-bold text-slate-900 dark:text-white">
                Peak Harvest Window: Day 27
              </span>
            </div>
          </Card>

          {/* AI Simulation Insights Section (Explaining Why Yield Improved) */}
          <Card padding="p-6 sm:p-8" header="AI Simulation Insights & Biological Drivers">
            <div className="space-y-4 text-sm">
              
              <div className="p-4 rounded-xl border border-emerald-100 dark:border-emerald-950 bg-emerald-50/50 dark:bg-emerald-950/20 flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
                <div>
                  <div className="font-bold text-slate-900 dark:text-white">Air Temperature Optimization (22.5°C)</div>
                  <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5 leading-relaxed">
                    Maintaining root zone temperature near 22.0°C minimizes respiration loss during canopy expansion, boosting net photosynthate accumulation.
                  </p>
                </div>
              </div>

              <div className="p-4 rounded-xl border border-emerald-100 dark:border-emerald-950 bg-emerald-50/50 dark:bg-emerald-950/20 flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
                <div>
                  <div className="font-bold text-slate-900 dark:text-white">Water Solution pH Balance (6.0)</div>
                  <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5 leading-relaxed">
                    A pH of 6.0 maximizes bioavailability of essential macro-nutrients (Nitrogen & Phosphorus) and Iron solubility, eliminating root tip chlorosis.
                  </p>
                </div>
              </div>

              <div className="p-4 rounded-xl border border-emerald-100 dark:border-emerald-950 bg-emerald-50/50 dark:bg-emerald-950/20 flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
                <div>
                  <div className="font-bold text-slate-900 dark:text-white">Nutrient Concentration (EC 2.0 mS/cm)</div>
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5 leading-relaxed">
                    Electrical Conductivity of 2.0 mS/cm provides optimal osmotic pressure for rapid vegetative leaf flushing without inducing tip-burn.
                  </p>
                </div>
              </div>

            </div>
          </Card>

        </div>

      </div>

    </div>
  );
}
