import React from 'react';
import { Outlet } from 'react-router-dom';
import SaaSNavbar from '../components/navigation/SaaSNavbar';
import Footer from '../components/Footer';

export default function DashboardLayout() {
  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors">
      <SaaSNavbar />
      <main className="flex-grow pt-20 pb-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}
