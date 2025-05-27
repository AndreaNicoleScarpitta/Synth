import React from 'react'
import { Link } from 'react-router-dom'
import { ArrowRight, Beaker, Shield, Zap, Database } from 'lucide-react'

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br to-blue-50" style={{backgroundImage: 'linear-gradient(to bottom right, #F5F7FA, rgb(239 246 255))'}}>
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
        <div className="text-center">
          <h1 className="font-syne text-5xl md:text-6xl font-extrabold mb-6" style={{color: '#0A1F44'}}>
            Synthetic Ascension
          </h1>
          <p className="text-2xl font-syne font-semibold mb-4 max-w-3xl mx-auto" style={{color: '#3C3C4E'}}>
            Simulate. Validate. Ascend.
          </p>
          <p className="text-lg font-inter text-slate-gray mb-8 max-w-2xl mx-auto">
            Your launchpad to validated, privacy-safe EHR simulation—fueling the next generation of AI, research, and healthtech.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/demo"
              className="inline-flex items-center px-8 py-3 border border-transparent text-base font-inter font-semibold rounded-md text-white hover:bg-purple-700 transition-colors"
              style={{backgroundColor: '#6B4EFF'}}
            >
              Launch Demo
              <ArrowRight className="ml-2 w-5 h-5" />
            </Link>
            <button className="inline-flex items-center px-8 py-3 border text-base font-inter font-semibold rounded-md bg-white hover:bg-gray-50 transition-colors" style={{borderColor: '#6B4EFF', color: '#6B4EFF'}}>
              Design Partnership Interest
            </button>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <FeatureCard
            icon={<Beaker className="w-8 h-8" />}
            title="AI-Powered Generation"
            description="Advanced synthetic patient record creation with comprehensive clinical data"
            color="ascension-blue"
          />
          <FeatureCard
            icon={<Shield className="w-8 h-8" />}
            title="Privacy-First"
            description="HIPAA-compliant architecture with zero real patient data exposure"
            color="biotech-green"
          />
          <FeatureCard
            icon={<Zap className="w-8 h-8" />}
            title="Research Ready"
            description="Validated synthetic cohorts for pharmaceutical and clinical research"
            color="signal-violet"
          />
          <FeatureCard
            icon={<Database className="w-8 h-8" />}
            title="Enterprise Scale"
            description="Scalable platform supporting thousands of synthetic patient records"
            color="ascension-blue"
          />
        </div>
      </div>

      {/* Demo Section */}
      <div className="bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <h2 className="font-syne text-3xl font-bold text-ascension-blue mb-4">
              Experience Synthetic EHR Generation
            </h2>
            <p className="text-lg font-inter text-slate-gray mb-8 max-w-2xl mx-auto">
              Explore our pediatric cardiology demo to see how Synthetic Ascension 
              generates comprehensive, clinically accurate synthetic patient records.
            </p>
            <Link
              to="/demo"
              className="inline-flex items-center px-6 py-3 border border-transparent text-base font-inter font-semibold rounded-md text-white bg-signal-violet hover:bg-purple-700 transition-colors"
            >
              Try Pediatric Cardiology Demo
              <ArrowRight className="ml-2 w-5 h-5" />
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

const FeatureCard = ({ icon, title, description, color = 'ascension-blue' }) => {
  const iconColors = {
    'ascension-blue': 'text-ascension-blue',
    'biotech-green': 'text-biotech-green',
    'signal-violet': 'text-signal-violet'
  };

  return (
    <div className="bg-white rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow border border-gray-100">
      <div className={`${iconColors[color]} mb-4`}>{icon}</div>
      <h3 className="text-lg font-syne font-semibold text-ascension-blue mb-2">{title}</h3>
      <p className="text-slate-gray font-inter">{description}</p>
    </div>
  )
}

export default LandingPage