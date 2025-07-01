import React from 'react';
import { 
  Zap, Shield, Target, Search, BarChart, FileText, TrendingUp, 
  DollarSign, Users, Heart, Brain, Activity, FileCheck
} from 'lucide-react';

const iconMap = {
  Zap, Shield, Target, Search, BarChart, FileText, TrendingUp, 
  DollarSign, Users, Heart, Brain, Activity, FileCheck
};

const FeatureCard = ({ icon, title, desc }) => {
  const IconComponent = iconMap[icon] || Zap;
  
  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200">
      <div className="flex items-center justify-center w-12 h-12 bg-purple-100 rounded-lg mb-4">
        <IconComponent className="w-6 h-6 text-purple-600" />
      </div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600 text-sm leading-relaxed">{desc}</p>
    </div>
  );
};

export default FeatureCard;