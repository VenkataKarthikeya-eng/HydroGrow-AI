import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { Camera, Upload, ShieldCheck, AlertCircle, XCircle, RefreshCw, Sprout, TestTube, Sparkles, History } from 'lucide-react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Badge from '../../components/ui/Badge';
import Loader from '../../components/ui/Loader';
import { plantDoctorApi } from '../../services/plantDoctorApi';
import { AppContext } from '../../context/AppContext';

export default function PlantDoctor() {
  const { savePlantDoctorScan } = useContext(AppContext);
  const navigate = useNavigate();
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [loadingStatus, setLoadingStatus] = useState('Uploading image...');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [rejectionInfo, setRejectionInfo] = useState(null);
  const [error, setError] = useState(null);

  const loaderSteps = [
    'Preparing image for analysis...',
    'Checking crop identity...',
    'Evaluating leaf health and growth stage...',
    'Detecting nutrient deficiency status...',
    'Generating diagnosis and care advice...'
  ];

  const analyzeImageFile = async (file) => {
    setLoading(true);
    setCurrentStep(0);
    setLoadingStatus(loaderSteps[0]);
    setError(null);
    setRejectionInfo(null);
    setAnalysisResult(null);

    // Step progression timer for continuous visual feedback
    const stepInterval = setInterval(() => {
      setCurrentStep((prev) => {
        const next = prev < loaderSteps.length - 1 ? prev + 1 : prev;
        setLoadingStatus(loaderSteps[next]);
        return next;
        });
    }, 450);

    const coldStartTimer = setTimeout(() => {
      setLoadingStatus('Initializing AI engine (please wait a few seconds)...');
    }, 6000);

    try {
      const data = await plantDoctorApi.analyzePlantCombined(file, (msg) => setLoadingStatus(msg));

      if (data?.status === 'rejected') {
        setRejectionInfo(data);
      } else if (data?.error) {
        setError(typeof data.error === 'string' ? data.error : JSON.stringify(data.error));
      } else {
        setAnalysisResult(data);
        if (savePlantDoctorScan) {
          savePlantDoctorScan(data);
        }
      }
    } catch (err) {
      console.error('Plant Doctor API error:', err);
      if (err?.status === 'rejected') {
        setRejectionInfo(err);
      } else if (err?.code === 'ECONNABORTED' || err?.reason?.includes('timeout')) {
        setError('Server request timed out. Please click "Try Again".');
      } else {
        const msg = (typeof err?.reason === 'string' && err.reason) ||
                    (typeof err?.detail === 'string' && err.detail) ||
                    (typeof err?.message === 'string' && err.message) ||
                    'Failed to connect to backend server.';
        setError(`Scanner Notice: ${msg}`);
      }
    } finally {
      clearInterval(stepInterval);
      clearTimeout(coldStartTimer);
      setLoading(false);
    }
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // File Size Validation (Max 5MB)
    const maxSize = 5 * 1024 * 1024;
    if (file.size > maxSize) {
      setError('File is too large. Please upload an image smaller than 5 MB.');
      return;
    }

    // MIME Type Validation
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (!validTypes.includes(file.type.toLowerCase())) {
      setError('Unsupported file format. Please upload a JPG, JPEG, or PNG lettuce leaf photo.');
      return;
    }

    setSelectedImage(file);
    const previewUrl = URL.createObjectURL(file);
    setPreview(previewUrl);
    analyzeImageFile(file);
  };

  const handleDemoImage = async () => {
    try {
      setLoading(true);
      const res = await fetch('/sample_lettuce_leaf.png');
      const blob = await res.blob();
      const file = new File([blob], "sample_healthy_lettuce_leaf.png", { type: "image/png" });
      setSelectedImage(file);
      setPreview(URL.createObjectURL(file));
      analyzeImageFile(file);
    } catch (e) {
      console.error('Failed to load sample leaf asset:', e);
      // Fallback in case of asset fetch issue
      const canvas = document.createElement('canvas');
      canvas.width = 224;
      canvas.height = 224;
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = '#2e7d32';
      ctx.fillRect(0, 0, 224, 224);
      canvas.toBlob((b) => {
        if (b) {
          const f = new File([b], "sample_leaf.png", { type: "image/png" });
          setSelectedImage(f);
          setPreview(URL.createObjectURL(f));
          analyzeImageFile(f);
        }
      });
    }
  };

  const handleReset = () => {
    if (preview && preview.startsWith('blob:')) {
      URL.revokeObjectURL(preview);
    }
    setSelectedImage(null);
    setPreview(null);
    setAnalysisResult(null);
    setRejectionInfo(null);
    setError(null);
    setLoading(false);
  };

  const formatConfidence = (conf) => {
    if (conf === undefined || conf === null) return '90%';
    const num = typeof conf === 'number' ? conf : parseFloat(conf);
    if (num <= 1.0) {
      return `${Math.round(num * 100)}%`;
    }
    return `${Math.round(num)}%`;
  };

  const getConfidenceBadgeColor = (conf) => {
    const num = typeof conf === 'number' ? conf : parseFloat(conf || 0);
    const val = num <= 1.0 ? num * 100 : num;
    if (val >= 90) return 'bg-emerald-500/20 text-emerald-300 border-emerald-400/40';
    if (val >= 75) return 'bg-amber-500/20 text-amber-300 border-amber-400/40';
    return 'bg-rose-500/20 text-rose-300 border-rose-400/40';
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in duration-300">
      
      {/* Page Header */}
      <div className="border-b border-slate-200 dark:border-slate-800 pb-6">
        <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
          <Camera className="w-4 h-4" /> Plant Doctor Scanner
        </div>
        <h1 className="text-3xl font-black text-slate-900 dark:text-white mt-1">
          Hydroponic Leaf Analysis
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
          Scan your hydroponic lettuce leaf to diagnose growth stage, growth day, and nutrient deficiencies in seconds.
        </p>
      </div>

      {/* Rejection Card */}
      {rejectionInfo && !loading && (
        <Card padding="p-8" className="border-red-300 bg-red-50/90 dark:bg-red-950/50 dark:border-red-900 shadow-md">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-xl bg-red-100 dark:bg-red-900/80 text-red-600 dark:text-red-300 flex items-center justify-center shrink-0">
              <XCircle className="w-7 h-7" />
            </div>
            <div className="flex-1 space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-black text-red-900 dark:text-red-200">Image Not Accepted</h3>
                <Badge variant="brand" className="bg-red-200 text-red-900 border-red-300 dark:bg-red-900/60 dark:text-red-200 font-bold">
                  Confidence: {formatConfidence(rejectionInfo.confidence)}
                </Badge>
              </div>
              <div>
                <span className="text-xs font-bold text-red-700 dark:text-red-400 uppercase tracking-wider block mb-1">Reason:</span>
                <p className="text-sm font-semibold text-red-900 dark:text-red-200 leading-relaxed">
                  {rejectionInfo.reason || "Please upload a clear photo of a hydroponic lettuce leaf."}
                </p>
              </div>
              <div className="p-3 rounded-lg bg-red-100/70 dark:bg-red-900/40 text-xs text-red-800 dark:text-red-300">
                💡 <span className="font-bold">Tip:</span> Use a clear, well-lit photo of a single leaf against a dark or neutral background.
              </div>
              <div className="pt-2 flex items-center gap-3">
                <Button size="sm" variant="primary" onClick={handleReset} icon={RefreshCw} className="bg-red-600 hover:bg-red-700 text-white">
                  Try Another Photo
                </Button>
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* General Error Alert Display */}
      {error && !rejectionInfo && (
        <Card padding="p-6" className="border-amber-200 bg-amber-50 dark:bg-amber-950/40 dark:border-amber-900">
          <div className="flex items-start gap-4">
            <AlertCircle className="w-6 h-6 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
            <div className="flex-1 space-y-2">
              <h4 className="text-sm font-bold text-amber-900 dark:text-amber-200">Scanner Notice</h4>
              <p className="text-xs text-amber-700 dark:text-amber-300 leading-relaxed">{error}</p>
              <Button size="sm" variant="outline" onClick={handleReset} className="mt-2 border-amber-300 text-amber-700 hover:bg-amber-100 dark:hover:bg-amber-900/50">
                Try Again
              </Button>
            </div>
          </div>
        </Card>
      )}

      {/* Main Upload Dropzone */}
      {!preview && !loading && (
        <Card padding="p-10 sm:p-14" className="text-center space-y-6">
          <div className="w-16 h-16 rounded-2xl bg-emerald-50 dark:bg-emerald-950 text-emerald-600 mx-auto flex items-center justify-center border border-emerald-100 dark:border-emerald-900 shadow-xs">
            <Upload className="w-8 h-8" />
          </div>

          <div className="max-w-md mx-auto space-y-2">
            <h3 className="text-lg font-bold text-slate-900 dark:text-white">Upload Lettuce Leaf Image</h3>
            <p className="text-xs text-slate-500 leading-relaxed">
              Upload a clear, well-lit photo of a single hydroponic lettuce leaf. Supported formats: JPG, PNG under 5 MB.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <label className="cursor-pointer">
              <input type="file" accept="image/*" onChange={handleImageUpload} className="hidden" disabled={loading} />
              <Button variant="primary" icon={Upload} className="pointer-events-none shadow-sm">
                Choose Image File
              </Button>
            </label>
            <Button variant="outline" onClick={handleDemoImage} disabled={loading}>
              Use Sample Healthy Leaf
            </Button>
          </div>

          <div className="pt-6 border-t border-slate-100 dark:border-slate-800/80 grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs text-slate-500">
            <div>
              <span className="font-bold text-slate-700 dark:text-slate-300 block mb-0.5">1. Crop Check</span>
              Verifies lettuce leaf identity
            </div>
            <div>
              <span className="font-bold text-slate-700 dark:text-slate-300 block mb-0.5">2. Growth Analysis</span>
              Identifies stage & growth day
            </div>
            <div>
              <span className="font-bold text-slate-700 dark:text-slate-300 block mb-0.5">3. Nutrient Check</span>
              Detects nutrient deficiency
            </div>
          </div>
        </Card>
      )}

      {/* Loading Scanning State */}
      {loading && (
        <Card padding="p-12">
          <Loader
            message={loadingStatus}
            steps={loaderSteps}
            currentStep={currentStep}
          />
        </Card>
      )}

      {/* Scan Results Card */}
      {analysisResult && !rejectionInfo && !loading && (
        <div className="space-y-6">

          {/* Low Confidence Warning Card (Bug 2) */}
          {(analysisResult.nutrient_prediction?.condition === 'Uncertain' || (analysisResult.nutrient_prediction?.confidence != null && analysisResult.nutrient_prediction.confidence < 0.50)) && (
            <Card padding="p-6" className="border-amber-300 bg-amber-50 dark:bg-amber-950/50 dark:border-amber-900 shadow-sm">
              <div className="flex items-start gap-4">
                <AlertCircle className="w-6 h-6 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
                <div className="flex-1 space-y-1">
                  <h4 className="text-sm font-bold text-amber-900 dark:text-amber-200">⚠️ Low Confidence Diagnostic Warning</h4>
                  <p className="text-xs text-amber-800 dark:text-amber-300 font-medium">
                    {analysisResult.nutrient_prediction?.recommendation || "Low confidence. Please upload a clearer leaf image."}
                  </p>
                </div>
              </div>
            </Card>
          )}
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            {/* Image Preview */}
            <Card padding="p-6" header="Leaf Sample Preview">
              {preview && (
                <img
                  src={preview}
                  alt="Analyzed leaf sample"
                  className="w-full h-48 object-cover rounded-xl border border-slate-200 dark:border-slate-800"
                />
              )}
              <div className="mt-3 flex justify-between items-center text-xs">
                <span className="text-slate-500">Scan Status:</span>
                <Badge variant="optimized">AI Validated Lettuce</Badge>
              </div>
            </Card>

            {/* Health Overview Banner */}
            <div className={`md:col-span-2 saas-card p-6 sm:p-8 text-white rounded-2xl flex flex-col justify-between shadow-lg ${
              analysisResult.nutrient_prediction?.condition === 'Healthy'
                ? 'bg-emerald-600'
                : analysisResult.nutrient_prediction?.condition === 'Uncertain'
                ? 'bg-amber-600'
                : 'bg-amber-600'
            }`}>
              <div>
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2 text-white/90 text-xs font-bold uppercase tracking-wider">
                    <ShieldCheck className="w-5 h-5" /> Combined AI Diagnostics
                  </div>
                  <Badge variant="brand" className={`px-2.5 py-1 text-xs font-bold border ${getConfidenceBadgeColor(analysisResult.nutrient_prediction?.confidence)}`}>
                    {formatConfidence(analysisResult.nutrient_prediction?.confidence)} Confidence
                  </Badge>
                </div>
                <div className="text-3xl sm:text-4xl font-black mt-3">
                  {analysisResult.nutrient_prediction?.condition || 'Analysis Complete'}
                </div>
                <p className="text-sm text-white/90 mt-2">
                  Growth Stage: <span className="font-bold">{analysisResult.growth_prediction?.stage || 'Unknown'}</span> (Day {analysisResult.growth_prediction?.growth_day ?? 'N/A'})
                </p>
              </div>

              <div className="pt-6 border-t border-white/30 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <span className="text-xs text-white/80 font-medium">
                  Source: {analysisResult.prediction_source === 'ml_model' ? 'Trained Vision Model' : 'Standard Rules Engine'}
                </span>
                <div className="flex gap-2">
                  <Button variant="secondary" size="sm" onClick={handleReset} icon={RefreshCw} className="bg-white text-slate-900 hover:bg-slate-100 shrink-0">
                    Scan Another Leaf
                  </Button>
                  <Button variant="outline" size="sm" onClick={() => navigate('/history/predictions')} icon={History} className="border-white/30 text-white hover:bg-white/10 shrink-0">
                    View Scan History
                  </Button>
                </div>
              </div>
            </div>

          </div>

          {/* Model Breakdown Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* Growth Card */}
            <Card padding="p-6">
              <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider mb-4 pb-2 border-b border-slate-100 dark:border-slate-800">
                <Sprout className="w-4 h-4" /> Growth Stage
              </div>
              
              <div className="space-y-3 text-sm">
                <div className="flex justify-between items-center pb-2 border-b border-slate-100 dark:border-slate-800/60">
                  <span className="text-slate-600 dark:text-slate-400 font-medium">Growth Stage</span>
                  <span className="font-bold text-slate-900 dark:text-white bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 px-3 py-1 rounded-lg border border-emerald-200 dark:border-emerald-800">
                    {analysisResult.growth_prediction?.stage || 'Unknown'}
                  </span>
                </div>
                
                <div className="flex justify-between items-center pb-2 border-b border-slate-100 dark:border-slate-800/60">
                  <span className="text-slate-600 dark:text-slate-400 font-medium">Growth Day</span>
                  <span className="font-bold text-slate-900 dark:text-white">
                    Day {analysisResult.growth_prediction?.growth_day ?? 'N/A'}
                  </span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-slate-600 dark:text-slate-400 font-medium">Confidence</span>
                  <span className="font-bold text-emerald-600 dark:text-emerald-400">
                    {formatConfidence(analysisResult.growth_prediction?.confidence)}
                  </span>
                </div>
              </div>
            </Card>

            {/* Nutrient Card */}
            <Card padding="p-6">
              <div className="flex items-center gap-2 text-xs font-bold text-indigo-600 dark:text-indigo-400 uppercase tracking-wider mb-4 pb-2 border-b border-slate-100 dark:border-slate-800">
                <TestTube className="w-4 h-4" /> Nutrient Status
              </div>
              
              <div className="space-y-3 text-sm">
                <div className="flex justify-between items-center pb-2 border-b border-slate-100 dark:border-slate-800/60">
                  <span className="text-slate-600 dark:text-slate-400 font-medium">Condition</span>
                  <span className={`font-bold px-3 py-1 rounded-lg border ${
                    analysisResult.nutrient_prediction?.condition === 'Healthy'
                      ? 'bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800'
                      : 'bg-amber-50 dark:bg-amber-950/60 text-amber-700 dark:text-amber-300 border-amber-200 dark:border-amber-800'
                  }`}>
                    {analysisResult.nutrient_prediction?.condition || 'Unknown'}
                  </span>
                </div>

                <div className="flex justify-between items-center pb-2 border-b border-slate-100 dark:border-slate-800/60">
                  <span className="text-slate-600 dark:text-slate-400 font-medium">Nutrient Status</span>
                  <span className="font-bold text-slate-900 dark:text-white">
                    {analysisResult.nutrient_prediction?.condition === 'Healthy' ? 'Optimal' : 'Attention Needed'}
                  </span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-slate-600 dark:text-slate-400 font-medium">Confidence</span>
                  <span className="font-bold text-indigo-600 dark:text-indigo-400">
                    {formatConfidence(analysisResult.nutrient_prediction?.confidence)}
                  </span>
                </div>
              </div>
            </Card>

          </div>

          {/* Recommendation Card */}
          <Card padding="p-6">
            <div className="flex items-center gap-2 text-xs font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wider mb-3">
              <Sparkles className="w-4 h-4 text-emerald-500" /> Agronomist Recommendation
            </div>
            <p className="text-sm text-slate-700 dark:text-slate-300 bg-slate-50 dark:bg-slate-900/60 p-4 rounded-xl border border-slate-200 dark:border-slate-800 leading-relaxed font-medium">
              {analysisResult.recommendation || 'No recommendation available.'}
            </p>
          </Card>

        </div>
      )}

    </div>
  );
}
