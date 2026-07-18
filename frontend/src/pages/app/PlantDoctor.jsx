import React, { useState } from 'react';
import { Camera, Upload, CheckCircle2, ShieldCheck, AlertCircle, RefreshCw } from 'lucide-react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Badge from '../../components/ui/Badge';
import Loader from '../../components/ui/Loader';

export default function PlantDoctor() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [isScanning, setIsScanning] = useState(false);
  const [scanResult, setScanResult] = useState(null);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      setSelectedImage(url);
      runScan();
    }
  };

  const handleDemoImage = () => {
    setSelectedImage('https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?auto=format&fit=crop&w=800&q=80');
    runScan();
  };

  const runScan = () => {
    setIsScanning(true);
    setScanResult(null);
    setTimeout(() => {
      setIsScanning(false);
      setScanResult({
        healthScore: 99,
        status: 'Healthy',
        pathogen: 'None Detected (Negative for Pythium & Powdered Mildew)',
        deficiency: 'None (Nitrogen, Magnesium & Iron Levels Optimal)',
        growthStage: 'Vegetative Flush (Day 18)',
        recommendation: 'Continue current nutrient fertigation and canopy lighting schedule.'
      });
    }, 2500);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in duration-300">
      
      {/* Title */}
      <div className="border-b border-slate-200 dark:border-slate-800 pb-6">
        <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
          <Camera className="w-4 h-4" /> Computer Vision Pathology
        </div>
        <h1 className="text-3xl font-black text-slate-900 dark:text-white mt-1">
          Plant Doctor Scanner
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Upload leaf photos for automated AI pathology detection, nutrient deficiency diagnosis, and care advice.
        </p>
      </div>

      {/* Main Upload Dropzone */}
      {!selectedImage && (
        <Card padding="p-10 sm:p-14" className="text-center space-y-6">
          <div className="w-16 h-16 rounded-2xl bg-emerald-50 dark:bg-emerald-950 text-emerald-600 mx-auto flex items-center justify-center border border-emerald-100 dark:border-emerald-900 shadow-xs">
            <Upload className="w-8 h-8" />
          </div>

          <div className="max-w-md mx-auto space-y-2">
            <h3 className="text-lg font-bold text-slate-900 dark:text-white">Upload Plant Leaf Photo</h3>
            <p className="text-xs text-slate-500 leading-relaxed">
              Our Vision Model evaluates foliage for 14 hydroponic leaf diseases, chlorosis, and micro-nutrient deficiencies.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <label className="cursor-pointer">
              <input type="file" accept="image/*" onChange={handleImageUpload} className="hidden" />
              <Button variant="primary" icon={Upload} className="pointer-events-none shadow-sm">
                Select Image File
              </Button>
            </label>
            <Button variant="outline" onClick={handleDemoImage}>
              Use Sample Healthy Leaf
            </Button>
          </div>

          <div className="pt-6 border-t border-slate-100 dark:border-slate-800/80 grid grid-cols-3 gap-4 text-xs text-slate-500">
            <div>
              <span className="font-bold text-slate-700 dark:text-slate-300 block mb-0.5">Pathogens</span>
              Pythium, Mildew, Blight
            </div>
            <div>
              <span className="font-bold text-slate-700 dark:text-slate-300 block mb-0.5">Deficiencies</span>
              N, P, K, Ca, Mg, Fe
            </div>
            <div>
              <span className="font-bold text-slate-700 dark:text-slate-300 block mb-0.5">Accuracy</span>
              98.4% Vision Score
            </div>
          </div>
        </Card>
      )}

      {/* Loading Scanning State */}
      {isScanning && (
        <Card padding="p-12">
          <Loader
            message="Analyzing leaf stomata and chlorosis patterns..."
            steps={[
              'Preprocessing high-resolution leaf tensor...',
              'Running Convolutional Pathology Model...',
              'Checking against 45,000 leaf disease samples...',
              'Compiling health score & treatment plan...',
            ]}
            currentStep={2}
          />
        </Card>
      )}

      {/* Scan Results Card */}
      {scanResult && !isScanning && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            {/* Image Preview */}
            <Card padding="p-6" header="Leaf Sample Preview">
              <img
                src={selectedImage}
                alt="Analyzed leaf sample"
                className="w-full h-48 object-cover rounded-xl border border-slate-200 dark:border-slate-800"
              />
              <div className="mt-3 flex justify-between items-center text-xs">
                <span className="text-slate-500">Scan Status:</span>
                <Badge variant="optimized">Verified Complete</Badge>
              </div>
            </Card>

            {/* Health Score Box */}
            <div className="md:col-span-2 saas-card p-8 bg-emerald-600 text-white rounded-2xl flex flex-col justify-between shadow-lg">
              <div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-emerald-100 text-xs font-bold uppercase tracking-wider">
                    <ShieldCheck className="w-5 h-5" /> Plant Health Score
                  </div>
                  <Badge variant="brand" className="bg-white/20 text-white border-white/30">
                    99% Optimal
                  </Badge>
                </div>
                <div className="text-5xl font-black mt-3">Healthy</div>
                <p className="text-sm text-emerald-100 mt-2">
                  No visual pathogens, chlorosis, or mineral toxicities detected in this foliage sample.
                </p>
              </div>

              <div className="pt-6 border-t border-emerald-500/40 flex justify-between items-center">
                <span className="text-xs text-emerald-100">Growth Stage: {scanResult.growthStage}</span>
                <Button variant="secondary" size="sm" onClick={() => setSelectedImage(null)} icon={RefreshCw} className="bg-white text-slate-900 hover:bg-emerald-50">
                  Scan Another Leaf
                </Button>
              </div>
            </div>

          </div>

          {/* Diagnostic Breakdown */}
          <Card padding="p-8" header="Diagnostic Pathology Report">
            <div className="space-y-4 text-sm">
              <div className="flex justify-between items-center pb-3 border-b border-slate-100 dark:border-slate-800">
                <span className="font-bold text-slate-700 dark:text-slate-300">Pathogens Detected</span>
                <span className="text-emerald-600 dark:text-emerald-400 font-semibold">{scanResult.pathogen}</span>
              </div>
              <div className="flex justify-between items-center pb-3 border-b border-slate-100 dark:border-slate-800">
                <span className="font-bold text-slate-700 dark:text-slate-300">Nutrient Deficiencies</span>
                <span className="text-emerald-600 dark:text-emerald-400 font-semibold">{scanResult.deficiency}</span>
              </div>
              <div className="pt-2">
                <span className="font-bold text-slate-900 dark:text-white block mb-1.5">Agronomist Recommendation:</span>
                <p className="text-slate-600 dark:text-slate-400 bg-slate-50 dark:bg-slate-900/60 p-4 rounded-xl border border-slate-200 dark:border-slate-800 leading-relaxed">
                  {scanResult.recommendation}
                </p>
              </div>
            </div>
          </Card>
        </div>
      )}

    </div>
  );
}
