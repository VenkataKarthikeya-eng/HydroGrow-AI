import React, { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Sprout, LogIn, Lock, Mail, ArrowRight } from 'lucide-react';
import { AppContext } from '../context/AppContext';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';

export default function Login() {
  const navigate = useNavigate();
  const { login } = useContext(AppContext);
  const [email, setEmail] = useState('karthikeya@hydrogrow.ai');
  const [password, setPassword] = useState('password123');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      if (login) await login(email, password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="py-16 px-4 max-w-md mx-auto space-y-8 animate-in fade-in duration-300">
      
      <div className="text-center space-y-3">
        <Link to="/" className="inline-flex items-center space-x-2 justify-center">
          <div className="p-2 bg-emerald-600 rounded-xl text-white">
            <Sprout className="h-6 w-6" />
          </div>
          <span className="text-2xl font-black text-slate-900 dark:text-white tracking-tight">
            HydroGrow <span className="text-emerald-600">AI</span>
          </span>
        </Link>
        <h1 className="text-2xl font-black text-slate-900 dark:text-white">Welcome Back</h1>
        <p className="text-sm text-slate-500">Sign in to manage your hydroponic farm & AI predictions.</p>
      </div>

      <Card padding="p-8">
        {error && (
          <div className="mb-4 p-3 rounded-xl bg-red-50 text-red-700 text-xs font-semibold border border-red-200">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Email Address</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-emerald-500 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-emerald-500 focus:outline-none"
            />
          </div>

          <Button variant="primary" type="submit" isLoading={loading} icon={LogIn} className="w-full">
            Sign In to Farm
          </Button>
        </form>

        <div className="mt-6 pt-4 border-t border-slate-100 dark:border-slate-800 text-center text-xs text-slate-500">
          Don't have an account?{' '}
          <Link to="/register" className="font-bold text-emerald-600 hover:underline">
            Register Free
          </Link>
        </div>
      </Card>

    </div>
  );
}
