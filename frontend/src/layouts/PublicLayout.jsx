import React, { useContext } from 'react';
import { Outlet, Link } from 'react-router-dom';
import { Sprout, Sun, Moon, ArrowRight } from 'lucide-react';
import { AppContext } from '../context/AppContext';
import Footer from '../components/Footer';

export default function PublicLayout() {
  const { theme, toggleTheme, isAuthenticated } = useContext(AppContext);

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors">
      <header className="sticky top-0 z-50 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <Link to="/" className="flex items-center space-x-2 group">
              <div className="p-2 bg-emerald-100 dark:bg-emerald-950/60 rounded-xl group-hover:bg-emerald-200 transition-colors">
                <Sprout className="h-6 w-6 text-emerald-600 dark:text-emerald-400" />
              </div>
              <span className="text-xl font-black tracking-tight text-slate-900 dark:text-white">
                HydroGrow <span className="text-emerald-600 dark:text-emerald-400">AI</span>
              </span>
            </Link>

            <nav className="hidden md:flex items-center space-x-8">
              <Link to="/" className="text-sm font-semibold text-slate-600 dark:text-slate-300 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors">
                Platform
              </Link>
              <Link to="/pricing" className="text-sm font-semibold text-slate-600 dark:text-slate-300 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors">
                Pricing
              </Link>
              <Link to="/about" className="text-sm font-semibold text-slate-600 dark:text-slate-300 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors">
                About Science
              </Link>
              <Link to="/contact" className="text-sm font-semibold text-slate-600 dark:text-slate-300 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors">
                Contact
              </Link>
            </nav>

            <div className="flex items-center space-x-3">
              <button
                onClick={toggleTheme}
                aria-label="Toggle theme"
                className="p-2 rounded-lg text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              >
                {theme === 'dark' ? <Sun className="w-5 h-5 text-amber-400" /> : <Moon className="w-5 h-5 text-slate-600" />}
              </button>

              {isAuthenticated ? (
                <Link
                  to="/dashboard"
                  className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-semibold text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg shadow-sm transition-all"
                >
                  Dashboard <ArrowRight className="w-4 h-4" />
                </Link>
              ) : (
                <div className="flex items-center space-x-2">
                  <Link
                    to="/login"
                    className="px-4 py-2 text-sm font-semibold text-slate-700 dark:text-slate-200 hover:text-emerald-600 transition-colors"
                  >
                    Log In
                  </Link>
                  <Link
                    to="/register"
                    className="px-4 py-2 text-sm font-semibold text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg shadow-sm transition-all"
                  >
                    Get Started Free
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      <main className="flex-grow">
        <Outlet />
      </main>

      <Footer />
    </div>
  );
}
