import React from 'react';
import { Sprout, ExternalLink, Linkedin, Github, Mail } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="bg-white dark:bg-slate-950 border-t border-slate-200 dark:border-slate-800/80 py-12 px-4 mt-auto transition-colors">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8 text-xs">
        
        {/* Column 1: Brand & Creator Attribution */}
        <div className="space-y-3">
          <div className="flex items-center gap-2 font-bold text-slate-900 dark:text-white text-sm">
            <Sprout className="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
            <span>HydroGrow AI</span>
            <span className="text-slate-400 text-xs font-medium">© 2026</span>
          </div>
          <p className="text-slate-500 dark:text-slate-400 leading-relaxed font-medium">
            Built with AI + Hydroponics Innovation
          </p>
          <div className="text-slate-500 dark:text-slate-400 pt-1 font-medium">
            Designed & Developed by{' '}
            <a
              href="https://www.linkedin.com/in/cherukuri-venkata-karthikeya-4b54393ab/"
              target="_blank"
              rel="noopener noreferrer"
              className="font-bold text-slate-900 dark:text-slate-200 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors"
            >
              Karthikeya Cherukuri
            </a>
          </div>
        </div>

        {/* Column 2: Platform Links */}
        <div className="space-y-3">
          <div className="font-bold text-slate-900 dark:text-white uppercase tracking-wider text-[11px]">
            Platform Links
          </div>
          <ul className="space-y-2 text-slate-500 dark:text-slate-400 font-medium">
            <li>
              <Link to="/about" className="hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors">
                Documentation & Research
              </Link>
            </li>
            <li>
              <Link to="/crop-intelligence" className="hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors">
                API Guide & Analytics
              </Link>
            </li>
            <li>
              <Link to="/iot-monitoring" className="hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors">
                System Diagnostics
              </Link>
            </li>
          </ul>
        </div>

        {/* Column 3: Connect Links */}
        <div className="space-y-3">
          <div className="font-bold text-slate-900 dark:text-white uppercase tracking-wider text-[11px]">
            Connect
          </div>
          <ul className="space-y-2.5 text-slate-500 dark:text-slate-400 font-medium">
            <li>
              <a
                href="https://www.linkedin.com/in/cherukuri-venkata-karthikeya-4b54393ab/"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors font-bold text-slate-700 dark:text-slate-300"
              >
                <Linkedin className="w-3.5 h-3.5 text-[#0A66C2]" />
                <span>LinkedIn</span>
                <ExternalLink className="w-3 h-3 opacity-70" />
              </a>
            </li>
            <li>
              <a
                href="https://github.com/VenkataKarthikeya-eng"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors font-bold text-slate-700 dark:text-slate-300"
              >
                <Github className="w-3.5 h-3.5 text-slate-800 dark:text-slate-200" />
                <span>GitHub</span>
                <ExternalLink className="w-3 h-3 opacity-70" />
              </a>
            </li>
            <li>
              <a
                href="mailto:venkatakarthikeya2005@gmail.com"
                className="inline-flex items-center gap-1.5 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors font-bold text-slate-700 dark:text-slate-300"
              >
                <Mail className="w-3.5 h-3.5 text-emerald-600" />
                <span>Email</span>
              </a>
            </li>
          </ul>
        </div>

      </div>
    </footer>
  );
}
