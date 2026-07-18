import React from 'react';
import { AlertOctagon, RotateCcw } from 'lucide-react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("HydroGrow UI Error Boundary caught an error:", error, errorInfo);
  }

  handleReload = () => {
    this.setState({ hasError: false, error: null });
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center justify-center p-6 text-center">
          <div className="p-4 rounded-full bg-rose-500/10 border border-rose-500/20 mb-4 text-rose-400">
            <AlertOctagon className="h-10 w-10 animate-bounce" />
          </div>
          <h2 className="text-xl font-extrabold text-slate-100 mb-2">Interface Recovery System</h2>
          <p className="text-xs text-slate-400 max-w-md mb-6">
            HydroGrow AI encountered an unexpected rendering fault. The system has prevented a crash and protected your active farm telemetry.
          </p>
          <button
            onClick={this.handleReload}
            className="px-6 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs uppercase tracking-wider transition-all flex items-center gap-2 shadow-lg"
          >
            <RotateCcw className="h-4 w-4" /> Reload Workspace
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
