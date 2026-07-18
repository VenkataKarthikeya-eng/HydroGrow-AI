import React, { useState, useContext } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Sprout, Bot, Menu, X, LayoutDashboard, User, History, LogIn, TrendingUp, Cpu, Sliders, Camera, Cloud, Building, Brain } from 'lucide-react';
import { AppContext } from '../context/AppContext';
import UserMenu from './UserMenu';

function Navbar() {
  const location = useLocation();
  const [isOpen, setIsOpen] = useState(false);
  const { isAuthenticated } = useContext(AppContext);

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="fixed top-0 left-0 w-full z-50 bg-slate-950/80 backdrop-blur-md border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2 group">
              <div className="p-1.5 bg-emerald-500/10 rounded-lg group-hover:bg-emerald-500/20 transition-colors">
                <Sprout className="h-6 w-6 text-emerald-400 group-hover:scale-105 transition-transform" />
              </div>
              <span className="text-xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-200 to-emerald-400 bg-clip-text text-transparent">
                HydroGrow <span className="text-emerald-400">AI</span>
              </span>
            </Link>
          </div>
          
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              <Link
                to="/"
                className={`px-3 py-2 rounded-md text-sm font-medium transition-all ${
                  isActive('/')
                    ? 'text-emerald-400 bg-emerald-500/5'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                }`}
              >
                Home
              </Link>
              <Link
                to="/prediction"
                className={`px-3 py-2 rounded-md text-sm font-medium flex items-center gap-1.5 transition-all ${
                  isActive('/prediction')
                    ? 'text-emerald-400 bg-emerald-500/5'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                }`}
              >
                <LayoutDashboard className="h-4 w-4" />
                Prediction Dashboard
              </Link>
              <Link
                to="/assistant"
                className={`px-3 py-2 rounded-md text-sm font-medium flex items-center gap-1.5 transition-all ${
                  isActive('/assistant')
                    ? 'text-emerald-400 bg-emerald-500/5'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                }`}
              >
                <Bot className="h-4 w-4" />
                Ask Assistant
              </Link>
              <Link
                to="/analytics"
                className={`px-3 py-2 rounded-md text-sm font-medium flex items-center gap-1.5 transition-all ${
                  isActive('/analytics')
                    ? 'text-emerald-400 bg-emerald-500/5'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                }`}
              >
                <TrendingUp className="h-4 w-4 animate-pulse" />
                Analytics
              </Link>
              <Link
                to="/iot"
                className={`px-3 py-2 rounded-md text-sm font-medium flex items-center gap-1.5 transition-all ${
                  isActive('/iot')
                    ? 'text-emerald-400 bg-emerald-500/5'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                }`}
              >
                <Cpu className="h-4 w-4 text-emerald-400" />
                IoT Monitoring
              </Link>
              <Link
                to="/automation"
                className={`px-3 py-2 rounded-md text-sm font-medium flex items-center gap-1.5 transition-all ${
                  isActive('/automation')
                    ? 'text-emerald-400 bg-emerald-500/5'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                }`}
              >
                <Sliders className="h-4 w-4 text-emerald-400" />
                Automation
              </Link>
              <Link
                to="/plant-health"
                className={`px-3 py-2 rounded-md text-sm font-medium flex items-center gap-1.5 transition-all ${
                  isActive('/plant-health')
                    ? 'text-emerald-400 bg-emerald-500/5'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                }`}
              >
                <Camera className="h-4 w-4 text-emerald-400" />
                Plant Health
              </Link>
              <Link
                to="/digital-twin"
                className={`px-3 py-2 rounded-md text-sm font-medium flex items-center gap-1.5 transition-all ${
                  isActive('/digital-twin')
                    ? 'text-emerald-400 bg-emerald-500/5'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                }`}
              >
                <Cpu className="h-4 w-4 text-emerald-450 animate-pulse" />
                Digital Twin
              </Link>
              <Link
                to="/copilot"
                className={`px-3 py-2 rounded-md text-sm font-medium flex items-center gap-1.5 transition-all ${
                  isActive('/copilot')
                    ? 'text-emerald-400 bg-emerald-500/5 font-extrabold'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                }`}
              >
                <Bot className="h-4 w-4 text-emerald-400 animate-pulse" />
                AI Copilot
              </Link>
              <Link
                to="/ml-center"
                className={`px-3 py-2 rounded-md text-sm font-medium flex items-center gap-1.5 transition-all ${
                  isActive('/ml-center')
                    ? 'text-emerald-400 bg-emerald-500/5 font-extrabold'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                }`}
              >
                <Cpu className="h-4 w-4 text-emerald-400" />
                ML Center
              </Link>
              <Link
                to="/cloud"
                className={`px-3 py-2 rounded-md text-sm font-medium flex items-center gap-1.5 transition-all ${
                  isActive('/cloud')
                    ? 'text-emerald-400 bg-emerald-500/5 font-extrabold'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                }`}
              >
                <Cloud className="h-4 w-4 text-emerald-400" />
                Cloud Ops
              </Link>
              <Link
                to="/farms"
                className={`px-3 py-2 rounded-md text-sm font-medium flex items-center gap-1.5 transition-all ${
                  isActive('/farms')
                    ? 'text-emerald-400 bg-emerald-500/5 font-extrabold'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                }`}
              >
                <Building className="h-4 w-4 text-emerald-400" />
                Farms SaaS
              </Link>
              <Link
                to="/marketplace"
                className={`px-3 py-2 rounded-md text-sm font-medium flex items-center gap-1.5 transition-all ${
                  isActive('/marketplace')
                    ? 'text-emerald-400 bg-emerald-500/5 font-extrabold'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                }`}
              >
                Marketplace
              </Link>
              <Link
                to="/community"
                className={`px-3 py-2 rounded-md text-sm font-medium flex items-center gap-1.5 transition-all ${
                  isActive('/community')
                    ? 'text-emerald-400 bg-emerald-500/5 font-extrabold'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                }`}
              >
                Community
              </Link>
              <Link
                to="/intelligence"
                className={`px-3 py-2 rounded-md text-sm font-medium flex items-center gap-1.5 transition-all ${
                  isActive('/intelligence')
                    ? 'text-emerald-400 bg-emerald-500/5 font-extrabold'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                }`}
              >
                <Brain className="h-4 w-4 text-emerald-400" />
                Intelligence
              </Link>
              {isAuthenticated && (
                <Link
                  to="/history/predictions"
                  className={`px-3 py-2 rounded-md text-sm font-medium flex items-center gap-1.5 transition-all ${
                    isActive('/history/predictions')
                      ? 'text-emerald-400 bg-emerald-500/5'
                      : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                  }`}
                >
                  <History className="h-4 w-4" />
                  Prediction Logs
                </Link>
              )}
            </div>
          </div>
 
          {/* User auth badge */}
          <div className="hidden md:block">
            {isAuthenticated ? (
              <UserMenu />
            ) : (
              <Link
                to="/login"
                className="flex items-center space-x-1.5 text-slate-300 hover:text-white bg-slate-900 border border-slate-850 hover:bg-slate-850 rounded-full px-4 py-1.5 transition-all text-xs font-semibold"
              >
                <LogIn className="h-4 w-4 text-emerald-400" />
                <span>Grower Portal</span>
              </Link>
            )}
          </div>
 
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-slate-400 hover:text-white hover:bg-slate-800 focus:outline-none"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>
 
      {/* Mobile menu */}
      {isOpen && (
        <div className="md:hidden bg-slate-950 border-b border-slate-800 px-2 pt-2 pb-3 space-y-1 sm:px-3">
          <Link
            to="/"
            onClick={() => setIsOpen(false)}
            className={`block px-3 py-2 rounded-md text-base font-medium ${
              isActive('/') ? 'text-emerald-400 bg-emerald-500/5' : 'text-slate-300 hover:text-white hover:bg-slate-800'
            }`}
          >
            Home
          </Link>
          <Link
            to="/prediction"
            onClick={() => setIsOpen(false)}
            className={`block px-3 py-2 rounded-md text-base font-medium ${
              isActive('/prediction') ? 'text-emerald-400 bg-emerald-500/5' : 'text-slate-300 hover:text-white hover:bg-slate-800'
            }`}
          >
            Prediction Dashboard
          </Link>
          <Link
            to="/assistant"
            onClick={() => setIsOpen(false)}
            className={`block px-3 py-2 rounded-md text-base font-medium ${
              isActive('/assistant') ? 'text-emerald-400 bg-emerald-500/5' : 'text-slate-300 hover:text-white hover:bg-slate-800'
            }`}
          >
            Ask Assistant
          </Link>
          <Link
            to="/analytics"
            onClick={() => setIsOpen(false)}
            className={`block px-3 py-2 rounded-md text-base font-medium ${
              isActive('/analytics') ? 'text-emerald-400 bg-emerald-500/5' : 'text-slate-300 hover:text-white hover:bg-slate-800'
            }`}
          >
            Analytics
          </Link>
          <Link
            to="/iot"
            onClick={() => setIsOpen(false)}
            className={`block px-3 py-2 rounded-md text-base font-medium ${
              isActive('/iot') ? 'text-emerald-400 bg-emerald-500/5' : 'text-slate-300 hover:text-white hover:bg-slate-800'
            }`}
          >
            IoT Monitoring
          </Link>
          <Link
            to="/automation"
            onClick={() => setIsOpen(false)}
            className={`block px-3 py-2 rounded-md text-base font-medium ${
              isActive('/automation') ? 'text-emerald-400 bg-emerald-500/5' : 'text-slate-300 hover:text-white hover:bg-slate-800'
            }`}
          >
            Automation
          </Link>
          <Link
            to="/plant-health"
            onClick={() => setIsOpen(false)}
            className={`block px-3 py-2 rounded-md text-base font-medium ${
              isActive('/plant-health') ? 'text-emerald-400 bg-emerald-500/5' : 'text-slate-300 hover:text-white hover:bg-slate-800'
            }`}
          >
            Plant Health
          </Link>
          <Link
            to="/digital-twin"
            onClick={() => setIsOpen(false)}
            className={`block px-3 py-2 rounded-md text-base font-medium ${
              isActive('/digital-twin') ? 'text-emerald-400 bg-emerald-500/5' : 'text-slate-300 hover:text-white hover:bg-slate-800'
            }`}
          >
            Digital Twin
          </Link>
          {isAuthenticated && (
            <>
              <Link
                to="/history/predictions"
                onClick={() => setIsOpen(false)}
                className={`block px-3 py-2 rounded-md text-base font-medium ${
                  isActive('/history/predictions') ? 'text-emerald-400 bg-emerald-500/5' : 'text-slate-300 hover:text-white hover:bg-slate-800'
                }`}
              >
                Prediction Logs
              </Link>
              <Link
                to="/profile"
                onClick={() => setIsOpen(false)}
                className={`block px-3 py-2 rounded-md text-base font-medium ${
                  isActive('/profile') ? 'text-emerald-400 bg-emerald-500/5' : 'text-slate-300 hover:text-white hover:bg-slate-800'
                }`}
              >
                Grower Profile
              </Link>
            </>
          )}
          <div className="pt-2">
            {isAuthenticated ? (
              <div className="flex items-center space-x-2 text-slate-400 text-sm bg-slate-900 border border-slate-800 rounded-md px-3 py-2">
                <User className="h-4 w-4 text-emerald-400" />
                <span>Logged In</span>
              </div>
            ) : (
              <Link
                to="/login"
                onClick={() => setIsOpen(false)}
                className="flex items-center justify-center space-x-2 text-slate-300 hover:text-white bg-slate-900 border border-slate-800 hover:bg-slate-850 rounded-md px-3 py-2 text-sm font-semibold"
              >
                <LogIn className="h-4 w-4 text-emerald-400" />
                <span>Grower Portal</span>
              </Link>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}

export default Navbar;
