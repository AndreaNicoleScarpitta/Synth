import React from 'react'
import { Link } from 'react-router-dom'
import { ArrowRight, Beaker, Shield, Zap, Database, Activity, Brain } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export function LandingPage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-signal-violet/5 to-ascension-blue/10"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
          <div className="text-center">
            <h1 className="font-syne text-5xl md:text-6xl font-extrabold text-ascension-blue mb-6 leading-tight">
              Synthetic Ascension
            </h1>
            <p className="text-2xl font-syne font-semibold text-slate-gray mb-4 max-w-3xl mx-auto">
              Simulate. Validate. Ascend.
            </p>
            <p className="text-lg font-inter text-gray-600 mb-8 max-w-2xl mx-auto">
              Your launchpad to validated, privacy-safe EHR simulation—fueling the next generation of AI, research, and healthtech.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
              <Button asChild variant="brand" size="xl" className="animate-pulse-glow">
                <Link to="/demo">
                  Launch Demo
                  <ArrowRight className="ml-2 w-5 h-5" />
                </Link>
              </Button>
              <Button variant="brandOutline" size="xl">
                Design Partnership Interest
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-16">
          <h2 className="font-syne text-3xl md:text-4xl font-bold text-ascension-blue mb-4">
            Enterprise-Grade Synthetic EHR Platform
          </h2>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Generate realistic, privacy-compliant patient data with advanced AI validation and comprehensive analytics.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <Card className="group hover:shadow-xl transition-all duration-300 border-0 shadow-lg">
            <CardHeader>
              <div className="w-12 h-12 bg-gradient-to-br from-signal-violet to-purple-600 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <Database className="w-6 h-6 text-white" />
              </div>
              <CardTitle className="font-syne text-xl">Synthetic Patient Generation</CardTitle>
              <CardDescription>
                Create realistic patient cohorts with complex medical histories, demographics, and clinical pathways.
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="group hover:shadow-xl transition-all duration-300 border-0 shadow-lg">
            <CardHeader>
              <div className="w-12 h-12 bg-gradient-to-br from-biotech-green to-green-600 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <CardTitle className="font-syne text-xl">Privacy-First Architecture</CardTitle>
              <CardDescription>
                HIPAA-compliant synthetic data generation with zero risk of patient privacy exposure.
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="group hover:shadow-xl transition-all duration-300 border-0 shadow-lg">
            <CardHeader>
              <div className="w-12 h-12 bg-gradient-to-br from-ascension-blue to-blue-600 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <CardTitle className="font-syne text-xl">AI-Powered Validation</CardTitle>
              <CardDescription>
                Advanced statistical validation and bias detection to ensure data quality and representativeness.
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="group hover:shadow-xl transition-all duration-300 border-0 shadow-lg">
            <CardHeader>
              <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-red-500 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <Activity className="w-6 h-6 text-white" />
              </div>
              <CardTitle className="font-syne text-xl">Real-time Analytics</CardTitle>
              <CardDescription>
                Interactive dashboards and comprehensive audit trails for complete transparency and control.
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="group hover:shadow-xl transition-all duration-300 border-0 shadow-lg">
            <CardHeader>
              <div className="w-12 h-12 bg-gradient-to-br from-yellow-500 to-orange-500 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <Zap className="w-6 h-6 text-white" />
              </div>
              <CardTitle className="font-syne text-xl">Scalable Infrastructure</CardTitle>
              <CardDescription>
                Generate cohorts from hundreds to millions of patients with enterprise-grade performance.
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="group hover:shadow-xl transition-all duration-300 border-0 shadow-lg">
            <CardHeader>
              <div className="w-12 h-12 bg-gradient-to-br from-pink-500 to-rose-500 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <Beaker className="w-6 h-6 text-white" />
              </div>
              <CardTitle className="font-syne text-xl">Research Ready</CardTitle>
              <CardDescription>
                Pre-configured templates for clinical trials, drug discovery, and healthcare AI development.
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-signal-violet to-ascension-blue text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <h2 className="font-syne text-3xl md:text-4xl font-bold mb-6">
              Ready to Transform Your Healthcare Data?
            </h2>
            <p className="text-xl mb-8 max-w-2xl mx-auto opacity-90">
              Join leading healthcare organizations and research institutions already using Synthetic Ascension.
            </p>
            <Button asChild variant="secondary" size="xl" className="bg-white text-ascension-blue hover:bg-gray-100">
              <Link to="/demo">
                Start Your Demo
                <ArrowRight className="ml-2 w-5 h-5" />
              </Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  )
}