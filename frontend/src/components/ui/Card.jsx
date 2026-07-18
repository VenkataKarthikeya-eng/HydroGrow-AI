import React from 'react';

export default function Card({
  children,
  className = '',
  header,
  subtitle,
  footer,
  hoverable = false,
  padding = 'p-6 sm:p-8',
  ...props
}) {
  return (
    <div
      className={`saas-card ${padding} ${hoverable ? 'saas-card-hover cursor-pointer' : ''} ${className}`}
      {...props}
    >
      {header && (
        <div className="border-b border-slate-100 dark:border-slate-800/80 pb-4 mb-5 flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-slate-900 dark:text-white tracking-tight">{header}</h3>
            {subtitle && <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{subtitle}</p>}
          </div>
        </div>
      )}
      <div>{children}</div>
      {footer && (
        <div className="border-t border-slate-100 dark:border-slate-800/80 pt-4 mt-6 text-xs text-slate-500 font-medium">
          {footer}
        </div>
      )}
    </div>
  );
}
