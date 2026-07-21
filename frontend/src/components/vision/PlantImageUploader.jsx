import React, { useState, useRef } from 'react';
import { plantDoctorApi } from '../../services/plantDoctorApi';
import { UploadCloud, ShieldAlert } from 'lucide-react';

function PlantImageUploader({ onAnalysisComplete }) {
  const [dragActive, setDragActive] = useState(false);
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState('');
  const inputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (selectedFile) => {
    setError('');
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (!validTypes.includes(selectedFile.type)) {
      setError('Invalid file type. Please upload a JPG, JPEG or PNG image.');
      return;
    }
    
    const maxSize = 5 * 1024 * 1024;
    if (selectedFile.size > maxSize) {
      setError('File is too large. Maximum allowed size is 5 MB.');
      return;
    }

    setFile(selectedFile);
    setPreviewUrl(URL.createObjectURL(selectedFile));
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setUploading(true);
    setProgress(20);
    setError('');

    try {
      setProgress(50);
      const data = await plantDoctorApi.analyzePlantCombined(file);
      setProgress(100);
      setTimeout(() => {
        setUploading(false);
        setFile(null);
        setPreviewUrl(null);
        if (onAnalysisComplete) onAnalysisComplete(data);
      }, 500);
    } catch (err) {
      const msg = (typeof err?.reason === 'string' && err.reason) ||
                  (typeof err?.detail === 'string' && err.detail) ||
                  (typeof err?.message === 'string' && err.message) ||
                  'Failed to analyze crop image.';
      setError(msg);
      setUploading(false);
    }
  };

  return (
    <div className="glass-panel p-6 rounded-3xl border border-slate-900 bg-slate-950/20 shadow-xl space-y-4">
      <div className="border-b border-slate-900 pb-3">
        <h4 className="text-xs font-black uppercase text-slate-400 tracking-wider">Crop Scan Uploader</h4>
        <p className="text-[10px] text-slate-500 font-semibold">Upload leaf photos to evaluate lettuce diseases and health indices</p>
      </div>

      <div 
        onDragEnter={handleDrag}
        onDragOver={handleDrag}
        onDragLeave={handleDrag}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        className={`border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all ${
          dragActive 
            ? 'border-emerald-500 bg-emerald-500/5' 
            : 'border-slate-900 hover:border-slate-800 hover:bg-slate-950/40'
        }`}
      >
        <input 
          ref={inputRef}
          type="file"
          accept=".jpg,.jpeg,.png"
          onChange={handleFileChange}
          className="hidden"
        />

        {previewUrl ? (
          <div className="space-y-3" onClick={(e) => e.stopPropagation()}>
            <img 
              src={previewUrl} 
              alt="Preview" 
              className="max-h-48 mx-auto rounded-xl border border-slate-900 object-cover shadow-lg"
            />
            <button
              onClick={() => { setFile(null); setPreviewUrl(null); }}
              className="text-[10px] text-rose-400 hover:underline font-bold uppercase"
            >
              Clear Selection
            </button>
          </div>
        ) : (
          <div className="space-y-2">
            <UploadCloud className="h-10 w-10 text-slate-500 mx-auto animate-pulse" />
            <p className="text-slate-300 text-xs font-bold">Drag and drop plant image here, or click to browse</p>
            <p className="text-slate-500 text-[10px] uppercase font-semibold tracking-wider">Supports JPG, JPEG, PNG (Max 5MB)</p>
          </div>
        )}
      </div>

      {error && (
        <div className="p-3 rounded-xl border border-rose-500/10 bg-rose-500/5 text-rose-450 text-[11px] font-semibold flex items-center gap-2">
          <ShieldAlert className="h-4.5 w-4.5" />
          <span>{error}</span>
        </div>
      )}

      {file && !uploading && (
        <button
          onClick={handleAnalyze}
          className="w-full py-3 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-slate-950 font-black uppercase tracking-wider rounded-xl transition-all shadow-lg active:scale-95 text-xs"
        >
          Begin Computer Vision Analysis
        </button>
      )}

      {uploading && (
        <div className="space-y-2">
          <div className="flex justify-between text-[10px] text-slate-400 font-bold uppercase">
            <span>Analyzing Image...</span>
            <span>{progress}%</span>
          </div>
          <div className="h-2 rounded-full bg-slate-900 border border-slate-850 overflow-hidden">
            <div 
              className="h-full bg-emerald-500 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default PlantImageUploader;
