import React, { useState } from 'react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';

export default function Contact() {
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="py-16 px-4 max-w-xl mx-auto space-y-8">
      <div className="text-center space-y-3">
        <h1 className="text-4xl font-black text-slate-900 dark:text-white">Contact HydroGrow AI</h1>
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Have questions about deploying HydroGrow AI on your farm? Send us a message.
        </p>
      </div>

      <Card>
        {submitted ? (
          <div className="text-center py-8 space-y-3">
            <div className="text-3xl">🎉</div>
            <h3 className="text-lg font-bold text-slate-900 dark:text-white">Message Received!</h3>
            <p className="text-sm text-slate-500">Our agronomist engineering team will respond within 24 hours.</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Full Name</label>
              <input
                type="text"
                required
                placeholder="Karthikeya"
                className="w-full px-3 py-2 text-sm rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Work Email</label>
              <input
                type="email"
                required
                placeholder="karthikeya@hydrofarm.com"
                className="w-full px-3 py-2 text-sm rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Message</label>
              <textarea
                rows={4}
                required
                placeholder="Tell us about your farm setup and yield target..."
                className="w-full px-3 py-2 text-sm rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>
            <Button variant="primary" type="submit" className="w-full">
              Send Message
            </Button>
          </form>
        )}
      </Card>
    </div>
  );
}
