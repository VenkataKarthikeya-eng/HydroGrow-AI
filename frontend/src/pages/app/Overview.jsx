import React, { useContext, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Sprout, Sparkles, Camera, Cpu, Activity, ArrowRight, 
  CheckCircle2, ChevronRight, ChevronLeft, Bell, Sliders, 
  BookOpen, AlertCircle, FileText, Compass, Flame
} from 'lucide-react';
import { AppContext } from '../../context/AppContext';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Badge from '../../components/ui/Badge';

export default function Overview() {
  const { user, predictionResult } = useContext(AppContext);
  const navigate = useNavigate();

  // Carousel Slider State
  const [currentSlide, setCurrentSlide] = useState(0);

  const carouselCards = [
    {
      id: 1,
      tag: 'Featured ML Tool',
      title: 'AI Crop Yield Wizard',
      subtitle: '3-Step ML Yield Prediction Engine',
      description: 'Configure climate, water, and seedling metrics to forecast harvest weight with 91% confidence.',
      badge: 'Most Popular',
      gradient: 'from-emerald-600 via-teal-600 to-emerald-700',
      actionText: 'Start Analysis',
      link: '/prediction',
      image: '📊'
    },
    {
      id: 2,
      tag: 'Computer Vision',
      title: 'Plant Doctor Pathology Scanner',
      subtitle: 'Leaf Disease & Chlorosis Diagnostics',
      description: 'Upload leaf imagery to detect early-stage pathogens, Pythium, and micro-nutrient deficiencies.',
      badge: '98.4% Vision Score',
      gradient: 'from-teal-600 via-cyan-600 to-emerald-700',
      actionText: 'Scan Plant Leaf',
      link: '/plant-doctor',
      image: '🩺'
    },
    {
      id: 3,
      tag: 'Digital Twin',
      title: 'Crop Simulation Lab',
      subtitle: 'Virtual Growth Curve Simulator',
      description: 'Experiment with temperature, humidity, and EC sliders to project 30-day crop trajectories.',
      badge: '+18% Yield Gain',
      gradient: 'from-indigo-600 via-emerald-600 to-teal-700',
      actionText: 'Simulate Growth',
      link: '/simulation-lab',
      image: '⚡'
    },
    {
      id: 4,
      tag: 'RAG AI Assistant',
      title: 'Agronomist Copilot',
      subtitle: 'Conversational Crop Science Advisor',
      description: 'Ask questions about fertigation formulas, Pythium prevention, or your active grow batch.',
      badge: '24/7 AI Advisor',
      gradient: 'from-emerald-700 via-teal-700 to-slate-800',
      actionText: 'Ask Copilot',
      link: '/assistant',
      image: '🤖'
    }
  ];

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % carouselCards.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + carouselCards.length) % carouselCards.length);
  };

  return (
    <div className="max-w-7xl mx-auto space-y-10 animate-in fade-in duration-300 py-2">
      
      {/* Top Greeting Header (Matching Reference Image) */}
      <div className="space-y-1">
        <h1 className="text-3xl sm:text-4xl font-black text-slate-900 dark:text-white tracking-tight flex items-center gap-2">
          Hi, {user?.name || 'Karthikeya'}! <span className="animate-bounce inline-block">👋</span>
        </h1>
        <p className="text-base text-slate-600 dark:text-slate-400 font-medium">
          Let's help you maximize your hydroponic harvest yield
        </p>
      </div>

      {/* Main 2-Column Internshala Portal Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left Column: Action Items (3) Sidebar (3 cols on lg) */}
        <div className="lg:col-span-4 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-black text-slate-900 dark:text-white tracking-tight flex items-center gap-2">
              <FileText className="w-5 h-5 text-emerald-600" />
              Action items (3)
            </h2>
          </div>

          <div className="space-y-3">
            
            {/* Action Item 1 */}
            <div
              onClick={() => navigate('/prediction')}
              className="saas-card p-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl hover:border-emerald-500 hover:shadow-lg transition-all cursor-pointer group flex items-start justify-between gap-3"
            >
              <div className="flex items-start gap-3">
                <div className="p-2.5 rounded-xl bg-emerald-50 dark:bg-emerald-950 text-emerald-600 shrink-0 mt-0.5">
                  <Sparkles className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900 dark:text-white group-hover:text-emerald-600 transition-colors">
                    Improve yield prediction accuracy
                  </h3>
                  <p className="text-xs text-slate-500 mt-1">3 parameters ready for calibration</p>
                </div>
              </div>
              <ChevronRight className="w-5 h-5 text-slate-400 group-hover:text-emerald-600 group-hover:translate-x-1 transition-all shrink-0 mt-1" />
            </div>

            {/* Action Item 2 */}
            <div
              onClick={() => navigate('/plant-doctor')}
              className="saas-card p-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl hover:border-emerald-500 hover:shadow-lg transition-all cursor-pointer group flex items-start justify-between gap-3"
            >
              <div className="flex items-start gap-3">
                <div className="p-2.5 rounded-xl bg-teal-50 dark:bg-teal-950 text-teal-600 shrink-0 mt-0.5">
                  <Camera className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900 dark:text-white group-hover:text-emerald-600 transition-colors">
                    Plant health scan pending
                  </h3>
                  <p className="text-xs text-slate-500 mt-1">Requested for Batch #214 (Lettuce)</p>
                </div>
              </div>
              <ChevronRight className="w-5 h-5 text-slate-400 group-hover:text-emerald-600 group-hover:translate-x-1 transition-all shrink-0 mt-1" />
            </div>

            {/* Action Item 3 */}
            <div
              onClick={() => navigate('/iot-monitoring')}
              className="saas-card p-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl hover:border-emerald-500 hover:shadow-lg transition-all cursor-pointer group flex items-start justify-between gap-3"
            >
              <div className="flex items-start gap-3">
                <div className="p-2.5 rounded-xl bg-blue-50 dark:bg-blue-950 text-blue-600 shrink-0 mt-0.5">
                  <Sliders className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900 dark:text-white group-hover:text-emerald-600 transition-colors">
                    Sensor probe calibration due
                  </h3>
                  <p className="text-xs text-slate-500 mt-1">Water pH probe check recommended</p>
                </div>
              </div>
              <ChevronRight className="w-5 h-5 text-slate-400 group-hover:text-emerald-600 group-hover:translate-x-1 transition-all shrink-0 mt-1" />
            </div>

          </div>

          {/* Quick Active Batch Status Widget */}
          <div className="saas-card p-5 bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-2xl space-y-3">
            <div className="flex items-center justify-between text-xs">
              <span className="font-bold text-slate-700 dark:text-slate-300">Active Batch Status</span>
              <Badge variant="optimized">95% Healthy</Badge>
            </div>
            <div className="text-sm font-bold text-slate-900 dark:text-white">
              Butterhead Lettuce • Batch #214
            </div>
            <div className="w-full bg-slate-200 dark:bg-slate-800 h-2 rounded-full overflow-hidden">
              <div className="bg-emerald-600 h-full w-[60%]" />
            </div>
            <div className="flex justify-between text-xs text-slate-500 font-medium pt-1">
              <span>Day 18 of 30</span>
              <span className="font-bold text-emerald-600">Harvest in 12 Days</span>
            </div>
          </div>
        </div>

        {/* Right Column: Trending Carousel & Recommended Sections (8 cols on lg) */}
        <div className="lg:col-span-8 space-y-10">
          
          {/* Section 1: Trending on HydroGrow AI Carousel Slider 🔥 */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-black text-slate-900 dark:text-white tracking-tight flex items-center gap-2">
                Trending on HydroGrow AI <Flame className="w-5 h-5 text-amber-500 fill-amber-500" />
              </h2>

              {/* Slider Controls */}
              <div className="flex items-center gap-2">
                <button
                  onClick={prevSlide}
                  aria-label="Previous Slide"
                  className="p-2 rounded-full border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 transition-all shadow-xs"
                >
                  <ChevronLeft className="w-4 h-4" />
                </button>
                <button
                  onClick={nextSlide}
                  aria-label="Next Slide"
                  className="p-2 rounded-full border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 transition-all shadow-xs"
                >
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Carousel Active Slide Card */}
            {(() => {
              const slide = carouselCards[currentSlide];
              return (
                <div className={`saas-card p-8 sm:p-10 bg-gradient-to-br ${slide.gradient} text-white rounded-3xl shadow-xl transition-all duration-500 transform hover:-translate-y-1 relative overflow-hidden flex flex-col justify-between min-h-[260px]`}>
                  <div className="flex items-center justify-between">
                    <span className="px-3 py-1 rounded-full bg-white/20 backdrop-blur-md text-xs font-bold uppercase tracking-wider text-white">
                      {slide.tag}
                    </span>
                    <Badge variant="brand" className="bg-white text-slate-900 font-bold border-none shadow-xs">
                      {slide.badge}
                    </Badge>
                  </div>

                  <div className="space-y-2 py-4">
                    <div className="flex items-center gap-3">
                      <span className="text-4xl">{slide.image}</span>
                      <div>
                        <h3 className="text-2xl sm:text-3xl font-black tracking-tight">{slide.title}</h3>
                        <p className="text-xs text-emerald-100 font-medium">{slide.subtitle}</p>
                      </div>
                    </div>
                    <p className="text-sm text-emerald-100 max-w-xl leading-relaxed pt-1">
                      {slide.description}
                    </p>
                  </div>

                  <div className="flex items-center justify-between pt-4 border-t border-white/20">
                    <Link to={slide.link}>
                      <Button variant="secondary" size="md" icon={ArrowRight} className="bg-white text-slate-900 hover:bg-emerald-50 shadow-md">
                        {slide.actionText}
                      </Button>
                    </Link>

                    {/* Slide Indicator Bar */}
                    <div className="flex items-center gap-1.5">
                      {carouselCards.map((_, i) => (
                        <button
                          key={i}
                          onClick={() => setCurrentSlide(i)}
                          aria-label={`Go to slide ${i + 1}`}
                          className={`h-2 rounded-full transition-all duration-300 ${
                            currentSlide === i ? 'w-6 bg-white' : 'w-2 bg-white/40'
                          }`}
                        />
                      ))}
                    </div>
                  </div>
                </div>
              );
            })()}
          </div>

          {/* Section 2: Current AI Supported Crop (Scientifically Accurate) */}
          <div className="space-y-4">
            <div>
              <h2 className="text-lg font-black text-slate-900 dark:text-white tracking-tight">
                Current AI Supported Crop
              </h2>
              <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">
                Model trained exclusively on hydroponic lettuce growth cycles. <span className="font-bold text-emerald-600 dark:text-emerald-400">216 growth cycles analyzed.</span>
              </p>
            </div>

            <Card padding="p-6 sm:p-8" className="space-y-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-sm hover:border-emerald-500 transition-all">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 dark:border-slate-800 pb-4">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-2xl bg-emerald-50 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400 flex items-center justify-center text-2xl font-black shrink-0 border border-emerald-100 dark:border-emerald-900 shadow-xs">
                    🌱
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="text-xl font-black text-slate-900 dark:text-white">Butterhead Lettuce</h3>
                      <Badge variant="optimized">Active Trained Model</Badge>
                    </div>
                    <p className="text-xs text-slate-500 mt-0.5 font-medium">Dataset: 216 Verified Hydroponic Growth Cycles</p>
                  </div>
                </div>

                <Link to="/prediction">
                  <Button variant="primary" size="sm" icon={ArrowRight}>
                    Run Prediction
                  </Button>
                </Link>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-left">
                <div className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-950/60 border border-slate-100 dark:border-slate-800">
                  <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">AI Yield Benchmark</div>
                  <div className="text-2xl font-black text-emerald-600 dark:text-emerald-400 mt-1">382.7g / plant</div>
                  <div className="text-[11px] text-slate-500 font-semibold mt-1">91% Model Confidence</div>
                </div>

                <div className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-950/60 border border-slate-100 dark:border-slate-800">
                  <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">Growth Stage</div>
                  <div className="text-2xl font-black text-slate-900 dark:text-white mt-1">Vegetative</div>
                  <div className="text-[11px] text-slate-500 font-semibold mt-1">Day 18 of 30</div>
                </div>

                <div className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-950/60 border border-slate-100 dark:border-slate-800">
                  <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">Environment</div>
                  <div className="text-2xl font-black text-slate-900 dark:text-white mt-1">Optimal</div>
                  <div className="text-[11px] text-emerald-600 dark:text-emerald-400 font-semibold mt-1">Temp 22°C • pH 6.0 • EC 2.0</div>
                </div>
              </div>
            </Card>
          </div>

        </div>

      </div>

    </div>
  );
}
