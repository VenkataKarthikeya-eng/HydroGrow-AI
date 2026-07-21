import React, { useState, useMemo, useEffect } from 'react';
import { Cpu, Sliders, TrendingUp, RefreshCw, Zap, CheckCircle2, AlertTriangle, Sparkles, HelpCircle, Info, Activity, Sprout, Calendar, ShieldCheck, Thermometer, Droplets, Gauge, TestTube, Save, History, Trash2, ArrowUpRight, Check, Loader2 } from 'lucide-react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Badge from '../../components/ui/Badge';
import ChartContainer from '../../components/ui/ChartContainer';
import { calculateGrowthSimulation } from '../../services/cropSimulationEngine';

export default function SimulationLab() {
  // Four simulation control states
  const [temp, setTemp] = useState(22.5);
  const [humidity, setHumidity] = useState(65);
  const [ec, setEc] = useState(2.0);
  const [ph, setPh] = useState(6.0);

  // Active day in 30-day cycle for Digital Twin status tracking
  const [currentDay, setCurrentDay] = useState(18);

  // Success notification feedback for save action
  const [saveToast, setSaveToast] = useState(false);

  // Loading animation trigger when recalculating parameters
  const [isCalculating, setIsCalculating] = useState(false);

  useEffect(() => {
    setIsCalculating(true);
    const timer = setTimeout(() => setIsCalculating(false), 200);
    return () => clearTimeout(timer);
  }, [temp, humidity, ec, ph]);

  // Simulation History state synchronized with localStorage
  const [history, setHistory] = useState(() => {
    try {
      const saved = localStorage.getItem('hydrogrow_simulation_history');
      if (saved) {
        return JSON.parse(saved);
      }
    } catch (e) {
      console.error('Error reading history from localStorage', e);
    }
    // Default seeded initial simulation runs
    return [
      {
        id: 'seed-1',
        date: 'Jul 21, 09:30 AM',
        temp: 22.0,
        humidity: 65,
        ec: 2.2,
        ph: 6.2,
        yieldWeight: 380,
        yieldGainPercent: 0,
        harvestDay: 28,
        healthScore: 100
      },
      {
        id: 'seed-2',
        date: 'Jul 20, 04:15 PM',
        temp: 18.5,
        humidity: 55,
        ec: 1.6,
        ph: 5.6,
        yieldWeight: 285,
        yieldGainPercent: -25,
        harvestDay: 35,
        healthScore: 78
      }
    ];
  });

  // Sync history state changes to localStorage
  useEffect(() => {
    try {
      localStorage.setItem('hydrogrow_simulation_history', JSON.stringify(history));
    } catch (e) {
      console.error('Error writing history to localStorage', e);
    }
  }, [history]);

  // Dynamic Digital Twin simulation calculation triggered whenever any slider changes
  const simResult = useMemo(() => {
    return calculateGrowthSimulation({
      temperature: temp,
      humidity,
      ec,
      ph
    });
  }, [temp, humidity, ec, ph]);

  // Baseline simulation (optimal baseline)
  const baselineResult = useMemo(() => {
    return calculateGrowthSimulation({
      temperature: 22.0,
      humidity: 65,
      ec: 2.2,
      ph: 6.2
    });
  }, []);

  const { growthCurve, yield: yieldData, harvestDay, healthScore, recommendations, factors } = simResult;
  const yieldGainPercent = yieldData.yieldGainPercent;

  // Growth stage definitions
  const stages = [
    { id: 'seedling', name: 'Seedling', range: 'Day 1-7', start: 1, end: 7 },
    { id: 'vegetative', name: 'Vegetative', range: 'Day 8-20', start: 8, end: 20 },
    { id: 'maturity', name: 'Maturity', range: 'Day 21-27', start: 21, end: 27 },
    { id: 'harvest', name: 'Harvest', range: 'Day 28-30', start: 28, end: 30 }
  ];

  // Current stage calculated dynamically
  const currentStage = useMemo(() => {
    return stages.find(s => currentDay >= s.start && currentDay <= s.end) || stages[1];
  }, [currentDay]);

  // Engine factor values formatted as percentages
  const factorPercentages = useMemo(() => {
    return {
      temperature: Math.round((factors?.temperatureFactor ?? 1) * 100),
      humidity: Math.round((factors?.humidityFactor ?? 1) * 100),
      nutrients: Math.round((factors?.ecFactor ?? 1) * 100),
      ph: Math.round((factors?.phFactor ?? 1) * 100)
    };
  }, [factors]);

  // Days sampled for graph visualization
  const chartDays = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30];

  // Dynamic maximum scale for bar heights
  const maxWeight = Math.max(
    400,
    ...simResult.growthCurve.map(p => p.weight),
    ...baselineResult.growthCurve.map(p => p.weight)
  );

  // Save current simulation parameters to history
  const handleSaveSimulation = () => {
    const newRun = {
      id: Date.now().toString(),
      date: new Date().toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }),
      temp,
      humidity,
      ec,
      ph,
      yieldWeight: yieldData.expectedWeight,
      yieldGainPercent: yieldData.yieldGainPercent,
      harvestDay,
      healthScore
    };

    setHistory(prev => [newRun, ...prev.slice(0, 19)]);
    setSaveToast(true);
    setTimeout(() => setSaveToast(false), 2500);
  };

  // Restore saved simulation parameters
  const handleLoadSimulation = (run) => {
    setTemp(run.temp);
    setHumidity(run.humidity);
    setEc(run.ec);
    setPh(run.ph);
  };

  // Delete a simulation run from history
  const handleDeleteHistoryItem = (id) => {
    setHistory(prev => prev.filter(item => item.id !== id));
  };

  // Clear all history entries
  const handleClearHistory = () => {
    setHistory([]);
  };

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-300">
      
      {/* Title & Header */}
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

        <div className="flex items-center gap-2 flex-wrap">
          {isCalculating ? (
            <Badge variant="outline" className="px-3 py-1.5 text-xs font-bold border-amber-500 text-amber-500 animate-pulse flex items-center gap-1.5">
              <Loader2 className="w-3.5 h-3.5 animate-spin" /> Recalculating...
            </Badge>
          ) : (
            <Badge variant="brand" className="px-3 py-1.5 text-xs">
              Digital Twin Model v3.1
            </Badge>
          )}
          <Badge
            variant="outline"
            className="px-3 py-1.5 text-xs font-bold border-emerald-500 text-emerald-600 dark:text-emerald-400"
            title="Composite Health Score indicating environmental factor alignment (0-100%)"
          >
            Health: {healthScore}%
          </Badge>
        </div>
      </div>

      {/* Top Section: Digital Twin Status & Stage Timeline Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
        
        {/* Section 1: Digital Twin Status Card (5 cols) */}
        <div className="lg:col-span-5">
          <Card padding="p-6 sm:p-8" header="Digital Twin Status" subtitle="Real-time crop lifecycle & model telemetry">
            <div className="space-y-5">
              
              {/* Crop & Confidence Row */}
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-100 dark:border-slate-800">
                  <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                    <Sprout className="w-3.5 h-3.5 text-emerald-500" /> Crop Specie
                  </div>
                  <div className="text-lg font-black text-slate-900 dark:text-white mt-1">
                    Lettuce
                  </div>
                  <div className="text-[11px] font-medium text-slate-500">Butterhead Hydroponic</div>
                </div>

                <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-100 dark:border-slate-800" title="Physics-informed ML model confidence based on sensor calibration log">
                  <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                    <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" /> Confidence
                  </div>
                  <div className="text-lg font-black text-emerald-600 dark:text-emerald-400 mt-1">
                    90%
                  </div>
                  <div className="text-[11px] font-medium text-slate-500">Physics + ML Model</div>
                </div>
              </div>

              {/* Growth Cycle & Current Stage */}
              <div className="p-4 rounded-xl bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-100 dark:border-emerald-900/50 space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-bold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                    <Calendar className="w-4 h-4 text-emerald-600 dark:text-emerald-400" /> Growth Cycle Progress
                  </span>
                  <span className="text-xs font-black text-emerald-600 dark:text-emerald-400">
                    Day {currentDay} / 30
                  </span>
                </div>

                {/* Day Slider */}
                <input
                  type="range"
                  min="1"
                  max="30"
                  value={currentDay}
                  onChange={(e) => setCurrentDay(parseInt(e.target.value, 10))}
                  className="w-full accent-emerald-600 cursor-pointer"
                />

                <div className="flex justify-between items-center pt-1 border-t border-emerald-100 dark:border-emerald-900/40">
                  <span className="text-xs text-slate-500 font-medium">Current Stage:</span>
                  <Badge variant="brand" className="px-3 py-1 text-xs font-bold uppercase tracking-wider">
                    {currentStage.name} ({currentStage.range})
                  </Badge>
                </div>
              </div>

            </div>
          </Card>
        </div>

        {/* Section 2: Growth Stage Timeline (7 cols) */}
        <div className="lg:col-span-7">
          <Card padding="p-6 sm:p-8" header="Growth Stage Timeline" subtitle="Phenological stage mapping across 30 days">
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 items-stretch h-full">
              {stages.map((stage) => {
                const isActive = currentStage.id === stage.id;
                return (
                  <button
                    key={stage.id}
                    onClick={() => setCurrentDay(stage.start === 1 ? 4 : stage.start === 8 ? 14 : stage.start === 21 ? 24 : 29)}
                    className={`p-4 rounded-2xl text-left border transition-all flex flex-col justify-between cursor-pointer ${
                      isActive
                        ? 'border-emerald-500 bg-emerald-500/10 shadow-lg shadow-emerald-500/10 ring-2 ring-emerald-500/30 scale-102'
                        : 'border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/40 hover:border-slate-300 dark:hover:border-slate-700'
                    }`}
                  >
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className={`text-[10px] font-black uppercase tracking-wider ${
                          isActive ? 'text-emerald-600 dark:text-emerald-400' : 'text-slate-400'
                        }`}>
                          Stage {stage.id === 'seedling' ? '1' : stage.id === 'vegetative' ? '2' : stage.id === 'maturity' ? '3' : '4'}
                        </span>
                        {isActive && (
                          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                        )}
                      </div>
                      <div className="font-extrabold text-sm text-slate-900 dark:text-white">
                        {stage.name}
                      </div>
                      <div className="text-xs font-medium text-slate-500 dark:text-slate-400 mt-1">
                        {stage.range}
                      </div>
                    </div>

                    <div className="mt-4 pt-2 border-t border-slate-200/60 dark:border-slate-800 flex justify-between items-center text-[10px]">
                      <span className={isActive ? 'font-bold text-emerald-600 dark:text-emerald-400' : 'text-slate-400'}>
                        {isActive ? 'Active Stage' : 'Select Stage'}
                      </span>
                    </div>
                  </button>
                );
              })}
            </div>
          </Card>
        </div>

      </div>

      {/* Main 2-Column Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left Column: Simulator Sliders + Environmental Factor Analysis (4 cols) */}
        <div className="lg:col-span-4 space-y-6">
          
          {/* Controls Card */}
          <Card padding="p-6 sm:p-8" header="Simulation Parameters" subtitle="Adjust virtual greenhouse variables">
            <div className="space-y-6">
              
              {/* Temperature Slider */}
              <div>
                <div className="flex justify-between items-center text-xs font-bold mb-2">
                  <span className="text-slate-700 dark:text-slate-300 flex items-center gap-1.5" title="Optimal root zone and canopy air temperature (20-24°C) for leaf expansion and photosynthate accumulation">
                    🌡️ Air Temp (°C) <HelpCircle className="w-3.5 h-3.5 text-slate-400 cursor-help inline" />
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
                  <span className="text-slate-700 dark:text-slate-300 flex items-center gap-1.5" title="Vapor Pressure Deficit (VPD) driver (60-75%). Controls stomatal transpiration without leaf wetness">
                    💧 Relative Humidity (%) <HelpCircle className="w-3.5 h-3.5 text-slate-400 cursor-help inline" />
                  </span>
                  <span className="text-emerald-600 dark:text-emerald-400 font-extrabold text-sm">{humidity}%</span>
                </div>
                <input
                  type="range"
                  min="40"
                  max="90"
                  step="1"
                  value={humidity}
                  onChange={(e) => setHumidity(parseInt(e.target.value, 10))}
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
                  <span className="text-slate-700 dark:text-slate-300 flex items-center gap-1.5" title="Electrical Conductivity (1.8-2.5 mS/cm) measuring total dissolved salt ion concentration for root uptake">
                    ⚡ Nutrient EC (mS/cm) <HelpCircle className="w-3.5 h-3.5 text-slate-400 cursor-help inline" />
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
                  <span className="text-slate-700 dark:text-slate-300 flex items-center gap-1.5" title="Hydrogen ion activity (5.8-6.5) dictating Nitrogen, Phosphorus, and Micronutrient bioavailability">
                    🧪 Solution pH <HelpCircle className="w-3.5 h-3.5 text-slate-400 cursor-help inline" />
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

              {/* Control Action Buttons: Save & Reset */}
              <div className="pt-2 space-y-2">
                <Button
                  variant="primary"
                  size="sm"
                  onClick={handleSaveSimulation}
                  icon={saveToast ? Check : Save}
                  className="w-full justify-center text-xs font-bold"
                >
                  {saveToast ? 'Simulation Saved!' : 'Save Current Simulation'}
                </Button>

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

          {/* Section 3: Environmental Factor Analysis (Growth Factors Card) */}
          <Card padding="p-6 sm:p-8" header="Growth Factors" subtitle="Simulation engine calculated physiological indices">
            <div className="space-y-4">
              
              {/* Temperature Factor */}
              <div>
                <div className="flex justify-between items-center text-xs font-bold mb-1.5">
                  <span className="text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                    <Thermometer className="w-3.5 h-3.5 text-emerald-500" /> Temperature Factor
                  </span>
                  <span className="font-extrabold text-slate-900 dark:text-white">
                    {factorPercentages.temperature}%
                  </span>
                </div>
                <div className="w-full h-2 rounded-full bg-slate-100 dark:bg-slate-800 overflow-hidden">
                  <div
                    style={{ width: `${factorPercentages.temperature}%` }}
                    className={`h-full transition-all duration-500 ease-out rounded-full ${
                      factorPercentages.temperature >= 90 ? 'bg-emerald-500' : factorPercentages.temperature >= 70 ? 'bg-amber-500' : 'bg-rose-500'
                    }`}
                  />
                </div>
              </div>

              {/* Humidity Factor */}
              <div>
                <div className="flex justify-between items-center text-xs font-bold mb-1.5">
                  <span className="text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                    <Droplets className="w-3.5 h-3.5 text-teal-500" /> Humidity Factor
                  </span>
                  <span className="font-extrabold text-slate-900 dark:text-white">
                    {factorPercentages.humidity}%
                  </span>
                </div>
                <div className="w-full h-2 rounded-full bg-slate-100 dark:bg-slate-800 overflow-hidden">
                  <div
                    style={{ width: `${factorPercentages.humidity}%` }}
                    className={`h-full transition-all duration-500 ease-out rounded-full ${
                      factorPercentages.humidity >= 90 ? 'bg-emerald-500' : factorPercentages.humidity >= 70 ? 'bg-amber-500' : 'bg-rose-500'
                    }`}
                  />
                </div>
              </div>

              {/* Nutrients (EC) Factor */}
              <div>
                <div className="flex justify-between items-center text-xs font-bold mb-1.5">
                  <span className="text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                    <Gauge className="w-3.5 h-3.5 text-sky-500" /> Nutrients Factor (EC)
                  </span>
                  <span className="font-extrabold text-slate-900 dark:text-white">
                    {factorPercentages.nutrients}%
                  </span>
                </div>
                <div className="w-full h-2 rounded-full bg-slate-100 dark:bg-slate-800 overflow-hidden">
                  <div
                    style={{ width: `${factorPercentages.nutrients}%` }}
                    className={`h-full transition-all duration-500 ease-out rounded-full ${
                      factorPercentages.nutrients >= 90 ? 'bg-emerald-500' : factorPercentages.nutrients >= 70 ? 'bg-amber-500' : 'bg-rose-500'
                    }`}
                  />
                </div>
              </div>

              {/* pH Factor */}
              <div>
                <div className="flex justify-between items-center text-xs font-bold mb-1.5">
                  <span className="text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                    <TestTube className="w-3.5 h-3.5 text-purple-500" /> pH Factor
                  </span>
                  <span className="font-extrabold text-slate-900 dark:text-white">
                    {factorPercentages.ph}%
                  </span>
                </div>
                <div className="w-full h-2 rounded-full bg-slate-100 dark:bg-slate-800 overflow-hidden">
                  <div
                    style={{ width: `${factorPercentages.ph}%` }}
                    className={`h-full transition-all duration-500 ease-out rounded-full ${
                      factorPercentages.ph >= 90 ? 'bg-emerald-500' : factorPercentages.ph >= 70 ? 'bg-amber-500' : 'bg-rose-500'
                    }`}
                  />
                </div>
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
                {yieldGainPercent >= 0 ? `+${yieldGainPercent}%` : `${yieldGainPercent}%`}{' '}
                <span className="text-xl font-semibold text-emerald-200">
                  {yieldGainPercent >= 0 ? 'Yield Increase' : 'Yield Decrease'}
                </span>
              </div>
              <p className="text-xs text-emerald-100 mt-1">
                Estimated harvest weight ({yieldData.expectedWeight}g) compared to baseline hydroponic cycles ({yieldData.baselineWeight}g).
              </p>
            </div>
            
            <div className="hidden sm:flex p-4 bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 items-center justify-center shrink-0">
              <Zap className="w-10 h-10 text-amber-300" />
            </div>
          </div>

          {/* AI Optimization Comparison Section */}
          <Card padding="p-6 sm:p-8" header="AI Optimization Comparison" subtitle="Before Optimization vs AI Optimized Environmental Trajectory">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-stretch">
              
              {/* Current Environment (Before Optimization) */}
              <div className="p-5 rounded-2xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 space-y-4">
                <div className="flex justify-between items-center pb-3 border-b border-slate-200 dark:border-slate-800">
                  <div>
                    <span className="text-[10px] font-black uppercase tracking-wider text-slate-400">Current Simulation</span>
                    <h4 className="text-base font-extrabold text-slate-900 dark:text-white">Current Environment</h4>
                  </div>
                  <Badge variant="outline" className="px-2.5 py-1 text-xs font-bold text-slate-600 dark:text-slate-400">
                    Before Optimization
                  </Badge>
                </div>

                <div className="grid grid-cols-3 gap-3 text-center">
                  <div className="p-3 rounded-xl bg-white dark:bg-slate-950 border border-slate-100 dark:border-slate-800">
                    <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Harvest Weight</div>
                    <div className="text-lg font-black text-slate-900 dark:text-white mt-1">
                      {simResult.yield.expectedWeight}g
                    </div>
                  </div>

                  <div className="p-3 rounded-xl bg-white dark:bg-slate-950 border border-slate-100 dark:border-slate-800">
                    <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Harvest Day</div>
                    <div className="text-lg font-black text-slate-900 dark:text-white mt-1">
                      Day {simResult.harvestDay}
                    </div>
                  </div>

                  <div className="p-3 rounded-xl bg-white dark:bg-slate-950 border border-slate-100 dark:border-slate-800">
                    <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Health Score</div>
                    <div className="text-lg font-black text-amber-500 mt-1">
                      {simResult.healthScore}%
                    </div>
                  </div>
                </div>
              </div>

              {/* AI Optimized */}
              <div className="p-5 rounded-2xl bg-slate-900 border border-emerald-500/30 shadow-lg space-y-4">
                <div className="flex justify-between items-center pb-3 border-b border-emerald-900/40">
                  <div>
                    <span className="text-[10px] font-black uppercase tracking-wider text-emerald-400 flex items-center gap-1">
                      <Sparkles className="w-3 h-3 text-amber-300" /> Recommendation
                    </span>
                    <h4 className="text-base font-extrabold text-white">AI Optimized</h4>
                  </div>
                  <Badge variant="brand" className="px-2.5 py-1 text-xs font-bold uppercase tracking-wider">
                    Peak Performance
                  </Badge>
                </div>

                <div className="grid grid-cols-3 gap-3 text-center">
                  <div className="p-3 rounded-xl bg-emerald-950/40 border border-emerald-800/40">
                    <div className="text-[10px] font-bold text-emerald-300 uppercase tracking-wider">Harvest Weight</div>
                    <div className="text-lg font-black text-emerald-400 mt-1">
                      {baselineResult.yield.expectedWeight}g
                    </div>
                  </div>

                  <div className="p-3 rounded-xl bg-emerald-950/40 border border-emerald-800/40">
                    <div className="text-[10px] font-bold text-emerald-300 uppercase tracking-wider">Harvest Day</div>
                    <div className="text-lg font-black text-emerald-400 mt-1">
                      Day {baselineResult.harvestDay}
                    </div>
                  </div>

                  <div className="p-3 rounded-xl bg-emerald-950/40 border border-emerald-800/40">
                    <div className="text-[10px] font-bold text-emerald-300 uppercase tracking-wider">Health Score</div>
                    <div className="text-lg font-black text-emerald-400 mt-1">
                      {baselineResult.healthScore}%
                    </div>
                  </div>
                </div>

                <Button
                  variant="primary"
                  size="sm"
                  onClick={() => { setTemp(22.0); setHumidity(65); setEc(2.2); setPh(6.2); }}
                  icon={Zap}
                  className="w-full justify-center text-xs font-bold"
                >
                  Apply AI Optimization Recipe (22.0°C / 65% / 2.2 EC / 6.2 pH)
                </Button>
              </div>

            </div>
          </Card>

          {/* High Visibility 30-Day Growth Curve Chart Container */}
          <Card padding="p-6 sm:p-8" header="Projected 30-Day Crop Growth Curve" subtitle="Baseline vs Simulated Environmental Trajectory">
            
            <div className="h-64 flex items-end justify-between gap-2.5 pt-10 pb-4 px-2 border-b border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/40 rounded-xl">
              {chartDays.map((day) => {
                const basePoint = baselineResult.growthCurve.find(p => p.day === day) || { weight: 0 };
                const simPoint = growthCurve.find(p => p.day === day) || { weight: 0 };
                
                const baseVal = basePoint.weight;
                const simulatedVal = simPoint.weight;

                const baseHeightPercent = Math.min(100, Math.round((baseVal / maxWeight) * 100));
                const simHeightPercent = Math.min(100, Math.round((simulatedVal / maxWeight) * 100));

                const isCurrentSelectedDay = day === currentDay || Math.abs(day - currentDay) <= 1;
                
                return (
                  <div key={day} className="flex-1 flex flex-col items-center gap-1.5 group relative h-full justify-end">
                    
                    {/* Tooltip Hover Value */}
                    <div className={`text-[11px] font-extrabold transition-all duration-300 ${
                      isCurrentSelectedDay
                        ? 'text-emerald-600 dark:text-emerald-400 scale-110 font-black'
                        : 'text-slate-500 opacity-80 group-hover:scale-110'
                    }`}>
                      {simulatedVal}g
                    </div>

                    {/* Dual Bars: Baseline vs Simulated */}
                    <div className="w-full flex items-end justify-center gap-1 h-full">
                      {/* Baseline Bar */}
                      <div
                        style={{ height: `${baseHeightPercent}%` }}
                        className="w-1.5 sm:w-2 bg-slate-300 dark:bg-slate-700 rounded-t-sm transition-all duration-500 ease-out"
                        title={`Baseline: ${baseVal}g`}
                      />
                      {/* Simulated Bar */}
                      <div
                        style={{ height: `${simHeightPercent}%` }}
                        className={`w-3 sm:w-4 rounded-t-md transition-all duration-500 ease-out shadow-xs ${
                          isCurrentSelectedDay
                            ? 'bg-gradient-to-t from-emerald-500 to-amber-300 ring-2 ring-emerald-400/50 scale-105'
                            : 'bg-gradient-to-t from-emerald-600 to-teal-400 group-hover:from-emerald-500 group-hover:to-teal-300'
                        } ${isCalculating ? 'opacity-50 scale-95' : 'opacity-100 scale-100'}`}
                        title={`Simulated: ${simulatedVal}g (Day ${day})`}
                      />
                    </div>

                    <span className={`text-[10px] font-bold mt-1 ${
                      isCurrentSelectedDay ? 'text-emerald-600 dark:text-emerald-400 font-extrabold underline' : 'text-slate-500 dark:text-slate-400'
                    }`}>
                      Day {day}
                    </span>
                  </div>
                );
              })}
            </div>

            {/* Legend & Stats Footer */}
            <div className="flex flex-wrap items-center justify-between gap-4 text-xs text-slate-600 dark:text-slate-400 mt-4 pt-2">
              <div className="flex items-center gap-4">
                <span className="flex items-center gap-1.5 font-medium">
                  <span className="w-3 h-3 bg-emerald-600 rounded-sm" /> Simulated Trajectory ({yieldData.expectedWeight}g)
                </span>
                <span className="flex items-center gap-1.5 font-medium">
                  <span className="w-3 h-3 bg-slate-300 dark:bg-slate-700 rounded-sm" /> Baseline ({yieldData.baselineWeight}g)
                </span>
              </div>
              <span className="font-bold text-slate-900 dark:text-white">
                Peak Harvest Window: Day {harvestDay}
              </span>
            </div>
          </Card>

          {/* AI Simulation Insights Section */}
          <Card padding="p-6 sm:p-8" header="AI Simulation Insights & Biological Drivers">
            <div className="space-y-4 text-sm">
              {recommendations.map((rec, idx) => {
                const isWarning = rec.type === 'warning';
                return (
                  <div key={idx} className={`p-4 rounded-xl border flex items-start gap-3 ${
                    isWarning
                      ? 'border-amber-200 dark:border-amber-900/50 bg-amber-50/50 dark:bg-amber-950/20'
                      : 'border-emerald-100 dark:border-emerald-950 bg-emerald-50/50 dark:bg-emerald-950/20'
                  }`}>
                    {isWarning ? (
                      <AlertTriangle className="w-5 h-5 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
                    ) : (
                      <CheckCircle2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
                    )}
                    <div>
                      <div className="font-bold text-slate-900 dark:text-white">{rec.title}</div>
                      <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5 leading-relaxed">
                        {rec.message}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          </Card>

        </div>

      </div>

      {/* Simulation History Card */}
      <Card
        padding="p-6 sm:p-8"
        header="Simulation History"
        subtitle="Local telemetry log of previously saved simulation runs"
      >
        <div className="space-y-4">
          <div className="flex justify-between items-center text-xs font-bold">
            <span className="text-slate-500 dark:text-slate-400 flex items-center gap-1.5">
              <History className="w-4 h-4 text-emerald-500" /> Saved Simulation Runs ({history.length})
            </span>
            {history.length > 0 && (
              <button
                onClick={handleClearHistory}
                className="text-rose-500 hover:text-rose-600 dark:hover:text-rose-400 flex items-center gap-1 font-semibold transition-colors"
              >
                <Trash2 className="w-3.5 h-3.5" /> Clear History
              </button>
            )}
          </div>

          {history.length === 0 ? (
            <div className="text-center py-10 border border-dashed border-slate-200 dark:border-slate-800 rounded-2xl bg-slate-50/50 dark:bg-slate-950/30">
              <History className="w-8 h-8 text-slate-300 dark:text-slate-700 mx-auto mb-2" />
              <p className="text-xs text-slate-500 dark:text-slate-400 font-semibold">No saved simulation runs found.</p>
              <p className="text-[11px] text-slate-400 dark:text-slate-500 mt-1 max-w-sm mx-auto">
                Adjust parameters above and click "Save Current Simulation" to preserve customized scenarios for future review.
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs font-medium text-slate-600 dark:text-slate-300">
                <thead>
                  <tr className="border-b border-slate-200 dark:border-slate-800 text-[10px] uppercase text-slate-400 font-bold tracking-wider">
                    <th className="pb-3 px-3">Date</th>
                    <th className="pb-3 px-3">Parameters (Temp / Hum / EC / pH)</th>
                    <th className="pb-3 px-3">Yield</th>
                    <th className="pb-3 px-3">Harvest Day</th>
                    <th className="pb-3 px-3">Health Score</th>
                    <th className="pb-3 px-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60">
                  {history.map((run) => (
                    <tr key={run.id} className="hover:bg-slate-50/60 dark:hover:bg-slate-900/40 transition-colors">
                      <td className="py-3 px-3 font-semibold text-slate-900 dark:text-white whitespace-nowrap">
                        {run.date}
                      </td>
                      <td className="py-3 px-3 font-mono text-[11px]">
                        {run.temp}°C · {run.humidity}% · {run.ec} mS · pH {run.ph}
                      </td>
                      <td className="py-3 px-3 font-extrabold text-emerald-600 dark:text-emerald-400">
                        {run.yieldWeight}g ({run.yieldGainPercent >= 0 ? `+${run.yieldGainPercent}%` : `${run.yieldGainPercent}%`})
                      </td>
                      <td className="py-3 px-3 font-bold text-slate-700 dark:text-slate-300">
                        Day {run.harvestDay}
                      </td>
                      <td className="py-3 px-3">
                        <Badge variant="outline" className={`px-2 py-0.5 text-[10px] font-bold ${
                          run.healthScore >= 90 ? 'border-emerald-500 text-emerald-500' : run.healthScore >= 75 ? 'border-amber-500 text-amber-500' : 'border-rose-500 text-rose-500'
                        }`}>
                          {run.healthScore}%
                        </Badge>
                      </td>
                      <td className="py-3 px-3 text-right whitespace-nowrap">
                        <div className="flex items-center justify-end gap-2">
                          <button
                            onClick={() => handleLoadSimulation(run)}
                            className="px-2.5 py-1 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 font-bold text-[11px] transition-colors flex items-center gap-1 cursor-pointer"
                            title="Load these parameters into simulator"
                          >
                            <ArrowUpRight className="w-3.5 h-3.5" /> Restore Run
                          </button>
                          <button
                            onClick={() => handleDeleteHistoryItem(run.id)}
                            className="p-1 rounded-lg text-slate-400 hover:text-rose-500 hover:bg-rose-500/10 transition-colors cursor-pointer"
                            title="Delete entry"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </Card>

    </div>
  );
}
