import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown } from 'lucide-react';

export default function Dropdown({
  label,
  icon: Icon,
  items = [],
  className = '',
}) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className={`relative inline-block text-left ${className}`} ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        aria-haspopup="true"
        aria-expanded={isOpen}
        className="inline-flex items-center gap-1.5 px-3 py-2 text-sm font-medium rounded-lg text-slate-700 dark:text-slate-200 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors focus:outline-none"
      >
        {Icon && <Icon className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />}
        <span>{label}</span>
        <ChevronDown className={`w-4 h-4 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute left-0 mt-2 w-56 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-lg ring-1 ring-black/5 z-50 py-2 animate-in fade-in slide-in-from-top-2">
          {items.map((item, idx) => (
            <div key={idx}>
              {item.divider ? (
                <div className="my-1 border-t border-slate-100 dark:border-slate-800" />
              ) : (
                <a
                  href={item.href || '#'}
                  onClick={(e) => {
                    if (item.onClick) {
                      e.preventDefault();
                      item.onClick();
                    }
                    setIsOpen(false);
                  }}
                  className="flex items-center gap-2 px-4 py-2.5 text-sm text-slate-700 dark:text-slate-300 hover:bg-emerald-50 dark:hover:bg-emerald-950/40 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors font-medium"
                >
                  {item.icon && <item.icon className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />}
                  <div>
                    <div>{item.label}</div>
                    {item.description && (
                      <div className="text-xs text-slate-400 dark:text-slate-500 font-normal">{item.description}</div>
                    )}
                  </div>
                </a>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
