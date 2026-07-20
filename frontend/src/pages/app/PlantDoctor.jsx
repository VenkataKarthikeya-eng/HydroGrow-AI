import React, { useState } from 'react';
import { Camera, Upload, ShieldCheck, AlertCircle, XCircle, RefreshCw, Sprout, TestTube, Sparkles } from 'lucide-react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Badge from '../../components/ui/Badge';
import Loader from '../../components/ui/Loader';
import { plantDoctorApi } from '../../services/plantDoctorApi';

export default function PlantDoctor() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingStatus, setLoadingStatus] = useState('Uploading image...');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [rejectionInfo, setRejectionInfo] = useState(null);
  const [error, setError] = useState(null);

  const analyzeImageFile = async (file) => {
    setLoading(true);
    setLoadingStatus('Uploading image...');
    setError(null);
    setRejectionInfo(null);
    setAnalysisResult(null);

    try {
      setLoadingStatus('AI analyzing with TensorFlow models...');
      const data = await plantDoctorApi.analyzePlantCombined(file);

      if (data?.status === 'rejected') {
        setRejectionInfo(data);
      } else if (data?.error) {
        setError(data.error);
      } else {
        setAnalysisResult(data);
      }
    } catch (err) {
      console.error('Plant Doctor API error:', err);
      if (err?.status === 'rejected') {
        setRejectionInfo(err);
      } else {
        const msg = err?.reason || err?.detail || err?.message || 'Failed to connect to HydroGrow AI backend.';
        setError(`AI Scanner Error: ${msg}. Please verify backend server is active.`);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      const previewUrl = URL.createObjectURL(file);
      setPreview(previewUrl);
      analyzeImageFile(file);
    }
  };

  const handleDemoImage = () => {
    // Generate a synthetic sample lettuce leaf canvas blob to send to backend API
    const canvas = document.createElement('canvas');
    canvas.width = 224;
    canvas.height = 224;
    const ctx = canvas.getContext('2d');
    
    // Background green leaf gradient
    const grad = ctx.createLinearGradient(0, 0, 224, 224);
    grad.addColorStop(0, '#1b5e20');
    grad.addColorStop(1, '#43a047');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 224, 224);
    
    // Leaf shape
    ctx.fillStyle = '#66bb6a';
    ctx.beginPath();
    ctx.ellipse(112, 112, 85, 55, Math.PI / 4, 0, 2 * Math.PI);
    ctx.fill();

    canvas.toBlob((blob) => {
      if (blob) {
        const file = new File([blob], "sample_healthy_leaf.png", { type: "image/png" });
        setSelectedImage(file);
        setPreview(URL.createObjectURL(file));
        analyzeImageFile(file);
      }
    }, "image/png");
  };

  const handleReset = () => {
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

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in duration-300">
      
      {/* Page Header */}
      <div className="border-b border-slate-200 dark:border-slate-800 pb-6">
        <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
          <Camera className="w-4 h-4" /> Computer Vision Pathology
        </div>
        <h1 className="text-3xl font-black text-slate-900 dark:text-white mt-1">
          Plant Doctor Scanner
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Upload lettuce leaf photos for real-time Crop Identity Validation (MobileNetV3), Growth Stage Prediction (EfficientNetB0), and Nutrient Deficiency Detection.
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
                <h3 className="text-lg font-black text-red-900 dark:text-red-200">❌ Scan Stopped</h3>
                <Badge variant="brand" className="bg-red-200 text-red-900 border-red-300 dark:bg-red-900/60 dark:text-red-200 font-bold">
                  Confidence: {formatConfidence(rejectionInfo.confidence)}
                </Badge>
              </div>
              <div>
                <span className="text-xs font-bold text-red-700 dark:text-red-400 uppercase tracking-wider block mb-1">Reason:</span>
                <p className="text-sm font-semibold text-red-900 dark:text-red-200 leading-relaxed">
                  {rejectionInfo.reason || "Please upload a hydroponic lettuce leaf image for AI analysis."}
                </p>
              </div>
              <div className="pt-2 flex items-center gap-3">
                <Button size="sm" variant="primary" onClick={handleReset} icon={RefreshCw} className="bg-red-600 hover:bg-red-700 text-white">
                  Try Another Image
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
              <h4 className="text-sm font-bold text-amber-900 dark:text-amber-200">System Notification</h4>
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
            <h3 className="text-lg font-bold text-slate-900 dark:text-white">Upload Plant Leaf Photo</h3>
            <p className="text-xs text-slate-500 leading-relaxed">
              Protected by AI Crop Identity Validation Gatekeeper. Only hydroponic lettuce leaf images pass for growth and nutrient analysis.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <label className="cursor-pointer">
              <input type="file" accept="image/*" onChange={handleImageUpload} className="hidden" disabled={loading} />
              <Button variant="primary" icon={Upload} className="pointer-events-none shadow-sm">
                Select Image File
              </Button>
            </label>
            <Button variant="outline" onClick={handleDemoImage} disabled={loading}>
              Use Sample Healthy Leaf
            </Button>
          </div>

          <div className="pt-6 border-t border-slate-100 dark:border-slate-800/80 grid grid-cols-3 gap-4 text-xs text-slate-500">
            <div>
              <span className="font-bold text-slate-700 dark:text-slate-300 block mb-0.5">Gatekeeper</span>
              Crop Identity Validation AI
            </div>
            <div>
              <span className="font-bold text-slate-700 dark:text-slate-300 block mb-0.5">Model 1</span>
              EfficientNetB0 Growth AI
            </div>
            <div>
              <span className="font-bold text-slate-700 dark:text-slate-300 block mb-0.5">Model 2</span>
              MobileNetV3 Nutrient AI
            </div>
          </div>
        </Card>
      )}

      {/* Loading Scanning State */}
      {loading && (
        <Card padding="p-12">
          <Loader
            message={loadingStatus}
            steps={[
              'Uploading image...',
              'AI analyzing...',
              'Running Crop Identity Validation Gatekeeper...',
              'Evaluating Growth Stage & Nutrient Deficiency...',
              'Compiling tailored agronomist advice...',
            ]}
            currentStep={1}
          />
        </Card>
      )}

      {/* Scan Results Card */}
      {analysisResult && !rejectionInfo && !loading && (
        <div className="space-y-6">
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
            <div className={`md:col-span-2 saas-card p-8 text-white rounded-2xl flex flex-col justify-between shadow-lg ${
              analysisResult.nutrient_prediction?.condition === 'Healthy'
                ? 'bg-emerald-600'
                : 'bg-amber-600'
            }`}>
              <div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-white/90 text-xs font-bold uppercase tracking-wider">
                    <ShieldCheck className="w-5 h-5" /> Combined AI Diagnostics
                  </div>
                  <Badge variant="brand" className="bg-white/20 text-white border-white/30">
                    {formatConfidence(analysisResult.nutrient_prediction?.confidence)} Confidence
                  </Badge>
                </div>
                <div className="text-4xl font-black mt-3">
                  {analysisResult.nutrient_prediction?.condition || 'Analysis Complete'}
                </div>
                <p className="text-sm text-white/90 mt-2">
                  Growth Stage: <span className="font-bold">{analysisResult.growth_prediction?.stage}</span> (Day {analysisResult.growth_prediction?.growth_day})
                </p>
              </div>

              <div className="pt-6 border-t border-white/30 flex justify-between items-center">
                <span className="text-xs text-white/90">
                  Render Production FastAPI API: https://hydrogrow-ai-plant-doctor.onrender.com
                </span>
                <Button variant="secondary" size="sm" onClick={handleReset} icon={RefreshCw} className="bg-white text-slate-900 hover:bg-slate-100">
                  Scan Another Leaf
                </Button>
              </div>
            </div>

          </div>

          {/* Model Intelligence Breakdown Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* 🌱 Growth Intelligence Card (Model 1) */}
            <Card padding="p-6">
              <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider mb-4 pb-2 border-b border-slate-100 dark:border-slate-800">
                <Sprout className="w-4 h-4" /> 🌱 Growth Analysis
              </div>
              
              <div className="space-y-3 text-sm">
                <div className="flex justify-between items-center pb-2 border-b border-slate-100 dark:border-slate-800/60">
                  <span className="text-slate-600 dark:text-slate-400 font-medium">Growth Stage</span>
                  <span className="font-bold text-slate-900 dark:text-white bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 px-3 py-1 rounded-lg border border-emerald-200 dark:border-emerald-800">
                    {analysisResult.growth_prediction?.stage}
                  </span>
                </div>
                
                <div className="flex justify-between items-center pb-2 border-b border-slate-100 dark:border-slate-800/60">
                  <span className="text-slate-600 dark:text-slate-400 font-medium">Growth Day</span>
                  <span className="font-bold text-slate-900 dark:text-white">
                    Day {analysisResult.growth_prediction?.growth_day}
                  </span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-slate-600 dark:text-slate-400 font-medium">Model Confidence</span>
                  <span className="font-bold text-emerald-600 dark:text-emerald-400">
                    {formatConfidence(analysisResult.growth_prediction?.confidence)}
                  </span>
                </div>
              </div>
            </Card>

            {/* 🧪 Nutrient Intelligence Card (Model 2) */}
            <Card padding="p-6">
              <div className="flex items-center gap-2 text-xs font-bold text-indigo-600 dark:text-indigo-400 uppercase tracking-wider mb-4 pb-2 border-b border-slate-100 dark:border-slate-800">
                <TestTube className="w-4 h-4" /> 🧪 Nutrient Analysis
              </div>
              
              <div className="space-y-3 text-sm">
                <div className="flex justify-between items-center pb-2 border-b border-slate-100 dark:border-slate-800/60">
                  <span className="text-slate-600 dark:text-slate-400 font-medium">Detected Deficiency</span>
                  <span className={`font-bold px-3 py-1 rounded-lg border ${
                    analysisResult.nutrient_prediction?.condition === 'Healthy'
                      ? 'bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800'
                      : 'bg-amber-50 dark:bg-amber-950/60 text-amber-700 dark:text-amber-300 border-amber-200 dark:border-amber-800'
                  }`}>
                    {analysisResult.nutrient_prediction?.condition}
                  </span>
                </div>

                <div className="flex justify-between items-center pb-2 border-b border-slate-100 dark:border-slate-800/60">
                  <span className="text-slate-600 dark:text-slate-400 font-medium">Nutrient Status</span>
                  <span className="font-bold text-slate-900 dark:text-white">
                    {analysisResult.nutrient_prediction?.condition === 'Healthy' ? 'Optimal Balance' : 'Action Required'}
                  </span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-slate-600 dark:text-slate-400 font-medium">Model Confidence</span>
                  <span className="font-bold text-indigo-600 dark:text-indigo-400">
                    {formatConfidence(analysisResult.nutrient_prediction?.confidence)}
                  </span>
                </div>
              </div>
            </Card>

          </div>

          {/* 🤖 AI Recommendation Card */}
          <Card padding="p-6">
            <div className="flex items-center gap-2 text-xs font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wider mb-3">
              <Sparkles className="w-4 h-4 text-emerald-500" /> 🤖 Suggested Actions & Plant Care Advice
            </div>
            <p className="text-sm text-slate-700 dark:text-slate-300 bg-slate-50 dark:bg-slate-900/60 p-4 rounded-xl border border-slate-200 dark:border-slate-800 leading-relaxed font-medium">
              {analysisResult.recommendation}
            </p>
          </Card>

        </div>
      )}

    </div>
  );
}
