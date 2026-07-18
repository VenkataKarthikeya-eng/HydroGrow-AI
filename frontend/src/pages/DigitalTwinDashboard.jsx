import React, { useState, useEffect, useContext } from 'react';
import { AppContext } from '../context/AppContext';
import { useNavigate, Link } from 'react-router-dom';
import client from '../api/client';
import { Lock, Cpu, RotateCw, Activity } from 'lucide-react';
import FarmSimulator from '../components/twin/FarmSimulator';
import GrowthForecastChart from '../components/twin/GrowthForecastChart';
import ScenarioComparison from '../components/twin/ScenarioComparison';
import HarvestPredictionCard from '../components/twin/HarvestPredictionCard';
import OptimizationRecommendations from '../components/twin/OptimizationRecommendations';

function DigitalTwinDashboard() {
  const { isAuthenticated, logout } = useContext(AppContext);
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [simulationResult, setSimulationResult] = useState(null);
  const [forecast, setForecast] = useState([]);
  const [recommendations, setRecommendations] = useState([]);

  // Live WebSocket state variables
  const [simulatingDay, setSimulatingDay] = useState(0);
  const [simulatingStage, setSimulatingStage] = useState('');
  const [wsStatus, setWsStatus] = useState('offline');

  const fetchTwinState = async () => {
    try {
      const [recsRes, historyRes] = await Promise.all([
        client.get('/api/twin/recommendations'),
        client.get('/api/twin/history')
      ]);
      setRecommendations(recsRes.data);
      if (historyRes.data.length > 0) {
        // Load latest simulation forecast details
        const latestSimId = historyRes.data[0].id;
        const forecastRes = await client.get(`/api/twin/forecast/${latestSimId}`);
        setForecast(forecastRes.data);
        
        // Setup mock result matching structure
        setSimulationResult({
          yield_change_percentage: historyRes.data[0].yield_change_percentage,
          final_prediction: {
            weight: historyRes.data[0].final_weight,
            health: historyRes.data[0].final_health
          },
          recommendations: ["Based on the latest recorded simulation parameters."]
        });
      }
    } catch (err) {
      if (err.response?.status === 401) {
        logout();
        navigate('/login');
      } else {
        setError(err.message || 'Failed to fetch digital twin settings.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!isAuthenticated) {
      setLoading(false);
      return;
    }
    fetchTwinState();
  }, [isAuthenticated]);

  // WebSocket Live streams
  useEffect(() => {
    if (!isAuthenticated) return;
    const wsUrlBase = "http://localhost:8000".replace(/^http/, "ws");
    const token = localStorage.getItem("token");
    if (!token) return;

    const ws = new WebSocket(`${wsUrlBase}/ws/iot/live?token=${token}`);

    ws.onopen = () => setWsStatus('live');
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'digital_twin_progress') {
          setForecast(prev => {
            const exists = prev.some(item => item.day === data.day);
            if (exists) return prev;

            return [...prev, {
              day: data.day,
              predicted_height: Math.round(data.day * 0.9 * 100) / 100,
              predicted_weight: data.weight,
              health_score: data.health_score,
              growth_stage: data.growth_stage
            }].sort((a, b) => a.day - b.day);
          });
          setSimulatingDay(data.day);
          setSimulatingStage(data.growth_stage);
        }
      } catch (err) {
        console.error("Error parsing socket twin frame:", err);
      }
    };
    ws.onclose = () => setWsStatus('offline');
    ws.onerror = () => setWsStatus('offline');

    return () => ws.close();
  }, [isAuthenticated]);

  const handleSimulationComplete = (data) => {
    // Clear forecast for live animation rebuild
    setForecast([]);
    setSimulatingDay(0);
    setSimulatingStage('');

    setSimulationResult(data);
    if (data.harvest_prediction) {
      // Re-fetch recommendations
      fetchTwinState();
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="max-w-md mx-auto my-16 p-8 glass-panel border border-slate-900 bg-slate-950/20 text-center space-y-6 rounded-3xl shadow-xl animate-fadeIn">
        <div className="p-4 bg-amber-500/10 rounded-full border border-amber-500/20 text-amber-400 w-fit mx-auto animate-pulse">
          <Lock className="h-10 w-10" />
        </div>
        <div className="space-y-2">
          <h2 className="text-lg font-black text-white uppercase tracking-wider">Digital Twin Locked</h2>
          <p className="text-slate-400 text-xs leading-relaxed font-semibold">
            Greenhouse digital twin simulations require user authentication. Please sign in.
          </p>
        </div>
        <Link to="/login" className="w-full py-3 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-slate-950 font-bold block transition-all hover:shadow-lg">
          Sign In
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-6 space-y-6 animate-fadeIn">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-900 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-black tracking-tight text-white uppercase">Digital Twin Platform</h1>
            <span className={`px-2 py-0.5 rounded text-[8px] font-black uppercase tracking-wider flex items-center gap-1 ${wsStatus === 'live' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-550/20' : 'bg-slate-900 text-slate-500 border border-slate-800'}`}>
              <Activity className="h-3 w-3" /> {wsStatus}
            </span>
          </div>
          <p className="text-slate-400 text-[11px] mt-1">
            Simulate crop lifecycle responses, compute yield forecasting, and generate optimization suggestions.
          </p>
        </div>
      </div>

      {loading ? (
        <div className="py-24 text-center space-y-4">
          <RotateCw className="h-10 w-10 text-emerald-400 animate-spin mx-auto" />
          <p className="text-slate-500 text-xs font-semibold">Aligning digital twin farm telemetry parameters...</p>
        </div>
      ) : error ? (
        <div className="p-4 rounded-xl border border-rose-500/10 bg-rose-500/5 text-rose-400 text-xs font-semibold">
          Error: {error}
        </div>
      ) : (
        <div className="space-y-6">
          {simulatingDay > 0 && (
            <div className="glass-panel p-4 rounded-2xl border border-slate-900 bg-emerald-500/5 flex items-center gap-4 animate-pulse">
              <Cpu className="h-6 w-6 text-emerald-400 shrink-0" />
              <div className="flex-grow space-y-1.5">
                <div className="flex justify-between text-[10px] font-bold text-slate-300">
                  <span className="uppercase tracking-wider">Simulating Stage Progress</span>
                  <span className="font-mono text-emerald-400">Day {simulatingDay} ({simulatingStage})</span>
                </div>
                <div className="h-1.5 w-full bg-slate-900 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-emerald-500 rounded-full transition-all duration-300"
                    style={{ width: `${(simulatingDay / 35) * 100}%` }}
                  />
                </div>
              </div>
            </div>
          )}

          <div className="grid md:grid-cols-3 gap-6">
            <div className="space-y-6">
              <FarmSimulator onSimulationComplete={handleSimulationComplete} />
              <HarvestPredictionCard 
                harvestData={simulationResult?.harvest_prediction} 
                riskFactors={simulationResult?.risk_factors}
              />
            </div>

            <div className="md:col-span-2 space-y-6">
              <GrowthForecastChart data={forecast} />
              <div className="grid md:grid-cols-2 gap-6">
                <ScenarioComparison simulationResult={simulationResult} />
                <OptimizationRecommendations recommendations={recommendations} />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default DigitalTwinDashboard;
