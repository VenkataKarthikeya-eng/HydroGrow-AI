import React, { useState } from 'react';
import { Store, ShoppingBag, Star, Plus, CheckCircle2, Tag } from 'lucide-react';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Badge from '../../components/ui/Badge';

export default function Marketplace() {
  const [activeCategory, setActiveCategory] = useState('All');

  const demoProducts = [
    { id: 1, name: 'Precision Hydroponic pH Buffer Kit (5L)', price: 49.99, category: 'Nutrients', rating: 4.9, desc: 'Medical grade pH-Down solution for closed loop recirculating systems.' },
    { id: 2, name: 'Digital EC & TDS Telemetry Probe', price: 129.00, category: 'Sensors', rating: 4.8, desc: 'High accuracy electrical conductivity probe with auto-temperature compensation.' },
    { id: 3, name: 'Full Spectrum LED Canopy Light (600W)', price: 349.99, category: 'Lighting', rating: 5.0, desc: 'High PAR output LED bar light optimized for vegetative lettuce flush.' },
    { id: 4, name: 'Pythium Prevention Organic Buffer (1L)', price: 39.50, category: 'Nutrients', rating: 4.7, desc: 'Biological root zone inoculant preventing fungal mildew.' },
    { id: 5, name: 'Automated 4-Channel Dosing Pump', price: 219.00, category: 'Hardware', rating: 4.9, desc: 'Microprocessor controlled peristaltic pump for automated fertigation.' },
    { id: 6, name: 'Butterhead Lettuce Certified Seeds (10k)', price: 85.00, category: 'Seeds', rating: 5.0, desc: 'High germination rate seeds bred specifically for deep water culture.' },
  ];

  const categories = ['All', 'Nutrients', 'Sensors', 'Lighting', 'Hardware', 'Seeds'];

  const filteredProducts = activeCategory === 'All'
    ? demoProducts
    : demoProducts.filter(p => p.category === activeCategory);

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-300">
      
      {/* Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
            <Store className="w-4 h-4" /> Agritech Inputs Directory
          </div>
          <h1 className="text-3xl font-black text-slate-900 dark:text-white mt-1">
            Hydroponic Equipment & Inputs Marketplace
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Browse verified commercial nutrients, LED grow lights, hardware telemetry sensors, and certified seeds.
          </p>
        </div>

        <Badge variant="brand" className="px-3 py-1.5 text-xs">
          Verified Vendors Only
        </Badge>
      </div>

      {/* Category Tabs */}
      <div className="flex flex-wrap items-center gap-2">
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              activeCategory === cat
                ? 'bg-emerald-600 text-white shadow-xs'
                : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Product Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredProducts.map((product) => (
          <Card key={product.id} padding="p-6 sm:p-8" className="flex flex-col justify-between space-y-4 hover:border-emerald-500 transition-colors">
            <div>
              <div className="flex justify-between items-start mb-2">
                <Badge variant="neutral">{product.category}</Badge>
                <div className="flex items-center gap-1 text-xs font-bold text-amber-500">
                  <Star className="w-3.5 h-3.5 fill-amber-400" />
                  <span>{product.rating}</span>
                </div>
              </div>
              <h3 className="text-base font-bold text-slate-900 dark:text-white mt-2">{product.name}</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-2 leading-relaxed">{product.desc}</p>
            </div>

            <div className="pt-4 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
              <div className="text-xl font-black text-slate-900 dark:text-white">${product.price.toFixed(2)}</div>
              <Button variant="primary" size="sm" icon={ShoppingBag}>
                Order Input
              </Button>
            </div>
          </Card>
        ))}
      </div>

    </div>
  );
}
