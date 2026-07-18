import React from 'react';
import { Check, Zap, Shield, Crown } from 'lucide-react';
import { Link } from 'react-router-dom';
import Button from '../../components/ui/Button';

export default function Pricing() {
  const plans = [
    {
      name: 'Starter Hydro',
      price: '$0',
      period: 'Forever free',
      description: 'Ideal for hobbyists and home hydroponic growers.',
      icon: Zap,
      features: [
        'Up to 5 crop yield predictions / month',
        'Basic environmental parameters tracking',
        'Plant Doctor leaf scanner (3 scans / month)',
        'Community Forum Access',
      ],
      cta: 'Start Free',
      variant: 'outline',
    },
    {
      name: 'Professional Farm',
      price: '$49',
      period: 'per month',
      popular: true,
      description: 'Built for commercial hydroponic farms and greenhouse operators.',
      icon: Shield,
      features: [
        'Unlimited AI yield predictions',
        'Real-time IoT telemetry integration',
        'Unlimited Plant Doctor computer vision scans',
        'Digital Twin simulation lab & yield optimizer',
        'Priority Agronomist AI Assistant',
        'Export PDF diagnostic reports',
      ],
      cta: 'Start 14-Day Free Trial',
      variant: 'primary',
    },
    {
      name: 'Enterprise Agritech',
      price: '$199',
      period: 'per month',
      description: 'For multi-location farms, agritech research labs & enterprise operations.',
      icon: Crown,
      features: [
        'Multi-tenant greenhouse management',
        'Custom ML model fine-tuning on your crop cycles',
        'Dedicated API access & webhook triggers',
        'Automated dosing control integration',
        'Dedicated agronomist support & SLA',
      ],
      cta: 'Contact Sales',
      variant: 'outline',
    },
  ];

  return (
    <div className="py-16 px-4 max-w-7xl mx-auto text-center space-y-12">
      <div className="max-w-3xl mx-auto space-y-4">
        <h1 className="text-4xl sm:text-5xl font-black text-slate-900 dark:text-white tracking-tight">
          Simple, Transparent <span className="text-emerald-600 dark:text-emerald-400">Pricing</span>
        </h1>
        <p className="text-lg text-slate-600 dark:text-slate-400">
          Supercharge your hydroponic crop yield and eliminate crop loss with our AI intelligence suite.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-left max-w-6xl mx-auto">
        {plans.map((plan, idx) => (
          <div
            key={idx}
            className={`saas-card p-8 flex flex-col justify-between relative ${
              plan.popular ? 'border-2 border-emerald-600 dark:border-emerald-500 shadow-xl scale-105 bg-white dark:bg-slate-900' : ''
            }`}
          >
            {plan.popular && (
              <span className="absolute -top-3.5 left-1/2 -translate-x-1/2 bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">
                Most Popular
              </span>
            )}

            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2.5 rounded-xl bg-emerald-100 dark:bg-emerald-950/60 text-emerald-600">
                  <plan.icon className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-bold text-slate-900 dark:text-white">{plan.name}</h3>
              </div>

              <p className="text-sm text-slate-500 dark:text-slate-400 mb-6">{plan.description}</p>

              <div className="mb-6">
                <span className="text-4xl font-black text-slate-900 dark:text-white">{plan.price}</span>
                <span className="text-sm font-medium text-slate-500 ml-2">{plan.period}</span>
              </div>

              <ul className="space-y-3 mb-8">
                {plan.features.map((feat, i) => (
                  <li key={i} className="flex items-start gap-2.5 text-sm text-slate-700 dark:text-slate-300">
                    <Check className="w-4 h-4 text-emerald-600 mt-0.5 shrink-0" />
                    <span>{feat}</span>
                  </li>
                ))}
              </ul>
            </div>

            <Link to="/register" className="w-full">
              <Button variant={plan.variant} className="w-full">
                {plan.cta}
              </Button>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}
