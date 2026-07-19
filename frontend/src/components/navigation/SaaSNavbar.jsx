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
              Overview
            </Link>

            {/* AI Tools Dropdown */}
            <div 
              className="relative"
              onMouseEnter={() => setActiveMenu('ai')}
              onMouseLeave={() => setActiveMenu(null)}
            >
              <button
                className={`px-3.5 py-2 rounded-lg text-sm font-semibold inline-flex items-center gap-1.5 transition-colors ${
                  ['/prediction', '/plant-doctor', '/simulation-lab', '/assistant'].some(p => isActive(p))
                    ? 'text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60'
                    : 'text-slate-700 dark:text-slate-200 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-slate-50 dark:hover:bg-slate-800'
                }`}
              >
                <Sparkles className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                <span>AI Tools</span>
                <ChevronDown className="w-3.5 h-3.5 opacity-60" />
              </button>

              {activeMenu === 'ai' && (
                <div className="absolute top-full left-0 w-64 pt-2">
                  <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl p-2 space-y-1">
                    <Link
                      to="/prediction"
                      className="flex items-center gap-3 p-3 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-emerald-50 dark:hover:bg-emerald-950/60 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors"
                    >
                      <Sparkles className="w-4 h-4 text-emerald-600" />
                      <div>
                        <div className="text-sm font-bold">AI Yield Wizard</div>
                        <div className="text-xs text-slate-500 dark:text-slate-400">3-Step ML Yield Forecast</div>
                      </div>
                    </Link>

                    <Link
                      to="/plant-doctor"
                      className="flex items-center gap-3 p-3 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-emerald-50 dark:hover:bg-emerald-950/60 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors"
                    >
                      <Camera className="w-4 h-4 text-emerald-600" />
                      <div>
                        <div className="text-sm font-bold">Plant Doctor Scanner</div>
                        <div className="text-xs text-slate-500 dark:text-slate-400">Leaf Pathology Scanner</div>
                      </div>
                    </Link>

                    <Link
                      to="/simulation-lab"
                      className="flex items-center gap-3 p-3 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-emerald-50 dark:hover:bg-emerald-950/60 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors"
                    >
                      <Cpu className="w-4 h-4 text-emerald-600" />
                      <div>
                        <div className="text-sm font-bold">Simulation Lab</div>
                        <div className="text-xs text-slate-500 dark:text-slate-400">Digital Twin Crop Simulator</div>
                      </div>
                    </Link>

                    <Link
                      to="/assistant"
                      className="flex items-center gap-3 p-3 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-emerald-50 dark:hover:bg-emerald-950/60 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors"
                    >
                      <Bot className="w-4 h-4 text-emerald-600" />
                      <div>
                        <div className="text-sm font-bold">Agronomist Copilot</div>
                        <div className="text-xs text-slate-500 dark:text-slate-400">RAG Crop Science AI</div>
                      </div>
                    </Link>
                  </div>
                </div>
              )}
            </div>

            {/* Farm Intelligence Dropdown */}
            <div 
              className="relative"
              onMouseEnter={() => setActiveMenu('intelligence')}
              onMouseLeave={() => setActiveMenu(null)}
            >
              <button
                className={`px-3.5 py-2 rounded-lg text-sm font-semibold inline-flex items-center gap-1.5 transition-colors ${
                  ['/crop-intelligence', '/iot-monitoring', '/automation'].some(p => isActive(p))
                    ? 'text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60'
                    : 'text-slate-700 dark:text-slate-200 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-slate-50 dark:hover:bg-slate-800'
                }`}
              >
                <TrendingUp className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                <span>Farm Intelligence</span>
                <ChevronDown className="w-3.5 h-3.5 opacity-60" />
              </button>

              {activeMenu === 'intelligence' && (
                <div className="absolute top-full left-0 w-64 pt-2">
                  <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl p-2 space-y-1">
                    <Link
                      to="/crop-intelligence"
                      className="flex items-center gap-3 p-3 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-emerald-50 dark:hover:bg-emerald-950/60 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors"
                    >
                      <TrendingUp className="w-4 h-4 text-emerald-600" />
                      <div>
                        <div className="text-sm font-bold">Crop Intelligence</div>
                        <div className="text-xs text-slate-500 dark:text-slate-400">Growth Cycle Analytics</div>
                      </div>
                    </Link>

                    <Link
                      to="/iot-monitoring"
                      className="flex items-center gap-3 p-3 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-emerald-50 dark:hover:bg-emerald-950/60 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors"
                    >
                      <Cpu className="w-4 h-4 text-emerald-600" />
                      <div>
                        <div className="text-sm font-bold">IoT Telemetry</div>
                        <div className="text-xs text-slate-500 dark:text-slate-400">Real-Time Sensor Streams</div>
                      </div>
                    </Link>

                    <Link
                      to="/automation"
                      className="flex items-center gap-3 p-3 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-emerald-50 dark:hover:bg-emerald-950/60 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors"
                    >
                      <Sliders className="w-4 h-4 text-emerald-600" />
                      <div>
                        <div className="text-sm font-bold">Automation Controls</div>
                        <div className="text-xs text-slate-500 dark:text-slate-400">Dosing Rules & Actuators</div>
                      </div>
                    </Link>
                  </div>
                </div>
              )}
            </div>

            {/* Management Dropdown */}
            <div 
              className="relative"
              onMouseEnter={() => setActiveMenu('management')}
              onMouseLeave={() => setActiveMenu(null)}
            >
              <button
                className={`px-3.5 py-2 rounded-lg text-sm font-semibold inline-flex items-center gap-1.5 transition-colors ${
                  ['/history/predictions', '/profile'].some(p => isActive(p))
                    ? 'text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60'
                    : 'text-slate-700 dark:text-slate-200 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-slate-50 dark:hover:bg-slate-800'
                }`}
              >
                <User className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                <span>Management</span>
                <ChevronDown className="w-3.5 h-3.5 opacity-60" />
              </button>

              {activeMenu === 'management' && (
                <div className="absolute top-full left-0 w-64 pt-2">
                  <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl p-2 space-y-1">
                    <Link
                      to="/history/predictions"
                      className="flex items-center gap-3 p-3 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-emerald-50 dark:hover:bg-emerald-950/60 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors"
                    >
                      <History className="w-4 h-4 text-emerald-600" />
                      <div>
                        <div className="text-sm font-bold">Prediction History</div>
                        <div className="text-xs text-slate-500 dark:text-slate-400">Historical Logs & PDF Reports</div>
                      </div>
                    </Link>

                    <Link
                      to="/profile"
                      className="flex items-center gap-3 p-3 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-emerald-50 dark:hover:bg-emerald-950/60 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors"
                    >
                      <Settings className="w-4 h-4 text-emerald-600" />
                      <div>
                        <div className="text-sm font-bold">Farm Settings</div>
                        <div className="text-xs text-slate-500 dark:text-slate-400">{user?.farmName || 'Demo Farm'}</div>
                      </div>
                    </Link>
                  </div>
                </div>
              )}
            </div>

            <Link
              to="/marketplace"
              className={`px-3.5 py-2 rounded-lg text-sm font-semibold transition-colors flex items-center gap-1.5 ${
                isActive('/marketplace')
                  ? 'text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60'
                  : 'text-slate-700 dark:text-slate-200 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-slate-50 dark:hover:bg-slate-800'
              }`}
            >
              <Store className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              Marketplace
            </Link>
          </div>

          {/* Right Actions (Matching Internshala Header Reference Image) */}
          <div className="hidden md:flex items-center space-x-3">
            
            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              aria-label="Toggle light and dark theme"
              className="p-2 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            >
              {theme === 'dark' ? <Sun className="w-5 h-5 text-amber-400" /> : <Moon className="w-5 h-5 text-slate-600" />}
            </button>

            {/* User Profile Avatar with Dropdown (Matching Screenshot: 👤 Karthikeya ▼) */}
            <div className="relative pl-2">
              <button
                onClick={() => setShowUserDropdown(!showUserDropdown)}
                className="flex items-center gap-2 p-1.5 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors border border-slate-200/80 dark:border-slate-800"
              >
                <div className="w-7 h-7 rounded-full bg-emerald-600 text-white font-bold flex items-center justify-center text-xs shadow-xs">
                  {user?.name ? user.name[0].toUpperCase() : 'K'}
                </div>
                <span className="text-xs font-bold text-slate-800 dark:text-slate-200">
                  {user?.name || 'Karthikeya'}
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
                    Prediction History
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
        <div className="md:hidden bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 px-4 pt-2 pb-6 space-y-4">
          <Link
            to="/dashboard"
            onClick={() => setIsMobileOpen(false)}
            className="block py-2 text-base font-bold text-slate-900 dark:text-white"
          >
            Overview
          </Link>
          
          <div className="space-y-1">
            <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">AI Tools</div>
            <Link to="/prediction" onClick={() => setIsMobileOpen(false)} className="block py-1.5 text-sm text-slate-700 dark:text-slate-300">AI Yield Wizard</Link>
            <Link to="/plant-doctor" onClick={() => setIsMobileOpen(false)} className="block py-1.5 text-sm text-slate-700 dark:text-slate-300">Plant Doctor Scanner</Link>
            <Link to="/simulation-lab" onClick={() => setIsMobileOpen(false)} className="block py-1.5 text-sm text-slate-700 dark:text-slate-300">Simulation Lab</Link>
            <Link to="/assistant" onClick={() => setIsMobileOpen(false)} className="block py-1.5 text-sm text-slate-700 dark:text-slate-300">Agronomist Copilot</Link>
          </div>

          <div className="space-y-1">
            <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">Farm Intelligence</div>
            <Link to="/crop-intelligence" onClick={() => setIsMobileOpen(false)} className="block py-1.5 text-sm text-slate-700 dark:text-slate-300">Crop Intelligence</Link>
            <Link to="/iot-monitoring" onClick={() => setIsMobileOpen(false)} className="block py-1.5 text-sm text-slate-700 dark:text-slate-300">IoT Telemetry</Link>
          </div>

          <div className="space-y-1">
            <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">Management</div>
            <Link to="/history/predictions" onClick={() => setIsMobileOpen(false)} className="block py-1.5 text-sm text-slate-700 dark:text-slate-300">Prediction History</Link>
            <Link to="/profile" onClick={() => setIsMobileOpen(false)} className="block py-1.5 text-sm text-slate-700 dark:text-slate-300">Profile & Settings</Link>
          </div>
        </div>
      )}
    </nav>
  );
}
