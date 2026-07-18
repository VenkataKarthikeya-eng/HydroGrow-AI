import React, { useState } from 'react';
import { Cpu, Wifi, Activity, Zap, CheckCircle2, RefreshCw, AlertTriangle, ShieldCheck } from 'lucide-react';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';

export default function IoTMonitoringDashboard() {
  const [isRefreshing, setIsRefreshing] = useState(false);

  const sensors = [
    { name: 'Water pH Sensor #01', value: '6.05 pH', target: '6.0 - 6.4 pH', status: 'Optimal', icon: '🧪', variant: 'optimized' },
    { name: 'EC Telemetry Probe #02', value: '1.82 mS/cm', target: '1.8 - 2.2 mS/cm', status: 'Optimal', icon: '⚡', variant: 'optimized' },
    { name: 'Solution Temp Sensor #03', value: '22.4°C', target: '21.0 - 23.0°C', status: 'Optimal', icon: '🌡️', variant: 'optimized' },
    { name: 'Canopy Air Temp Probe #04', value: '22.8°C', target: '20.0 - 25.0°C', status: 'Optimal', icon: '☀️', variant: 'optimized' },
    { name: 'Ambient Humidity Sensor #05', value: '64.5%', target: '60 - 70%', status: 'Optimal', icon: '💧', variant: 'optimized' },
    { name: 'CO2 Greenhouse Sensor #06', value: '460 ppm', target: '400 - 600 ppm', status: 'Optimal', icon: '💨', variant: 'optimized' },
  ];

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => setIsRefreshing(false), 1000);
  };

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-300">
      
      {/* Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
            <Cpu className="w-4 h-4" /> Telemetry & MQTT Feeds
          </div>
          <h1 className="text-3xl font-black text-slate-900 dark:text-white mt-1">
            IoT Monitoring Center
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Real-time telemetry feeds from physical greenhouse sensors, water probes, and dosing actuators.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Badge variant="optimized" className="px-3 py-1.5 text-xs">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" /> Live Streaming (100ms)
          </Badge>
          <Button variant="outline" size="sm" onClick={handleRefresh} isLoading={isRefreshing} icon={RefreshCw}>
            Sync Sensors
          </Button>
        </div>
      </div>

      {/* Sensor Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {sensors.map((sensor, idx) => (
          <Card key={idx} padding="p-6 sm:p-8" className="space-y-4 hover:border-emerald-500 transition-colors">
            <div className="flex items-center justify-between">
              <span className="text-2xl">{sensor.icon}</span>
              <Badge variant={sensor.variant}>{sensor.status}</Badge>
            </div>
            <div>
              <div className="text-xs font-bold text-slate-500 uppercase tracking-wider">{sensor.name}</div>
              <div className="text-3xl font-black text-slate-900 dark:text-white mt-1">{sensor.value}</div>
            </div>
            <div className="pt-3 border-t border-slate-100 dark:border-slate-800 flex justify-between text-xs text-slate-500">
              <span>Target Range:</span>
              <span className="font-semibold text-slate-700 dark:text-slate-300">{sensor.target}</span>
            </div>
          </Card>
        ))}
      </div>

      {/* Actuator Status Card */}
      <Card padding="p-8" header="Automated Fertigation Actuators & Dosing Systems">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
          <div className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 flex justify-between items-center">
            <div>
              <div className="font-bold text-slate-900 dark:text-white">Dosing Pump A (Macro)</div>
              <div className="text-xs text-slate-500">Scheduled: Every 4 Hours</div>
            </div>
            <Badge variant="optimized">Online</Badge>
          </div>

          <div className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 flex justify-between items-center">
            <div>
              <div className="font-bold text-slate-900 dark:text-white">pH Buffer Injector</div>
              <div className="text-xs text-slate-500">Auto Dose: Enabled</div>
            </div>
            <Badge variant="optimized">Online</Badge>
          </div>

          <div className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 flex justify-between items-center">
            <div>
              <div className="font-bold text-slate-900 dark:text-white">Misting & Aeration Fan</div>
              <div className="text-xs text-slate-500">Duty Cycle: 80%</div>
            </div>
            <Badge variant="optimized">Online</Badge>
          </div>
        </div>
      </Card>

    </div>
  );
}
