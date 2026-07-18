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

// SaaS App Pages
import Overview from './pages/app/Overview.jsx';
import AIPredictionWizard from './pages/app/AIPredictionWizard.jsx';
import PlantDoctor from './pages/app/PlantDoctor.jsx';
import SimulationLab from './pages/app/SimulationLab.jsx';

// Existing App Modules
import AIAssistantPage from './pages/AIAssistantPage.jsx';
import Profile from './pages/Profile.jsx';
import PredictionHistory from './pages/PredictionHistory.jsx';
import AnalyticsDashboard from './pages/AnalyticsDashboard.jsx';
import IoTMonitoringDashboard from './pages/IoTMonitoringDashboard.jsx';
import AutomationDashboard from './pages/AutomationDashboard.jsx';
import AutonomousCopilot from './pages/AutonomousCopilot.jsx';
import MLModelCenter from './pages/MLModelCenter.jsx';
import CloudDashboard from './pages/CloudDashboard.jsx';
import FarmDashboard from './pages/farm/FarmDashboard.jsx';
import Marketplace from './pages/ecosystem/Marketplace.jsx';
import CommunityHub from './pages/ecosystem/CommunityHub.jsx';
import ExpertDirectory from './pages/ecosystem/ExpertDirectory.jsx';
import CropTemplateLibrary from './pages/ecosystem/CropTemplateLibrary.jsx';
import FarmIntelligenceDashboard from './pages/intelligence/FarmIntelligenceDashboard.jsx';

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
                
                {/* AI Tools */}
                <Route path="/prediction" element={<AIPredictionWizard />} />
                <Route path="/plant-doctor" element={<PlantDoctor />} />
                <Route path="/plant-health" element={<PlantDoctor />} />
                <Route path="/simulation-lab" element={<SimulationLab />} />
                <Route path="/digital-twin" element={<SimulationLab />} />
                <Route path="/assistant" element={<AIAssistantPage />} />
                <Route path="/copilot" element={<AutonomousCopilot />} />
                <Route path="/ml-center" element={<MLModelCenter />} />

                {/* Farm Intelligence */}
                <Route path="/crop-intelligence" element={<AnalyticsDashboard />} />
                <Route path="/analytics" element={<AnalyticsDashboard />} />
                <Route path="/iot-monitoring" element={<IoTMonitoringDashboard />} />
                <Route path="/iot" element={<IoTMonitoringDashboard />} />
                <Route path="/automation" element={<AutomationDashboard />} />
                <Route path="/intelligence" element={<FarmIntelligenceDashboard />} />

                {/* Management */}
                <Route path="/profile" element={<Profile />} />
                <Route path="/history/predictions" element={<PredictionHistory />} />
                
                {/* Ecosystem */}
                <Route path="/marketplace" element={<Marketplace />} />
                <Route path="/community" element={<CommunityHub />} />
                <Route path="/experts" element={<ExpertDirectory />} />
                <Route path="/templates" element={<CropTemplateLibrary />} />
                <Route path="/cloud" element={<CloudDashboard />} />
                <Route path="/farms" element={<FarmDashboard />} />
              </Route>

              {/* Fallback */}
              <Route path="*" element={<Navigate to="/" replace />} />

            </Routes>
          </Suspense>
        </Router>
      </AppProvider>
    </ErrorBoundary>
  );
}

export default App;
