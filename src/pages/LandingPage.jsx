import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  ArrowRight, 
  Rocket, 
  Shield, 
  RefreshCw, 
  Cloud, 
  CheckCircle, 
  Users, 
  BarChart3, 
  Database,
  Globe,
  Lock,
  Zap,
  Award,
  TrendingUp
} from 'lucide-react';
import FeatureCard from '../components/FeatureCard';
import WaitlistModal from '../components/WaitlistModal';
import { useToast } from '../components/Toast';
import personas from '../config/personas';
import verticals from '../config/verticals';

const LandingPage = ({ onStartDemo }) => {
  const [persona, setPersona] = useState('builder');
  const [visibleSection, setVisibleSection] = useState(0);
  const [showWaitlist, setShowWaitlist] = useState(false);
  const { showToast, ToastContainer } = useToast();
  const { headline, description, features } = personas[persona];

  const handleStartDemo = () => {
    console.log('Get Early Access button clicked!');
    showToast('Early access coming soon! We\'re putting the finishing touches on this feature.', 'info', 4000);
  };

  const handleJoinWaitlist = () => {
    console.log('Join Waitlist button clicked!');
    setShowWaitlist(true);
  };

  // Intersection Observer for scroll animations
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-fade-in');
          }
        });
      },
      { threshold: 0.1 }
    );

    const sections = document.querySelectorAll('.scroll-reveal');
    sections.forEach((section) => observer.observe(section));

    return () => observer.disconnect();
  }, []);

  const keyFeatures = [
    {
      icon: Globe,
      title: "Diverse & Realistic Data",
      description: "Statistically mirrors real patient populations, including rare conditions and underrepresented groups.",
      color: "text-secondary-500"
    },
    {
      icon: Shield,
      title: "Privacy by Design",
      description: "100% synthetic records with zero PHI, compliant with HIPAA and GDPR from day one.",
      color: "text-primary-500"
    },
    {
      icon: RefreshCw,
      title: "Continuously Updated",
      description: "AI agents ingest new medical research continuously, so your data never goes stale.",
      color: "text-accent-500"
    },
    {
      icon: Cloud,
      title: "On-Demand & Scalable",
      description: "Access via API or UI; generate millions of records in minutes.",
      color: "text-primary-500"
    },
    {
      icon: CheckCircle,
      title: "Validated Accuracy",
      description: "Benchmarked against real-world stats to ensure clinical credibility.",
      color: "text-secondary-500"
    }
  ];

  const howItWorks = [
    {
      step: "01",
      title: "Input Your Criteria",
      description: "Researchers or clinicians define the patient cohort or parameters via our no-code UI.",
      icon: Database
    },
    {
      step: "02", 
      title: "AI-Generates Multimodal Synthetic Data",
      description: "Our engine creates comprehensive synthetic datasets with EHR records, imaging data, genomics, and clinical notes - all linked and clinically consistent.",
      icon: Zap
    },
    {
      step: "03",
      title: "Integrate & Innovate", 
      description: "Download via API or CSV and plug into your AI models, studies, or applications immediately.",
      icon: TrendingUp
    }
  ];

  const useCases = [
    {
      title: "Pharma & Biotech",
      description: "Simulate trials on virtual patients to accelerate drug discovery.",
      icon: Award,
      accent: "accent"
    },
    {
      title: "AI/MedTech Companies",
      description: "Train models on bias-free synthetic data to improve accuracy and reduce hallucinations.",
      icon: BarChart3,
      accent: "primary"
    },
    {
      title: "Clinical Researchers",
      description: "Access a trove of EHR data for hypothesis testing without IRB hurdles.",
      icon: Users,
      accent: "secondary"
    }
  ];

  return (
    <div className="min-h-screen bg-white dark:bg-neutral-900 transition-colors duration-300">
      {/* Hero Section */}
      <div className="relative pt-20 pb-16 sm:pt-24 sm:pb-20 lg:pt-32 lg:pb-28 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-50 via-white to-secondary-50 dark:from-neutral-900 dark:via-neutral-800 dark:to-neutral-900"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center animate-slide-up">
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-heading font-extrabold mb-6">
              <span className="bg-gradient-to-r from-primary-600 via-accent-500 to-secondary-600 bg-clip-text text-transparent">
                Synthetic Ascension
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-neutral-700 dark:text-neutral-300 max-w-4xl mx-auto mb-8 leading-relaxed">
              Generate millions of synthetic patient records in <span className="font-bold text-accent-600">minutes, not months</span>. 
              Cut data acquisition time by <span className="font-bold text-secondary-600">90%</span> while eliminating privacy risks entirely.
            </p>
            <p className="text-lg text-neutral-600 dark:text-neutral-400 max-w-3xl mx-auto mb-8">
              Replace months of IRB approvals and data partnerships with instant access to diverse, clinically-accurate synthetic EHR data.
            </p>
            
            {/* Value Props */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto mb-12">
              <div className="text-center">
                <div className="text-3xl font-bold text-primary-600 dark:text-primary-400">90%</div>
                <div className="text-sm text-neutral-600 dark:text-neutral-400">Faster Time-to-Data</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-accent-600 dark:text-accent-400">$0</div>
                <div className="text-sm text-neutral-600 dark:text-neutral-400">Privacy Risk</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-secondary-600 dark:text-secondary-400">24/7</div>
                <div className="text-sm text-neutral-600 dark:text-neutral-400">API Access</div>
              </div>
            </div>

            <div className="flex flex-wrap justify-center gap-3 mb-8">
              {Object.entries(personas).map(([key, p]) => (
                <button
                  key={key}
                  onClick={() => setPersona(key)}
                  className={`px-6 py-3 rounded-xl font-medium transition-all duration-300 border ${
                    persona === key
                      ? 'bg-primary-500 text-white border-primary-500 shadow-soft-lg transform scale-105'
                      : 'bg-white dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 border-neutral-200 dark:border-neutral-600 hover:bg-neutral-50 dark:hover:bg-neutral-700 hover:border-primary-300 dark:hover:border-primary-500'
                  }`}
                >
                  {p.label}
                </button>
              ))}
            </div>

            {/* DEBUG: Simple test buttons */}
            <div style={{ 
              position: 'fixed', 
              top: '10px', 
              right: '10px', 
              zIndex: 9999, 
              background: 'red', 
              padding: '20px',
              color: 'white' 
            }}>
              <button 
                onClick={() => alert('TEST BUTTON WORKS!')}
                style={{ 
                  background: 'blue', 
                  color: 'white', 
                  padding: '10px 20px', 
                  border: 'none',
                  cursor: 'pointer',
                  marginRight: '10px'
                }}
              >
                TEST
              </button>
              <button 
                onClick={() => setShowWaitlist(true)}
                style={{ 
                  background: 'green', 
                  color: 'white', 
                  padding: '10px 20px', 
                  border: 'none',
                  cursor: 'pointer'
                }}
              >
                OPEN MODAL
              </button>
            </div>

            <div className="flex flex-col gap-4 justify-center items-center" style={{ zIndex: 10, position: 'relative' }}>
              <div className="flex flex-col sm:flex-row gap-4 items-center">
                <button
                  onClick={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('Get Early Access clicked - Event triggered!');
                    alert('Get Early Access clicked!'); // Temporary debug
                    showToast('Early access coming soon! We\'re putting the finishing touches on this feature.', 'info', 4000);
                  }}
                  className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-primary-500 to-accent-500 text-white font-bold rounded-xl hover:from-primary-600 hover:to-accent-600 transition-all duration-300 shadow-soft-lg hover:shadow-soft-lg transform hover:scale-105 text-lg cursor-pointer"
                  style={{ pointerEvents: 'all', zIndex: 20 }}
                >
                  Get Early Access
                </button>
                <button
                  onClick={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('Join Waitlist clicked - Event triggered!');
                    alert('Join Waitlist clicked!'); // Temporary debug
                    setShowWaitlist(true);
                  }}
                  className="inline-flex items-center px-8 py-4 bg-neutral-100 dark:bg-neutral-800 text-neutral-800 dark:text-neutral-100 font-bold rounded-xl hover:bg-neutral-200 dark:hover:bg-neutral-700 transition-all duration-300 shadow-soft-lg hover:shadow-soft-lg transform hover:scale-105 text-lg border border-neutral-300 dark:border-neutral-600 cursor-pointer"
                  style={{ pointerEvents: 'all', zIndex: 20 }}
                >
                  Join Waitlist
                </button>
              </div>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                Join researchers from Stanford, Mayo Clinic, and 500+ healthcare organizations
              </p>
            </div>

            <div className="mt-12 text-center">
              <p className="text-sm text-neutral-500 dark:text-neutral-400 mb-4">
                <Shield className="inline w-4 h-4 mr-1" />
                HIPAA Compliant • 100% Synthetic Data • No Patient Privacy Risk
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Problem & Solution Overview */}
      <div className="scroll-reveal py-16 lg:py-24 bg-neutral-50 dark:bg-neutral-800/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl lg:text-4xl font-heading font-bold text-neutral-900 dark:text-white mb-6">
                AI healthcare models are starving for diverse, representative data
              </h2>
              <div className="space-y-4 text-lg text-neutral-600 dark:text-neutral-300">
                <div className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-red-500 rounded-full mt-3"></div>
                  <p>Real patient data is siloed, biased, and hard to obtain</p>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-red-500 rounded-full mt-3"></div>
                  <p>IRB approvals take months and limit research scope</p>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-red-500 rounded-full mt-3"></div>
                  <p>80% of healthcare data goes unused due to privacy constraints</p>
                </div>
              </div>
            </div>
            <div>
              <h3 className="text-2xl lg:text-3xl font-heading font-bold text-neutral-900 dark:text-white mb-6">
                The answer? A new kind of data.
              </h3>
              <div className="space-y-4 text-lg text-neutral-600 dark:text-neutral-300">
                <div className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-secondary-500 rounded-full mt-3"></div>
                  <p>Unlimited synthetic patients with no privacy risk</p>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-secondary-500 rounded-full mt-3"></div>
                  <p>Statistically validated against real-world data</p>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-secondary-500 rounded-full mt-3"></div>
                  <p>Ready to use immediately via API or download</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Key Features Section */}
      <div className="scroll-reveal py-16 lg:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-heading font-bold text-neutral-900 dark:text-white mb-4">
              Why Leading AI Teams Choose Synthetic Ascension
            </h2>
            <p className="text-xl text-neutral-600 dark:text-neutral-300 max-w-3xl mx-auto">
              Built for AI researchers, validated by clinicians, trusted by enterprise teams
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {keyFeatures.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div
                  key={index}
                  className="bg-white dark:bg-neutral-800 p-8 rounded-2xl shadow-soft hover:shadow-soft-lg transition-all duration-300 border border-neutral-100 dark:border-neutral-700 group hover:border-primary-200 dark:hover:border-primary-600"
                >
                  <div className={`inline-flex p-3 rounded-xl ${feature.color} bg-opacity-10 mb-6 group-hover:bg-opacity-20 transition-all duration-300`}>
                    <Icon className={`w-6 h-6 ${feature.color}`} />
                  </div>
                  <h3 className="text-xl font-heading font-semibold text-neutral-900 dark:text-white mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-neutral-600 dark:text-neutral-300 leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* How It Works Section */}
      <div className="scroll-reveal py-16 lg:py-24 bg-neutral-50 dark:bg-neutral-800/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-heading font-bold text-neutral-900 dark:text-white mb-4">
              How It Works
            </h2>
            <p className="text-xl text-neutral-600 dark:text-neutral-300 max-w-3xl mx-auto">
              From criteria to data in minutes, not months
            </p>
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {howItWorks.map((step, index) => {
              const Icon = step.icon;
              return (
                <div key={index} className="relative">
                  <div className="bg-white dark:bg-neutral-800 p-8 rounded-2xl shadow-soft border border-neutral-100 dark:border-neutral-700">
                    <div className="text-center">
                      <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-primary-500 to-accent-500 text-white rounded-2xl font-bold text-xl mb-6">
                        {step.step}
                      </div>
                      <Icon className="w-12 h-12 text-primary-500 mx-auto mb-6" />
                      <h3 className="text-xl font-heading font-semibold text-neutral-900 dark:text-white mb-4">
                        {step.title}
                      </h3>
                      <p className="text-neutral-600 dark:text-neutral-300 leading-relaxed">
                        {step.description}
                      </p>
                    </div>
                  </div>
                  {index < howItWorks.length - 1 && (
                    <div className="hidden lg:block absolute top-1/2 -right-4 transform -translate-y-1/2">
                      <ArrowRight className="w-8 h-8 text-primary-300" />
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Use Cases Section */}
      <div className="scroll-reveal py-16 lg:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-heading font-bold text-neutral-900 dark:text-white mb-4">
              Built for Every Healthcare AI Team
            </h2>
            <p className="text-xl text-neutral-600 dark:text-neutral-300 max-w-3xl mx-auto">
              Tailored solutions for your specific research and development needs
            </p>
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {useCases.map((useCase, index) => {
              const Icon = useCase.icon;
              const colorClass = {
                primary: 'from-primary-500 to-primary-600',
                secondary: 'from-secondary-500 to-secondary-600',
                accent: 'from-accent-500 to-accent-600'
              };
              return (
                <div
                  key={index}
                  className="relative overflow-hidden bg-white dark:bg-neutral-800 rounded-2xl shadow-soft hover:shadow-soft-lg transition-all duration-300 border border-neutral-100 dark:border-neutral-700 group"
                >
                  <div className={`absolute inset-0 bg-gradient-to-br ${colorClass[useCase.accent]} opacity-5 group-hover:opacity-10 transition-opacity duration-300`}></div>
                  <div className="relative p-8">
                    <Icon className={`w-12 h-12 text-${useCase.accent}-500 mb-6`} />
                    <h3 className="text-xl font-heading font-semibold text-neutral-900 dark:text-white mb-4">
                      {useCase.title}
                    </h3>
                    <p className="text-neutral-600 dark:text-neutral-300 leading-relaxed">
                      {useCase.description}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Trust & Testimonials Section */}
      <div className="scroll-reveal py-16 lg:py-24 bg-neutral-50 dark:bg-neutral-800/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-heading font-bold text-neutral-900 dark:text-white mb-4">
              Trusted by Leading Research Teams
            </h2>
            <p className="text-xl text-neutral-600 dark:text-neutral-300 max-w-3xl mx-auto">
              Join the growing community of AI researchers accelerating healthcare innovation
            </p>
          </div>

          {/* Trust Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
            <div className="text-center">
              <div className="text-4xl font-bold text-primary-500 mb-2">10x</div>
              <div className="text-lg font-medium text-neutral-900 dark:text-white mb-1">Faster Data Access</div>
              <div className="text-neutral-600 dark:text-neutral-300">vs traditional IRB approvals</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-secondary-500 mb-2">100%</div>
              <div className="text-lg font-medium text-neutral-900 dark:text-white mb-1">Privacy Compliant</div>
              <div className="text-neutral-600 dark:text-neutral-300">HIPAA, GDPR, and CCPA ready</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-accent-500 mb-2">86%</div>
              <div className="text-lg font-medium text-neutral-900 dark:text-white mb-1">Reduction in Prep Time</div>
              <div className="text-neutral-600 dark:text-neutral-300">from data request to model training</div>
            </div>
          </div>

          {/* Trust Badges */}
          <div className="flex flex-wrap justify-center items-center gap-8 opacity-60">
            <div className="flex items-center space-x-2 bg-white dark:bg-neutral-800 px-4 py-2 rounded-lg">
              <Shield className="w-5 h-5 text-primary-500" />
              <span className="text-sm font-medium text-neutral-700 dark:text-neutral-300">HIPAA Compliant</span>
            </div>
            <div className="flex items-center space-x-2 bg-white dark:bg-neutral-800 px-4 py-2 rounded-lg">
              <Lock className="w-5 h-5 text-primary-500" />
              <span className="text-sm font-medium text-neutral-700 dark:text-neutral-300">Enterprise Security</span>
            </div>
            <div className="flex items-center space-x-2 bg-white dark:bg-neutral-800 px-4 py-2 rounded-lg">
              <CheckCircle className="w-5 h-5 text-secondary-500" />
              <span className="text-sm font-medium text-neutral-700 dark:text-neutral-300">Clinically Validated</span>
            </div>
          </div>
        </div>
      </div>

      {/* Final CTA Section */}
      <div className="scroll-reveal py-16 lg:py-24 bg-gradient-to-r from-primary-500 via-accent-500 to-secondary-500">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl lg:text-4xl font-heading font-bold text-white mb-6">
            Skip months of data delays. Start building tomorrow.
          </h2>
          <p className="text-xl text-neutral-100 mb-8">
            Join 500+ AI teams already using synthetic data to accelerate healthcare innovation. 
            <span className="font-semibold">Early access includes 10,000 free patient records.</span>
          </p>
          
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 mb-8 max-w-2xl mx-auto">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-white">
              <div className="flex items-center space-x-3">
                <CheckCircle className="w-6 h-6 text-accent-200" />
                <span>Instant API access</span>
              </div>
              <div className="flex items-center space-x-3">
                <CheckCircle className="w-6 h-6 text-accent-200" />
                <span>No IRB delays</span>
              </div>
              <div className="flex items-center space-x-3">
                <CheckCircle className="w-6 h-6 text-accent-200" />
                <span>Zero privacy risk</span>
              </div>
              <div className="flex items-center space-x-3">
                <CheckCircle className="w-6 h-6 text-accent-200" />
                <span>Clinical accuracy guaranteed</span>
              </div>
            </div>
          </div>
          

        </div>
      </div>
      
      {/* Waitlist Modal - COMMENTED OUT - Using App.tsx modal instead */}
      {/* {showWaitlist && (
        <WaitlistModal 
          isOpen={showWaitlist}
          onClose={() => setShowWaitlist(false)}
        />
      )} */}
      
      <ToastContainer />
    </div>
  );
};

export default LandingPage;