import React from 'react';
import { UserCheck, Star, Calendar, MessageCircle } from 'lucide-react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Badge from '../../components/ui/Badge';

export default function ExpertDirectory() {
  const experts = [
    { name: 'Dr. Evelyn Vance', title: 'Senior Hydroponic Agronomist', specialty: 'Leafy Green Fertigation & EC Tuning', rating: 4.9, sessions: '120+ Consultations' },
    { name: 'Marcus Thorne', title: 'Commercial Greenhouse Systems Engineer', specialty: 'NFT & Deep Water Culture Automation', rating: 5.0, sessions: '95+ Consultations' },
    { name: 'Dr. Aris Thorne', title: 'Plant Pathology Specialist', specialty: 'Pythium Root Rot & Fungal Containment', rating: 4.8, sessions: '140+ Consultations' },
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-300">
      <div className="border-b border-slate-200 dark:border-slate-800 pb-6">
        <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
          <UserCheck className="w-4 h-4" /> Certified Advisory Network
        </div>
        <h1 className="text-3xl font-black text-slate-900 dark:text-white mt-1">
          Agronomist & Systems Expert Directory
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Book 1-on-1 consultations with verified hydroponic crop scientists, fertigation engineers, and plant pathologists.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {experts.map((e, idx) => (
          <Card key={idx} padding="p-8" className="space-y-4 flex flex-col justify-between hover:border-emerald-500 transition-colors">
            <div>
              <div className="flex justify-between items-start mb-2">
                <Badge variant="brand">Verified Agronomist</Badge>
                <div className="flex items-center gap-1 text-xs font-bold text-amber-500">
                  <Star className="w-3.5 h-3.5 fill-amber-400" />
                  <span>{e.rating}</span>
                </div>
              </div>
              <h3 className="text-lg font-bold text-slate-900 dark:text-white mt-2">{e.name}</h3>
              <p className="text-xs text-emerald-600 font-semibold">{e.title}</p>
              <p className="text-xs text-slate-500 mt-2 leading-relaxed">{e.specialty}</p>
            </div>

            <div className="pt-4 border-t border-slate-100 dark:border-slate-800 flex justify-between items-center">
              <span className="text-xs text-slate-400">{e.sessions}</span>
              <Button variant="primary" size="sm" icon={Calendar}>
                Book Consultation
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
