import React, { useContext, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { AppContext } from '../context/AppContext';
import { User, LogOut, History, ShieldAlert, Award } from 'lucide-react';

function UserMenu() {
  const { userProfile, logout } = useContext(AppContext);
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);

  if (!userProfile) return null;

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 text-slate-300 hover:text-white bg-slate-900 border border-slate-800 rounded-full px-3 py-1.5 transition-all text-xs font-semibold"
      >
        <User className="h-4 w-4 text-emerald-400" />
        <span>{userProfile.username}</span>
      </button>

      {isOpen && (
        <>
          {/* Overlay to close menu on outside clicks */}
          <div onClick={() => setIsOpen(false)} className="fixed inset-0 z-40"></div>
          
          <div className="absolute right-0 mt-2 w-48 rounded-xl bg-slate-950 border border-slate-800 p-2 shadow-2xl z-50 animate-fadeIn">
            {/* Header info */}
            <div className="px-3 py-2 border-b border-slate-900 mb-1">
              <span className="text-[10px] text-slate-500 uppercase tracking-widest font-extrabold block">Designation</span>
              <span className="text-slate-200 text-xs font-bold block">{userProfile.role}</span>
              <span className="text-slate-500 text-[10px] block font-mono">{userProfile.greenhouseId}</span>
            </div>

            <Link
              to="/profile"
              onClick={() => setIsOpen(false)}
              className="flex items-center space-x-2 px-3 py-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-900 text-xs font-medium transition-all"
            >
              <Award className="h-4 w-4 text-emerald-400" />
              <span>Grower Profile</span>
            </Link>

            <Link
              to="/prediction"
              onClick={() => setIsOpen(false)}
              className="flex items-center space-x-2 px-3 py-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-900 text-xs font-medium transition-all"
            >
              <History className="h-4 w-4 text-blue-400" />
              <span>Run Predictions</span>
            </Link>

            <button
              onClick={handleLogout}
              className="w-full flex items-center space-x-2 px-3 py-2 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-slate-900 text-xs font-medium transition-all text-left"
            >
              <LogOut className="h-4 w-4" />
              <span>Log out</span>
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default UserMenu;
