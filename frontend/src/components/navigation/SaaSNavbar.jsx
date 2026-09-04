import React, { useState, useContext } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { 
  Sprout, Bot, Menu, X, LayoutDashboard, User, History, 
  TrendingUp, Cpu, Sliders, Camera, Sun, Moon, Sparkles, 
  ChevronDown, Store, LogOut, Settings
} from 'lucide-react';
import { AppContext } from '../../context/AppContext';

export default function SaaSNavbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const [isMobileOpen, setIsMobileOpen] = useState(false);
  const [activeMenu, setActiveMenu] = useState(null);
  const [showUserDropdown, setShowUserDropdown] = useState(false);
  
  const { theme, toggleTheme, user, isAuthenticated, logout } = useContext(AppContext);

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="fixed top-0 left-0 w-full z-50 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border-b border-slate-200/80 dark:border-slate-800 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/dashboard" className="flex items-center space-x-2.5 group">
              <div className="p-2 bg-emerald-600 rounded-xl text-white group-hover:scale-105 transition-transform shadow-xs">
                <Sprout className="h-5 w-5" />
              </div>
              <span className="text-lg font-black tracking-tight text-slate-900 dark:text-white">
                HydroGrow <span className="text-emerald-600 dark:text-emerald-400">AI</span>
              </span>
            </Link>
          </div>

          {/* Desktop Navigation Links */}
          <div className="hidden md:flex items-center space-x-1">
            <Link
              to="/dashboard"
              className={`px-3.5 py-2 rounded-lg text-sm font-semibold transition-colors ${
                isActive('/dashboard')
                  ? 'text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60'
                  : 'text-slate-700 dark:text-slate-200 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-slate-50 dark:hover:bg-slate-800'
              }`}
            >
              Dashboard
            </Link>

            <Link
              to="/plant-doctor"
              className={`px-3.5 py-2 rounded-lg text-sm font-semibold flex items-center gap-1.5 transition-colors ${
                isActive('/plant-doctor') || isActive('/plant-health')
                  ? 'text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60'
                  : 'text-slate-700 dark:text-slate-200 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-slate-50 dark:hover:bg-slate-800'
              }`}
            >
              <Camera className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              <span>Plant Doctor</span>
            </Link>

            <Link
              to="/prediction"
              className={`px-3.5 py-2 rounded-lg text-sm font-semibold flex items-center gap-1.5 transition-colors ${
                isActive('/prediction')
                  ? 'text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60'
                  : 'text-slate-700 dark:text-slate-200 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-slate-50 dark:hover:bg-slate-800'
              }`}
            >
              <Sparkles className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              <span>Yield Predictor</span>
            </Link>

            <Link
              to="/simulation"
              className={`px-3.5 py-2 rounded-lg text-sm font-semibold flex items-center gap-1.5 transition-colors ${
                isActive('/simulation') || isActive('/digital-twin') || isActive('/twin')
                  ? 'text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60'
                  : 'text-slate-700 dark:text-slate-200 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-slate-50 dark:hover:bg-slate-800'
              }`}
            >
              <Cpu className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              <span>Digital Twin</span>
            </Link>

            <Link
              to="/history/predictions"
              className={`px-3.5 py-2 rounded-lg text-sm font-semibold flex items-center gap-1.5 transition-colors ${
                isActive('/history/predictions') || isActive('/history')
                  ? 'text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60'
                  : 'text-slate-700 dark:text-slate-200 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-slate-50 dark:hover:bg-slate-800'
              }`}
            >
              <History className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              <span>Scan History</span>
            </Link>
          </div>

          {/* Right Actions */}
          <div className="hidden md:flex items-center space-x-3">
            
            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              aria-label="Toggle light and dark theme"
              className="p-2 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            >
              {theme === 'dark' ? <Sun className="w-5 h-5 text-amber-400" /> : <Moon className="w-5 h-5 text-slate-600" />}
            </button>

            {/* User Profile Avatar with Dropdown */}
            <div className="relative pl-2">
              <button
                onClick={() => setShowUserDropdown(!showUserDropdown)}
                className="flex items-center gap-2 p-1.5 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors border border-slate-200/80 dark:border-slate-800"
              >
                <div className="w-7 h-7 rounded-full bg-emerald-600 text-white font-bold flex items-center justify-center text-xs shadow-xs">
                  {user?.name ? user.name[0].toUpperCase() : 'K'}
                </div>
                <span className="text-xs font-bold text-slate-800 dark:text-slate-200">
                  {user?.name || 'Grower'}
                </span>
                <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
              </button>

              {showUserDropdown && (
                <div className="absolute right-0 top-full mt-2 w-48 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl p-2 space-y-1">
                  <Link
                    to="/profile"
                    onClick={() => setShowUserDropdown(false)}
                    className="flex items-center gap-2 p-2.5 text-xs font-bold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-xl"
                  >
                    <User className="w-4 h-4 text-emerald-600" />
                    Profile & Settings
                  </Link>
                  <Link
                    to="/history/predictions"
                    onClick={() => setShowUserDropdown(false)}
                    className="flex items-center gap-2 p-2.5 text-xs font-bold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-xl"
                  >
                    <History className="w-4 h-4 text-emerald-600" />
                    Scan History
                  </Link>
                  <button
                    onClick={() => {
                      if (logout) logout();
                      setShowUserDropdown(false);
                      navigate('/');
                    }}
                    className="w-full flex items-center gap-2 p-2.5 text-xs font-bold text-red-600 hover:bg-red-50 dark:hover:bg-red-950/50 rounded-xl text-left"
                  >
                    <LogOut className="w-4 h-4" />
                    Log Out
                  </button>
                </div>
              )}
            </div>

          </div>

          {/* Mobile hamburger button */}
          <div className="md:hidden flex items-center gap-2">
            <button
              onClick={toggleTheme}
              aria-label="Toggle theme"
              className="p-2 rounded-xl text-slate-600 dark:text-slate-300"
            >
              {theme === 'dark' ? <Sun className="w-5 h-5 text-amber-400" /> : <Moon className="w-5 h-5" />}
            </button>
            <button
              onClick={() => setIsMobileOpen(!isMobileOpen)}
              className="p-2 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800"
            >
              {isMobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

        </div>
      </div>

      {/* Mobile Drawer Navigation */}
      {isMobileOpen && (
        <div className="md:hidden bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 px-4 pt-2 pb-6 space-y-3">
          <Link
            to="/dashboard"
            onClick={() => setIsMobileOpen(false)}
            className="block py-2 text-base font-bold text-slate-900 dark:text-white"
          >
            Dashboard
          </Link>
          <Link to="/plant-doctor" onClick={() => setIsMobileOpen(false)} className="block py-1.5 text-sm font-semibold text-slate-700 dark:text-slate-300">Plant Doctor</Link>
          <Link to="/prediction" onClick={() => setIsMobileOpen(false)} className="block py-1.5 text-sm font-semibold text-slate-700 dark:text-slate-300">Yield Predictor</Link>
          <Link to="/simulation" onClick={() => setIsMobileOpen(false)} className="block py-1.5 text-sm font-semibold text-slate-700 dark:text-slate-300">Digital Twin</Link>
          <Link to="/history/predictions" onClick={() => setIsMobileOpen(false)} className="block py-1.5 text-sm font-semibold text-slate-700 dark:text-slate-300">Scan History</Link>
          <Link to="/profile" onClick={() => setIsMobileOpen(false)} className="block py-1.5 text-sm font-semibold text-slate-700 dark:text-slate-300">Profile & Settings</Link>
        </div>
      )}
    </nav>
  );
}
