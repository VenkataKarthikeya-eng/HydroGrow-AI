import React from 'react';
import { MessageSquare, Users, ThumbsUp, Plus } from 'lucide-react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Badge from '../../components/ui/Badge';

export default function CommunityHub() {
  const posts = [
    { title: 'Best EC range for summer butterhead lettuce in NFT systems?', author: 'Karthikeya', replies: 12, likes: 34, tag: 'Fertigation' },
    { title: 'How we reduced Pythium root rot using dissolved oxygen nanobubbles', author: 'Dr. Sarah Lin', replies: 28, likes: 89, tag: 'Pathology' },
    { title: 'Automating pH buffer dosing with Arduino & FastAPI webhooks', author: 'Alex Rivera', replies: 15, likes: 45, tag: 'Automation' },
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-300">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
            <Users className="w-4 h-4" /> Growers Network
          </div>
          <h1 className="text-3xl font-black text-slate-900 dark:text-white mt-1">
            Commercial Hydroponics Community Hub
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Share crop yield recipes, discuss pathology troubleshooting, and connect with commercial growers worldwide.
          </p>
        </div>

        <Button variant="primary" size="sm" icon={Plus}>
          New Discussion Topic
        </Button>
      </div>

      <div className="space-y-4">
        {posts.map((p, idx) => (
          <Card key={idx} padding="p-6 sm:p-8" className="hover:border-emerald-500 transition-colors">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <Badge variant="neutral">{p.tag}</Badge>
                  <span className="text-xs text-slate-400">Posted by <span className="font-bold text-slate-700 dark:text-slate-300">{p.author}</span></span>
                </div>
                <h3 className="text-base font-bold text-slate-900 dark:text-white mt-1">{p.title}</h3>
              </div>

              <div className="flex items-center gap-4 text-xs text-slate-500 font-semibold shrink-0">
                <span className="flex items-center gap-1"><MessageSquare className="w-4 h-4 text-emerald-600" /> {p.replies} Replies</span>
                <span className="flex items-center gap-1"><ThumbsUp className="w-4 h-4 text-blue-600" /> {p.likes} Likes</span>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
