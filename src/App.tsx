import React from 'react'
import './index.css'

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-md border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center space-x-8">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-600 to-blue-800 flex items-center justify-center">
                  <span className="text-white font-bold text-sm">SA</span>
                </div>
                <div className="font-bold text-xl text-blue-900">
                  Synthetic Ascension
                </div>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="hidden sm:flex items-center space-x-2 text-sm text-gray-500">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span>System Online</span>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="pt-16">
        {/* Hero Section */}
        <section className="relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-purple-600/5 to-blue-800/10"></div>
          <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
            <div className="text-center">
              <h1 className="text-5xl md:text-6xl font-extrabold text-blue-900 mb-6 leading-tight">
                Synthetic Ascension
              </h1>
              <p className="text-2xl font-semibold text-gray-700 mb-4 max-w-3xl mx-auto">
                Simulate. Validate. Ascend.
              </p>
              <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
                Your launchpad to validated, privacy-safe EHR simulation—fueling the next generation of AI, research, and healthtech.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
                <button className="bg-purple-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-purple-700 transition-all duration-200 shadow-lg hover:shadow-xl animate-pulse">
                  Launch Demo →
                </button>
                <button className="border-2 border-purple-600 text-purple-600 px-8 py-3 rounded-lg font-medium hover:bg-purple-600 hover:text-white transition-all duration-200">
                  Design Partnership Interest
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* Features Grid */}
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-blue-900 mb-4">
              Enterprise-Grade Synthetic EHR Platform
            </h2>
            <p className="text-lg text-gray-600 max-w-3xl mx-auto">
              Generate realistic, privacy-compliant patient data with advanced AI validation and comprehensive analytics.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                title: "Synthetic Patient Generation",
                description: "Create realistic patient cohorts with complex medical histories, demographics, and clinical pathways.",
                color: "from-purple-600 to-purple-700"
              },
              {
                title: "Privacy-First Architecture", 
                description: "HIPAA-compliant synthetic data generation with zero risk of patient privacy exposure.",
                color: "from-green-500 to-green-600"
              },
              {
                title: "AI-Powered Validation",
                description: "Advanced statistical validation and bias detection to ensure data quality and representativeness.",
                color: "from-blue-600 to-blue-700"
              },
              {
                title: "Real-time Analytics",
                description: "Interactive dashboards and comprehensive audit trails for complete transparency and control.",
                color: "from-orange-500 to-red-500"
              },
              {
                title: "Scalable Infrastructure",
                description: "Generate cohorts from hundreds to millions of patients with enterprise-grade performance.",
                color: "from-yellow-500 to-orange-500"
              },
              {
                title: "Research Ready",
                description: "Pre-configured templates for clinical trials, drug discovery, and healthcare AI development.",
                color: "from-pink-500 to-rose-500"
              }
            ].map((feature, index) => (
              <div key={index} className="group bg-white rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 border-0 p-6">
                <div className={`w-12 h-12 bg-gradient-to-br ${feature.color} rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                  <div className="w-6 h-6 bg-white rounded"></div>
                </div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </section>

        {/* CTA Section */}
        <section className="bg-gradient-to-r from-purple-600 to-blue-800 text-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
            <div className="text-center">
              <h2 className="text-3xl md:text-4xl font-bold mb-6">
                Ready to Transform Your Healthcare Data?
              </h2>
              <p className="text-xl mb-8 max-w-2xl mx-auto opacity-90">
                Join leading healthcare organizations and research institutions already using Synthetic Ascension.
              </p>
              <button className="bg-white text-blue-800 px-8 py-3 rounded-lg font-medium hover:bg-gray-100 transition-all duration-200 shadow-lg">
                Start Your Demo →
              </button>
            </div>
          </div>
        </section>
      </main>
    </div>
  )
}

export default App