import React, { lazy, Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AppProvider } from './context/AppContext.jsx';
import ErrorBoundary from './components/common/ErrorBoundary.jsx';
import Loader from './components/ui/Loader.jsx';

// Layouts
import PublicLayout from './layouts/PublicLayout.jsx';
import DashboardLayout from './layouts/DashboardLayout.jsx';

// Public Marketing Pages
import LandingPage from './pages/LandingPage.jsx';
import Pricing from './pages/public/Pricing.jsx';
import About from './pages/public/About.jsx';
import Contact from './pages/public/Contact.jsx';
import Login from './pages/Login.jsx';
import Register from './pages/Register.jsx';

// Core SaaS App Pages
import Overview from './pages/app/Overview.jsx';
import AIPredictionWizard from './pages/app/AIPredictionWizard.jsx';
import PlantDoctor from './pages/app/PlantDoctor.jsx';
import SimulationLab from './pages/app/SimulationLab.jsx';
import Profile from './pages/Profile.jsx';
import PredictionHistory from './pages/PredictionHistory.jsx';

function App() {
  return (
    <ErrorBoundary>
      <AppProvider>
        <Router>
          <Suspense fallback={<div className="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-950"><Loader message="Loading HydroGrow AI..." /></div>}>
            <Routes>
              
              {/* Public Marketing Routes */}
              <Route element={<PublicLayout />}>
                <Route path="/" element={<LandingPage />} />
                <Route path="/pricing" element={<Pricing />} />
                <Route path="/about" element={<About />} />
                <Route path="/contact" element={<Contact />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
              </Route>

              {/* Authenticated SaaS Dashboard App Routes */}
              <Route element={<DashboardLayout />}>
                <Route path="/dashboard" element={<Overview />} />
                <Route path="/plant-doctor" element={<PlantDoctor />} />
                <Route path="/plant-health" element={<PlantDoctor />} />
                <Route path="/prediction" element={<AIPredictionWizard />} />
                <Route path="/simulation" element={<SimulationLab />} />
                <Route path="/twin" element={<SimulationLab />} />
                <Route path="/digital-twin" element={<SimulationLab />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/history/predictions" element={<PredictionHistory />} />
                <Route path="/history" element={<PredictionHistory />} />
              </Route>

              {/* Fallback */}
              <Route path="*" element={<Navigate to="/dashboard" replace />} />

            </Routes>
          </Suspense>
        </Router>
      </AppProvider>
    </ErrorBoundary>
  );
}

export default App;
