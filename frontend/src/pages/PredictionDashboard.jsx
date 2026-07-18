import React, { useContext, useState } from 'react';
import { AppContext } from '../context/AppContext';
import { useNavigate } from 'react-router-dom';
import MetricCard from '../components/MetricCard';
import PredictionCard from '../components/PredictionCard';
import RecommendationCard from '../components/RecommendationCard';
import LoadingSpinner from '../components/LoadingSpinner';
import { 
  Sprout, Thermometer, Droplets, Wind, Activity, Zap, 
  Trash2, Send, Save, ArrowLeftRight, CheckCircle2, XCircle
} from 'lucide-react';

function PredictionDashboard() {
  const {
    predictionInputs,
    predictionResult,
    isPredicting,
    predictionError,
    runPrediction,
    resetPrediction,
    saveCurrentPrediction
  } = useContext(AppContext);

  const navigate = useNavigate();

  // Local state for form validation & tracking
  const [formData, setFormData] = useState(predictionInputs);
  const [localError, setLocalError] = useState(null);
  const [saveLabel, setSaveLabel] = useState('');
  const [showSaveModal, setShowSaveModal] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: parseFloat(value) || 0
    }));
  };

  const handleSliderChange = (name, val) => {
    setFormData(prev => ({
      ...prev,
      [name]: val
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLocalError(null);
    try {
      await runPrediction(formData);
    } catch (err) {
      setLocalError(err.message || 'Failed to generate crop prediction.');
    }
  };

  const handleReset = () => {
    resetPrediction();
    setFormData(predictionInputs);
    setLocalError(null);
  };

  const handleSave = (e) => {
    e.preventDefault();
    if (!saveLabel.trim()) return;
    saveCurrentPrediction(saveLabel);
    setSaveSuccess(true);
    setSaveLabel('');
    setTimeout(() => {
      setSaveSuccess(false);
      setShowSaveModal(false);
    }, 1500);
  };

  return (
    <div className="space-y-8 py-4">
      {/* Title Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-slate-900 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white">Prediction Dashboard</h1>
          <p className="text-slate-400 text-xs mt-1">Configure greenhouse conditions to forecast crop growth dynamics.</p>
        </div>
        
        {predictionResult && (
          <div className="flex items-center gap-2">
            <button
              onClick={() => navigate('/assistant')}
              className="py-2 px-3 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/20 text-emerald-400 text-xs font-semibold flex items-center gap-1.5 transition-all"
            >
              <ArrowLeftRight className="h-4 w-4" />
              Discuss in Chat
            </button>
            <button
              onClick={() => setShowSaveModal(true)}
              className="py-2 px-3 rounded-lg bg-slate-900 hover:bg-slate-850 border border-slate-800 text-slate-200 text-xs font-semibold flex items-center gap-1.5 transition-all"
            >
              <Save className="h-4 w-4 text-emerald-400" />
              Save Run
            </button>
          </div>
        )}
      </div>

      {/* Global Error Banner */}
      {(predictionError || localError) && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs flex items-start gap-2 animate-pulse">
          <XCircle className="h-4.5 w-4.5 shrink-0 mt-0.5" />
          <div>
            <span className="font-bold">System Connection Failure:</span>
            <p className="mt-0.5 text-rose-300">{predictionError || localError}</p>
          </div>
        </div>
      )}

      {/* Save Modal */}
      {showSaveModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 max-w-sm w-full space-y-4">
            <h3 className="text-lg font-bold text-white">Save Prediction Session</h3>
            {saveSuccess ? (
              <div className="flex items-center gap-2 text-emerald-400 text-sm py-2">
                <CheckCircle2 className="h-5 w-5" /> Saved successfully to profile library.
              </div>
            ) : (
              <form onSubmit={handleSave} className="space-y-4">
                <div>
                  <label className="block text-xs text-slate-400 mb-1.5">Run Identifier Label</label>
                  <input
                    type="text"
                    required
                    value={saveLabel}
                    onChange={(e) => setSaveLabel(e.target.value)}
                    placeholder="e.g. Batch 12 - High CO2 Test"
                    className="w-full bg-slate-900 border border-slate-800 rounded-lg py-2 px-3 text-xs text-white focus:outline-none focus:border-emerald-500"
                  />
                </div>
                <div className="flex justify-end gap-2 text-xs font-semibold">
                  <button
                    type="button"
                    onClick={() => setShowSaveModal(false)}
                    className="py-2 px-3 rounded-lg bg-slate-900 hover:bg-slate-850 border border-slate-800 text-slate-400"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="py-2 px-3 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-white"
                  >
                    Save session
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}

      <div className="grid lg:grid-cols-12 gap-8 items-start">
        {/* Left Form: Inputs Form */}
        <form onSubmit={handleSubmit} className="lg:col-span-7 space-y-6">
          {/* Section 1: Ambient Environmental Conditions */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-800/80 space-y-5">
            <h3 className="text-sm font-extrabold text-white uppercase tracking-wider flex items-center gap-2 border-b border-slate-900 pb-2">
              <Wind className="h-4.5 w-4.5 text-emerald-400" />
              1. Environmental Conditions
            </h3>
            
            <div className="grid sm:grid-cols-3 gap-6">
              {/* Air Temp */}
              <div className="space-y-2">
                <div className="flex justify-between items-baseline">
                  <label className="text-[11px] font-bold text-slate-300">Air Temp (°C)</label>
                  <span className="text-xs text-emerald-400 font-mono font-bold">{formData.air_temperature.toFixed(1)}</span>
                </div>
                <input
                  type="range"
                  min="10.0"
                  max="40.0"
                  step="0.5"
                  name="air_temperature"
                  value={formData.air_temperature}
                  onChange={(e) => handleSliderChange('air_temperature', parseFloat(e.target.value))}
                  className="w-full accent-emerald-500 cursor-ew-resize bg-slate-900 rounded-lg appearance-none h-1.5"
                />
                <span className="text-[9px] text-slate-500 block">Range: 10.0 - 40.0 °C</span>
              </div>

              {/* Humidity */}
              <div className="space-y-2">
                <div className="flex justify-between items-baseline">
                  <label className="text-[11px] font-bold text-slate-300">Humidity (%)</label>
                  <span className="text-xs text-emerald-400 font-mono font-bold">{formData.humidity.toFixed(0)}</span>
                </div>
                <input
                  type="range"
                  min="30"
                  max="90"
                  step="1"
                  name="humidity"
                  value={formData.humidity}
                  onChange={(e) => handleSliderChange('humidity', parseFloat(e.target.value))}
                  className="w-full accent-emerald-500 cursor-ew-resize bg-slate-900 rounded-lg appearance-none h-1.5"
                />
                <span className="text-[9px] text-slate-500 block">Range: 30.0 - 90.0 %</span>
              </div>

              {/* CO2 */}
              <div className="space-y-2">
                <div className="flex justify-between items-baseline">
                  <label className="text-[11px] font-bold text-slate-300">CO2 (ppm)</label>
                  <span className="text-xs text-emerald-400 font-mono font-bold">{formData.co2.toFixed(0)}</span>
                </div>
                <input
                  type="range"
                  min="300"
                  max="1000"
                  step="10"
                  name="co2"
                  value={formData.co2}
                  onChange={(e) => handleSliderChange('co2', parseFloat(e.target.value))}
                  className="w-full accent-emerald-500 cursor-ew-resize bg-slate-900 rounded-lg appearance-none h-1.5"
                />
                <span className="text-[9px] text-slate-500 block">Range: 300 - 1000 ppm</span>
              </div>
            </div>
          </div>

          {/* Section 2: Water Parameters */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-800/80 space-y-5">
            <h3 className="text-sm font-extrabold text-white uppercase tracking-wider flex items-center gap-2 border-b border-slate-900 pb-2">
              <Thermometer className="h-4.5 w-4.5 text-blue-400" />
              2. Water Parameters
            </h3>
            
            <div className="grid sm:grid-cols-3 gap-6">
              {/* pH */}
              <div className="space-y-2">
                <div className="flex justify-between items-baseline">
                  <label className="text-[11px] font-bold text-slate-300">Water pH</label>
                  <span className="text-xs text-blue-400 font-mono font-bold">{formData.water_ph.toFixed(2)}</span>
                </div>
                <input
                  type="range"
                  min="4.0"
                  max="9.0"
                  step="0.1"
                  name="water_ph"
                  value={formData.water_ph}
                  onChange={(e) => handleSliderChange('water_ph', parseFloat(e.target.value))}
                  className="w-full accent-blue-500 cursor-ew-resize bg-slate-900 rounded-lg appearance-none h-1.5"
                />
                <span className="text-[9px] text-slate-500 block">Range: 4.0 - 9.0</span>
              </div>

              {/* EC */}
              <div className="space-y-2">
                <div className="flex justify-between items-baseline">
                  <label className="text-[11px] font-bold text-slate-300">Water EC (mS/cm)</label>
                  <span className="text-xs text-blue-400 font-mono font-bold">{formData.water_ec.toFixed(2)}</span>
                </div>
                <input
                  type="range"
                  min="0.5"
                  max="5.0"
                  step="0.1"
                  name="water_ec"
                  value={formData.water_ec}
                  onChange={(e) => handleSliderChange('water_ec', parseFloat(e.target.value))}
                  className="w-full accent-blue-500 cursor-ew-resize bg-slate-900 rounded-lg appearance-none h-1.5"
                />
                <span className="text-[9px] text-slate-500 block">Range: 0.5 - 5.0 mS/cm</span>
              </div>

              {/* Water Temp */}
              <div className="space-y-2">
                <div className="flex justify-between items-baseline">
                  <label className="text-[11px] font-bold text-slate-300">Water Temp (°C)</label>
                  <span className="text-xs text-blue-400 font-mono font-bold">{formData.water_temperature.toFixed(1)}</span>
                </div>
                <input
                  type="range"
                  min="15.0"
                  max="35.0"
                  step="0.5"
                  name="water_temperature"
                  value={formData.water_temperature}
                  onChange={(e) => handleSliderChange('water_temperature', parseFloat(e.target.value))}
                  className="w-full accent-blue-500 cursor-ew-resize bg-slate-900 rounded-lg appearance-none h-1.5"
                />
                <span className="text-[9px] text-slate-500 block">Range: 15.0 - 35.0 °C</span>
              </div>
            </div>
          </div>

          {/* Section 3: Plant Starting Conditions & Management */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-800/80 space-y-6">
            <div className="grid sm:grid-cols-2 gap-8">
              {/* Plant Starting Conditions */}
              <div className="space-y-4">
                <h3 className="text-xs font-extrabold text-white uppercase tracking-wider flex items-center gap-1.5 border-b border-slate-900 pb-2">
                  <Sprout className="h-4 w-4 text-emerald-400" /> Seedling Details
                </h3>

                <div className="grid gap-4">
                  {/* Height */}
                  <div className="flex items-center justify-between gap-4">
                    <label className="text-[11px] text-slate-300 font-medium shrink-0">Height (cm)</label>
                    <div className="flex flex-col gap-1 w-32">
                      <input
                        type="number"
                        min="5.0"
                        max="20.0"
                        step="0.1"
                        name="seedling_height"
                        value={formData.seedling_height}
                        onChange={handleChange}
                        className="bg-slate-950 border border-slate-800 rounded py-1 px-2 text-[11px] font-mono text-white text-right focus:outline-none focus:border-emerald-500"
                      />
                      <span className="text-[9px] text-slate-600 text-right">Range: 5.0 - 20.0</span>
                    </div>
                  </div>

                  {/* Weight */}
                  <div className="flex items-center justify-between gap-4">
                    <label className="text-[11px] text-slate-300 font-medium shrink-0">Weight (g)</label>
                    <div className="flex flex-col gap-1 w-32">
                      <input
                        type="number"
                        min="0.5"
                        max="10.0"
                        step="0.1"
                        name="seedling_weight"
                        value={formData.seedling_weight}
                        onChange={handleChange}
                        className="bg-slate-950 border border-slate-800 rounded py-1 px-2 text-[11px] font-mono text-white text-right focus:outline-none focus:border-emerald-500"
                      />
                      <span className="text-[9px] text-slate-600 text-right">Range: 0.5 - 10.0</span>
                    </div>
                  </div>

                  {/* Root Length */}
                  <div className="flex items-center justify-between gap-4">
                    <label className="text-[11px] text-slate-300 font-medium shrink-0">Root Length (cm)</label>
                    <div className="flex flex-col gap-1 w-32">
                      <input
                        type="number"
                        min="3.0"
                        max="15.0"
                        step="0.1"
                        name="root_length"
                        value={formData.root_length}
                        onChange={handleChange}
                        className="bg-slate-950 border border-slate-800 rounded py-1 px-2 text-[11px] font-mono text-white text-right focus:outline-none focus:border-emerald-500"
                      />
                      <span className="text-[9px] text-slate-600 text-right">Range: 3.0 - 15.0</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Management Inputs */}
              <div className="space-y-4">
                <h3 className="text-xs font-extrabold text-white uppercase tracking-wider flex items-center gap-1.5 border-b border-slate-900 pb-2">
                  <Zap className="h-4 w-4 text-orange-400" /> Operations inputs
                </h3>

                <div className="grid gap-4">
                  {/* Nutrient Solution */}
                  <div className="flex items-center justify-between gap-4">
                    <label className="text-[11px] text-slate-300 font-medium shrink-0">Nutrients (mL)</label>
                    <div className="flex flex-col gap-1 w-32">
                      <input
                        type="number"
                        min="0.0"
                        max="1500.0"
                        step="10.0"
                        name="nutrient_solution"
                        value={formData.nutrient_solution}
                        onChange={handleChange}
                        className="bg-slate-950 border border-slate-800 rounded py-1 px-2 text-[11px] font-mono text-white text-right focus:outline-none focus:border-emerald-500"
                      />
                      <span className="text-[9px] text-slate-600 text-right">Range: 0.0 - 1500.0</span>
                    </div>
                  </div>

                  {/* Water Consumption */}
                  <div className="flex items-center justify-between gap-4">
                    <label className="text-[11px] text-slate-300 font-medium shrink-0">Water Usage (L)</label>
                    <div className="flex flex-col gap-1 w-32">
                      <input
                        type="number"
                        min="0.0"
                        max="500.0"
                        step="5.0"
                        name="water_consumption"
                        value={formData.water_consumption}
                        onChange={handleChange}
                        className="bg-slate-950 border border-slate-800 rounded py-1 px-2 text-[11px] font-mono text-white text-right focus:outline-none focus:border-emerald-500"
                      />
                      <span className="text-[9px] text-slate-600 text-right">Range: 0.0 - 500.0</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Action buttons */}
          <div className="flex gap-4">
            <button
              type="submit"
              disabled={isPredicting}
              className="flex-grow py-3.5 px-4 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 disabled:opacity-50 text-white font-bold text-sm flex items-center justify-center gap-1.5 shadow-lg shadow-emerald-950/20 active:scale-[0.98] transition-all"
            >
              {isPredicting ? (
                <span>Predicting lettuce weight...</span>
              ) : (
                <>
                  <Activity className="h-4.5 w-4.5" />
                  Predict Lettuce Growth
                </>
              )}
            </button>
            
            <button
              type="button"
              onClick={handleReset}
              className="p-3.5 rounded-xl bg-slate-900 border border-slate-850 hover:bg-slate-850 text-slate-400 hover:text-white transition-all active:scale-[0.98]"
              title="Reset parameters"
            >
              <Trash2 className="h-5 w-5" />
            </button>
          </div>
        </form>

        {/* Right Column: Prediction Results */}
        <div className="lg:col-span-5 space-y-6">
          {isPredicting ? (
            <div className="glass-panel p-8 rounded-2xl border border-slate-800">
              <LoadingSpinner message="Calculating predictive weights & biological constraints..." />
            </div>
          ) : predictionResult ? (
            <div className="space-y-6 animate-fadeIn">
              {/* Output Prediction Card */}
              <PredictionCard 
                prediction={predictionResult.prediction} 
                validation={predictionResult.validation} 
              />

              {/* Explainable AI Details */}
              {predictionResult.explanation && (
                <div className="glass-panel p-5 rounded-xl border border-slate-800/80 space-y-4">
                  <h4 className="text-xs font-extrabold uppercase text-slate-400 tracking-wider flex items-center gap-1.5">
                    <Activity className="h-4 w-4 text-emerald-400" />
                    Explainable AI Diagnostics
                  </h4>

                  {/* Summary */}
                  {predictionResult.explanation.summary && (
                    <p className="text-slate-300 text-xs leading-relaxed italic bg-slate-950/45 p-3 rounded-lg border border-slate-900">
                      "{predictionResult.explanation.summary}"
                    </p>
                  )}

                  {/* Positive Factors */}
                  {predictionResult.explanation.positive_factors && 
                   predictionResult.explanation.positive_factors.length > 0 && (
                    <div className="space-y-2">
                      <span className="text-[10px] text-emerald-400/80 uppercase font-extrabold tracking-wider block">Positive Influences</span>
                      <ul className="space-y-1.5">
                        {predictionResult.explanation.positive_factors.map((f, i) => (
                          <li key={i} className="text-slate-300 text-xs flex items-start gap-1.5">
                            <span className="text-emerald-500 font-bold shrink-0">•</span>
                            <div>
                              <strong className="text-white text-xs">{f.factor}:</strong> {f.explanation}
                            </div>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Improvement opportunities */}
                  {predictionResult.explanation.improvement_opportunities && 
                   predictionResult.explanation.improvement_opportunities.length > 0 ? (
                    <div className="space-y-2 pt-2 border-t border-slate-900/60">
                      <span className="text-[10px] text-rose-400/80 uppercase font-extrabold tracking-wider block">Deficit Warnings</span>
                      <ul className="space-y-1.5">
                        {predictionResult.explanation.improvement_opportunities.map((f, i) => (
                          <li key={i} className="text-slate-300 text-xs flex items-start gap-1.5">
                            <span className="text-rose-500 font-bold shrink-0">•</span>
                            <div>
                              <strong className="text-white text-xs">{f.factor}:</strong> {f.explanation}
                            </div>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ) : (
                    <div className="text-[10px] text-slate-500 py-1.5 border-t border-slate-900/60 flex items-center gap-1.5">
                      <CheckCircle2 className="h-4 w-4 text-emerald-500" />
                      No critical environmental deficits detected for optimization.
                    </div>
                  )}

                  {/* Confidence Explanation */}
                  {predictionResult.explanation.confidence_explanation && (
                    <p className="text-[10px] text-slate-500 leading-relaxed pt-2 border-t border-slate-900/60">
                      {predictionResult.explanation.confidence_explanation}
                    </p>
                  )}
                </div>
              )}

              {/* Recommendations list */}
              {predictionResult.recommendations && predictionResult.recommendations.length > 0 && (
                <div className="space-y-4">
                  <h4 className="text-xs font-extrabold uppercase text-slate-400 tracking-wider flex items-center gap-1.5">
                    <Sprout className="h-4 w-4 text-emerald-400" />
                    Agricultural Recommendations ({predictionResult.recommendations.length})
                  </h4>
                  <div className="grid gap-3">
                    {predictionResult.recommendations.map((rec, idx) => (
                      <RecommendationCard key={idx} recommendation={rec} />
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            /* Empty State */
            <div className="glass-panel p-8 rounded-2xl border border-slate-800 text-center space-y-4 py-16 flex flex-col items-center justify-center">
              <div className="p-4 bg-emerald-500/10 rounded-full border border-emerald-500/20 text-emerald-400 w-fit">
                <Sprout className="h-10 w-10 animate-pulse" />
              </div>
              <div className="space-y-1.5 max-w-sm">
                <h3 className="text-base font-bold text-white">Awaiting Model Inputs</h3>
                <p className="text-slate-400 text-xs leading-relaxed">
                  Configure greenhouse air metrics, nutrient saturation, and seedling data then submit the form to receive regression diagnostics.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default PredictionDashboard;
