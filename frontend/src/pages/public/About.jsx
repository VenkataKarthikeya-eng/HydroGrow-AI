import React from 'react';
import { Sprout, Cpu, Brain, Activity, User, Award, Code, Linkedin, Github, Mail, ExternalLink } from 'lucide-react';
import Card from '../../components/ui/Card';
import Badge from '../../components/ui/Badge';

export default function About() {
  return (
    <div className="py-16 px-4 max-w-5xl mx-auto space-y-12 animate-in fade-in duration-300">
      
      {/* Title */}
      <div className="text-center space-y-4">
        <h1 className="text-4xl sm:text-5xl font-black text-slate-900 dark:text-white tracking-tight">
          About <span className="text-emerald-600 dark:text-emerald-400">HydroGrow AI</span>
        </h1>
        <p className="text-lg text-slate-600 dark:text-slate-400 max-w-3xl mx-auto">
          Combining agricultural crop science with machine learning to maximize harvest yield, prevent plant stress, and reduce water consumption by up to 90%.
        </p>
      </div>

      {/* Recruiter-Focused About the Creator Section */}
      <Card padding="p-8 sm:p-10" className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-lg space-y-6">
        
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-100 dark:border-slate-800 pb-6">
          <div>
            <Badge variant="brand" className="mb-2">
              About the Creator
            </Badge>
            <h2 className="text-3xl font-black text-slate-900 dark:text-white tracking-tight">
              Karthikeya Cherukuri
            </h2>
            <p className="text-sm font-bold text-emerald-600 dark:text-emerald-400 mt-1">
              Software Engineer | AI Developer | Data Analyst
            </p>
          </div>

          <div className="w-16 h-16 rounded-2xl bg-emerald-50 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400 flex items-center justify-center text-2xl font-black shrink-0 border border-emerald-200 dark:border-emerald-900 shadow-xs">
            KC
          </div>
        </div>

        <div className="space-y-3 text-sm text-slate-600 dark:text-slate-300 leading-relaxed font-normal">
          <p>
            Integrated M.Tech Software Engineering student passionate about building intelligent solutions using Artificial Intelligence, Machine Learning, Full Stack Development, and Data Analytics.
          </p>
          <p>
            HydroGrow AI showcases my work in combining Machine Learning, Computer Vision, IoT Systems, Data Analytics, and Digital Twin Technology to develop smart solutions for modern agriculture.
          </p>
        </div>

        {/* Professional Connect Buttons Group */}
        <div className="pt-4 border-t border-slate-100 dark:border-slate-800 flex flex-wrap items-center gap-3">
          <a
            href="https://www.linkedin.com/in/cherukuri-venkata-karthikeya-4b54393ab/"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-[#0A66C2] hover:bg-[#084e96] text-white text-xs font-bold transition-all shadow-xs"
          >
            <Linkedin className="w-4 h-4" />
            <span>LinkedIn</span>
            <ExternalLink className="w-3 h-3 opacity-80" />
          </a>

          <a
            href="https://github.com/VenkataKarthikeya-eng"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white dark:bg-slate-800 dark:hover:bg-slate-700 text-xs font-bold transition-all shadow-xs"
          >
            <Github className="w-4 h-4" />
            <span>GitHub</span>
            <ExternalLink className="w-3 h-3 opacity-80" />
          </a>

          <a
            href="mailto:venkatakarthikeya2005@gmail.com"
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-700 text-xs font-bold transition-all"
          >
            <Mail className="w-4 h-4 text-emerald-600" />
            <span>Email</span>
          </a>
        </div>

      </Card>

      {/* Platform Core Pillars */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <Card className="space-y-3" header="Precision Hydroponics ML">
          <p className="text-slate-600 dark:text-slate-300 text-sm leading-relaxed">
            Our machine learning models analyze 210+ historical growth cycles across temperature, humidity, pH, electrical conductivity (EC), and light intensity to accurately forecast harvest yields down to the gram.
          </p>
        </Card>

        <Card className="space-y-3" header="Computer Vision Plant Doctor">
          <p className="text-slate-600 dark:text-slate-300 text-sm leading-relaxed">
            Using convolutional neural networks trained on leaf pathology datasets, HydroGrow AI detects early-stage nutrient deficiencies (Nitrogen, Iron, Magnesium) and fungal infections before visual symptoms spread.
          </p>
        </Card>

        <Card className="space-y-3" header="Digital Twin Crop Simulator">
          <p className="text-slate-600 dark:text-slate-300 text-sm leading-relaxed">
            Our Digital Twin simulation lab allows growers to experiment with virtual climate variations and nutrient dosing adjustments without risking physical crop stress.
          </p>
        </Card>

        <Card className="space-y-3" header="IoT Telemetry & Automation">
          <p className="text-slate-600 dark:text-slate-300 text-sm leading-relaxed">
            Stream continuous sensor telemetry via MQTT / WebSockets to maintain automated dosing schedules and real-time environmental equilibrium.
          </p>
        </Card>
      </div>

    </div>
  );
}
