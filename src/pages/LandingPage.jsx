import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Rocket } from 'lucide-react';
import FeatureCard from '../components/FeatureCard';
import LeadCaptureModal from '../components/LeadCaptureModal';
import personas from '../config/personas';
import verticals from '../config/verticals';

const LandingPage = ({ onStartDemo }) => {
  const [persona, setPersona] = useState('builder');
  const { headline, description, features } = personas[persona];

  const handleStartDemo = () => {
    if (onStartDemo) {
      onStartDemo();
    } else {
      // Fallback navigation to demo route
      window.location.href = '/demo';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-20">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16 transform transition-all duration-600 animate-in slide-in-from-top-8">
          <h1 className="text-5xl md:text-6xl font-extrabold mb-6 bg-gradient-to-r from-purple-600 to-blue-500 bg-clip-text text-transparent">
            Synthetic Ascension
          </h1>
          <p className="text-xl text-gray-700 max-w-3xl mx-auto mb-8">
            Privacy-safe synthetic EHRs to accelerate clinical AI development, model validation,
            and regulatory confidence — from day one.
          </p>

          <div className="flex flex-wrap justify-center gap-4 mb-8">
            {Object.entries(personas).map(([key, p]) => (
              <button
                key={key}
                onClick={() => setPersona(key)}
                className={`px-6 py-2 rounded-lg font-medium transition-all duration-200 ${
                  persona === key
                    ? 'bg-purple-600 text-white shadow-lg'
                    : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                }`}
              >
                {p.label}
              </button>
            ))}
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center mt-4">
            <button
              onClick={handleStartDemo}
              className="inline-flex items-center px-8 py-3 bg-gradient-to-r from-purple-600 to-blue-500 text-white font-semibold rounded-lg hover:from-purple-700 hover:to-blue-600 transition-all duration-200 shadow-lg hover:shadow-xl"
            >
              <Rocket className="mr-2 w-5 h-5" />
              Start Demo
            </button>
            <LeadCaptureModal />
          </div>
        </div>

        {/* Vision Section */}
        <div className="text-center mb-16 px-4">
          <h2 className="text-3xl font-bold mb-8">Our Vision</h2>
          <div className="max-w-4xl mx-auto space-y-6">
            <p className="text-gray-700 leading-relaxed">
              Synthetic Ascension is building the foundation for next-generation clinical innovation.
              We generate lifelike synthetic Electronic Health Records that empower AI teams, medical
              researchers, and regulators to iterate faster, safer, and earlier — without risking real
              patient privacy.
            </p>
            <p className="text-gray-700 leading-relaxed">
              Our agentic QA systems continuously audit synthetic reports and datasets for plausibility,
              consistency, and completeness — ensuring every output is usable, traceable, and review-ready.
              This isn't a replacement for real-world evidence — it's the way to design it better.
            </p>
          </div>
        </div>

        {/* Persona Section */}
        <div className="mb-16 px-4">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold mb-4">{headline}</h2>
            <p className="text-gray-600 max-w-3xl mx-auto">{description}</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {features.map((feature, i) => (
              <FeatureCard key={i} icon={feature.icon} title={feature.title} desc={feature.desc} />
            ))}
          </div>
        </div>

        {/* Why Now Section */}
        <div className="text-center mb-20 px-4">
          <h2 className="text-3xl font-bold mb-8">Why Now?</h2>
          <div className="max-w-4xl mx-auto space-y-6">
            <p className="text-gray-700 leading-relaxed">
              AI in healthcare is outpacing access to safe and structured data. Privacy laws like HIPAA and
              GDPR are tightening. Regulators now demand explainability, fairness, and reproducibility in
              clinical AI.
            </p>
            <p className="text-gray-700 leading-relaxed">
              Synthetic Ascension is purpose-built for this inflection point — delivering the simulation,
              auditability, and speed required to innovate responsibly.
            </p>
          </div>
        </div>

        {/* Industry Verticals */}
        <div className="mb-20 px-4">
          <h2 className="text-2xl font-bold text-center mb-12">Real Use Cases. Real Value.</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {verticals.map((vertical, i) => (
              <FeatureCard key={i} icon={vertical.icon} title={vertical.title} desc={vertical.desc} />
            ))}
          </div>
        </div>

        {/* Impact Section */}
        <div className="bg-gray-100 p-10 rounded-lg shadow-sm max-w-6xl mx-auto mb-20">
          <div className="text-center">
            <h2 className="text-2xl font-bold mb-4">Why This Matters</h2>
            <p className="text-gray-700 max-w-4xl mx-auto leading-relaxed">
              The world's most vulnerable patients are often the least represented in data. We built
              Synthetic Ascension not just for speed or scalability — but to enable safer innovation,
              equitable research, and accessible care. No PHI. No delays. Just progress.
            </p>
          </div>
        </div>

        {/* Final CTA */}
        <div className="text-center px-4">
          <h2 className="text-2xl font-bold mb-4">Join the movement.</h2>
          <p className="text-gray-600 max-w-2xl mx-auto mb-8">
            Synthetic Ascension is already powering dozens of teams across healthcare, life sciences,
            and AI. Be part of the next wave of safer, smarter clinical innovation.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <LeadCaptureModal />
            <Link
              to="/demo"
              className="inline-flex items-center px-8 py-3 border border-purple-600 text-purple-600 font-semibold rounded-lg hover:bg-purple-50 transition-colors"
            >
              Explore Demo
              <ArrowRight className="ml-2 w-5 h-5" />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;