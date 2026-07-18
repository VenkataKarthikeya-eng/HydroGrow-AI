import React, { useContext, useEffect, useState } from 'react';
import { AppContext } from '../context/AppContext';
import { useNavigate, Link } from 'react-router-dom';
import client from '../api/client';
import PlantImageUploader from '../components/vision/PlantImageUploader';
import HealthScoreCard from '../components/vision/HealthScoreCard';
import DiseaseResultCard from '../components/vision/DiseaseResultCard';
import GrowthStageTimeline from '../components/vision/GrowthStageTimeline';
import RecommendationPanel from '../components/vision/RecommendationPanel';
import VisionHistory from '../components/vision/VisionHistory';
import { Lock, Settings, ShieldAlert, Image } from 'lucide-react';

function PlantHealthDashboard() {
  const { isAuthenticated, logout } = useContext(AppContext);
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [scans, setScans] = useState([]);
  const [selectedScan, setSelectedScan] = useState(null);
  const [selectedId, setSelectedId] = useState(null);

  const fetchHistory = async (autoSelectId = null) => {
    try {
      const res = await client.get('/api/vision/history');
      setScans(res.data);
      
      if (res.data.length > 0) {
        const idToSelect = autoSelectId || res.data[0].id;
        setSelectedId(idToSelect);
        fetchScanDetails(idToSelect);
      } else {
        setSelectedScan(null);
        setSelectedId(null);
      }
    } catch (err) {
      if (err.response?.status === 401) {
        logout();
        navigate('/login');
      } else {
        setError(err.message || 'Failed to retrieve scan history.');
      }
    } finally {
      setLoading(false);
    }
  };

  const fetchScanDetails = async (id) => {
    try {
      const res = await client.get(`/api/vision/${id}`);
      setSelectedScan(res.data);
    } catch (err) {
      console.error('Failed to load scan details', err);
    }
  };

  useEffect(() => {
    if (!isAuthenticated) {
      setLoading(false);
      return;
    }
    fetchHistory();
  }, [isAuthenticated]);

  const handleAnalysisComplete = (newAnalysis) => {
    fetchHistory(newAnalysis.id);
  };

  const handleSelectScan = (id) => {
    setSelectedId(id);
    fetchScanDetails(id);
  };

  if (!isAuthenticated) {
    return (
      <div className="max-w-md mx-auto my-16 p-8 glass-panel border border-slate-900 bg-slate-950/20 text-center space-y-6 rounded-3xl shadow-xl animate-fadeIn select-none">
        <div className="p-4 bg-amber-500/10 rounded-full border border-amber-500/20 text-amber-400 w-fit mx-auto">
          <Lock className="h-10 w-10 animate-pulse" />
        </div>
        <div className="space-y-2">
          <h2 className="text-lg font-black text-white uppercase tracking-wider">Vision System Locked</h2>
          <p className="text-slate-400 text-xs leading-relaxed font-medium">
            AI Computer Vision leaf diagnostics and plant pathology tools require account authentication. Sign in to scan crops.
          </p>
        </div>
        <div className="pt-2">
          <Link
            to="/login"
            className="w-full py-3 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-slate-950 font-bold block transition-all hover:shadow-lg active:scale-95"
          >
            Sign In
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-6 space-y-6 animate-fadeIn">
      <div className="border-b border-slate-900 pb-4">
        <h1 className="text-2xl font-black tracking-tight text-white uppercase">Plant Health Intelligence</h1>
        <p className="text-slate-400 text-[11px] mt-1">Multimodal AI computer vision diagnostics, leaf pathogen screening, and recovery tracking.</p>
      </div>

      {loading ? (
        <div className="py-24 text-center space-y-4">
          <Settings className="h-10 w-10 text-emerald-400 animate-spin mx-auto" />
          <p className="text-slate-500 text-xs font-semibold">Configuring crop diagnostic vision cameras...</p>
        </div>
      ) : error ? (
        <div className="p-4 rounded-xl border border-rose-500/10 bg-rose-500/5 text-rose-450 text-xs font-semibold flex items-center gap-2">
          <ShieldAlert className="h-4.5 w-4.5" />
          <span>Error: {error}</span>
        </div>
      ) : (
        <div className="grid md:grid-cols-3 gap-6">
          <div className="md:col-span-1 space-y-6">
            <PlantImageUploader onAnalysisComplete={handleAnalysisComplete} />
            <VisionHistory scans={scans} onSelectScan={handleSelectScan} selectedId={selectedId} />
          </div>

          <div className="md:col-span-2">
            {!selectedScan ? (
              <div className="h-full flex flex-col justify-center items-center p-12 text-center border-2 border-dashed border-slate-900 rounded-3xl bg-slate-950/20 py-24 space-y-4">
                <div className="p-4 bg-emerald-500/10 rounded-full border border-emerald-500/20 text-emerald-400">
                  <Image className="h-12 w-12 animate-pulse" />
                </div>
                <div className="max-w-sm space-y-2">
                  <h3 className="text-xs font-black uppercase text-white tracking-wider">Awaiting Leaf Telemetry</h3>
                  <p className="text-slate-400 text-[11px] leading-relaxed font-semibold">
                    Upload an active lettuce leaf photo to run disease analysis, calculate health metrics, and obtain AI copilot suggestions.
                  </p>
                </div>
              </div>
            ) : (
              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-6">
                  <HealthScoreCard score={selectedScan.health_score} />
                  <GrowthStageTimeline currentStage={selectedScan.growth_stage} />
                </div>
                <div className="space-y-6">
                  <DiseaseResultCard 
                    disease={selectedScan.disease} 
                    confidence={selectedScan.confidence} 
                    severity={selectedScan.severity} 
                  />
                  <RecommendationPanel recommendations={selectedScan.recommendations} />
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default PlantHealthDashboard;
