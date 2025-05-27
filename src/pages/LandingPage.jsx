import React from 'react'
import { Link } from 'react-router-dom'
import { ArrowRight, Beaker, Shield, Zap, Database } from 'lucide-react'

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
        <div className="text-center">
          <h1 className="font-syne text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Synthetic Ascension
          </h1>
          <p className="text-xl text-gray-600 mb-4 max-w-3xl mx-auto">
            Enterprise-Grade Synthetic EHR Platform
          </p>
          <p className="text-lg text-gray-500 mb-8 max-w-2xl mx-auto">
            Simulate. Validate. Ascend.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/demo"
              className="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 transition-colors"
            >
              Launch Demo
              <ArrowRight className="ml-2 w-5 h-5" />
            </Link>
            <button className="inline-flex items-center px-8 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors">
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
          />
          <FeatureCard
            icon={<Shield className="w-8 h-8" />}
            title="Privacy-First"
            description="HIPAA-compliant architecture with zero real patient data exposure"
          />
          <FeatureCard
            icon={<Zap className="w-8 h-8" />}
            title="Research Ready"
            description="Validated synthetic cohorts for pharmaceutical and clinical research"
          />
          <FeatureCard
            icon={<Database className="w-8 h-8" />}
            title="Enterprise Scale"
            description="Scalable platform supporting thousands of synthetic patient records"
          />
        </div>
      </div>

      {/* Demo Section */}
      <div className="bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <h2 className="font-syne text-3xl font-bold text-gray-900 mb-4">
              Experience Synthetic EHR Generation
            </h2>
            <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
              Explore our pediatric cardiology demo to see how Synthetic Ascension 
              generates comprehensive, clinically accurate synthetic patient records.
            </p>
            <Link
              to="/demo"
              className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 transition-colors"
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

const FeatureCard = ({ icon, title, description }) => {
  return (
    <div className="bg-white rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
      <div className="text-primary-600 mb-4">{icon}</div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}

export default LandingPage