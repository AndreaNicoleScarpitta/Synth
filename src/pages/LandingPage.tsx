import { Link } from 'react-router-dom'
import { Shield, Zap, Database, Activity, Brain, Mail, User, Beaker } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { DNALogo } from '@/components/DNALogo'
import { MatrixBackground } from '@/components/MatrixBackground'

export function LandingPage() {
  return (
    <div className="min-h-screen bg-black-950 text-gold-400 relative">
      <MatrixBackground />
      
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-black-900/80 to-black-950/90"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
          <div className="text-center">
            {/* DNA Logo */}
            <div className="flex justify-center mb-8">
              <DNALogo size="xl" className="animate-float" />
            </div>
            
            <h1 className="font-syne text-5xl md:text-7xl font-extrabold text-gold-400 mb-6 leading-tight animate-glow-pulse">
              Synthetic Ascension
            </h1>
            <p className="text-2xl font-syne font-semibold text-gold-300 mb-4 max-w-3xl mx-auto">
              Decode. Synthesize. Evolve.
            </p>
            <p className="text-lg font-inter text-gold-200/80 mb-8 max-w-2xl mx-auto">
              Next-generation synthetic EHR platform powered by AI—where genetic data meets matrix intelligence.
            </p>
            
            {/* Early Sign Up CTA */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
              <Button 
                asChild 
                className="bg-gradient-to-r from-gold-500 to-gold-600 hover:from-gold-400 hover:to-gold-500 text-black-950 font-bold py-3 px-8 rounded-lg shadow-lg animate-glow-pulse"
                size="xl"
              >
                <Link to="/signup">
                  <User className="mr-2 w-5 h-5" />
                  Get Early Access
                </Link>
              </Button>
              <Button 
                variant="outline" 
                size="xl"
                className="border-gold-400 text-gold-400 hover:bg-gold-400/10"
              >
                <Mail className="mr-2 w-5 h-5" />
                Join Waitlist
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-16">
          <h2 className="font-syne text-3xl md:text-4xl font-bold text-gold-400 mb-4">
            Matrix-Grade Synthetic Intelligence
          </h2>
          <p className="text-lg text-gold-200/80 max-w-3xl mx-auto">
            Harness the power of genetic algorithms and neural networks to generate unprecedented synthetic medical data.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <Card className="group hover:shadow-2xl transition-all duration-500 bg-black-900/50 border border-gold-600/20 backdrop-blur-sm hover:border-gold-400/40">
            <CardHeader>
              <div className="w-12 h-12 bg-gradient-to-br from-gold-500 to-gold-600 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform animate-glow-pulse">
                <Database className="w-6 h-6 text-black-950" />
              </div>
              <CardTitle className="font-syne text-xl text-gold-300">Neural EHR Genesis</CardTitle>
              <CardDescription className="text-gold-200/70">
                Generate hyper-realistic patient cohorts using advanced genetic algorithms and deep neural networks.
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="group hover:shadow-2xl transition-all duration-500 bg-black-900/50 border border-gold-600/20 backdrop-blur-sm hover:border-gold-400/40">
            <CardHeader>
              <div className="w-12 h-12 bg-gradient-to-br from-gold-500 to-gold-600 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform animate-glow-pulse">
                <Shield className="w-6 h-6 text-black-950" />
              </div>
              <CardTitle className="font-syne text-xl text-gold-300">Quantum Privacy Shield</CardTitle>
              <CardDescription className="text-gold-200/70">
                Unhackable privacy architecture with quantum-encrypted synthetic data generation protocols.
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="group hover:shadow-2xl transition-all duration-500 bg-black-900/50 border border-gold-600/20 backdrop-blur-sm hover:border-gold-400/40">
            <CardHeader>
              <div className="w-12 h-12 bg-gradient-to-br from-gold-500 to-gold-600 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform animate-glow-pulse">
                <Brain className="w-6 h-6 text-black-950" />
              </div>
              <CardTitle className="font-syne text-xl text-gold-300">AI Consciousness Engine</CardTitle>
              <CardDescription className="text-gold-200/70">
                Self-learning validation systems that evolve with your data, ensuring unprecedented accuracy.
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="group hover:shadow-2xl transition-all duration-500 bg-black-900/50 border border-gold-600/20 backdrop-blur-sm hover:border-gold-400/40">
            <CardHeader>
              <div className="w-12 h-12 bg-gradient-to-br from-gold-500 to-gold-600 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform animate-glow-pulse">
                <Activity className="w-6 h-6 text-black-950" />
              </div>
              <CardTitle className="font-syne text-xl text-gold-300">Holographic Analytics</CardTitle>
              <CardDescription className="text-gold-200/70">
                Multi-dimensional data visualization with real-time matrix-style analytical interfaces.
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="group hover:shadow-2xl transition-all duration-500 bg-black-900/50 border border-gold-600/20 backdrop-blur-sm hover:border-gold-400/40">
            <CardHeader>
              <div className="w-12 h-12 bg-gradient-to-br from-gold-500 to-gold-600 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform animate-glow-pulse">
                <Zap className="w-6 h-6 text-black-950" />
              </div>
              <CardTitle className="font-syne text-xl text-gold-300">Infinite Scalability</CardTitle>
              <CardDescription className="text-gold-200/70">
                Cloud-native architecture capable of generating billions of synthetic patients instantaneously.
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="group hover:shadow-2xl transition-all duration-500 bg-black-900/50 border border-gold-600/20 backdrop-blur-sm hover:border-gold-400/40">
            <CardHeader>
              <div className="w-12 h-12 bg-gradient-to-br from-gold-500 to-gold-600 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform animate-glow-pulse">
                <Beaker className="w-6 h-6 text-black-950" />
              </div>
              <CardTitle className="font-syne text-xl text-gold-300">Research Nexus</CardTitle>
              <CardDescription className="text-gold-200/70">
                Pre-loaded with genetic markers and clinical pathways for breakthrough medical research.
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="relative bg-gradient-to-r from-black-950 via-black-900 to-black-950">
        <div className="absolute inset-0 bg-gradient-to-r from-gold-600/10 via-gold-500/5 to-gold-600/10"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <div className="flex justify-center mb-6">
              <DNALogo size="lg" className="animate-dna-helix" />
            </div>
            <h2 className="font-syne text-3xl md:text-4xl font-bold mb-6 text-gold-400">
              Ascend to the Next Level
            </h2>
            <p className="text-xl mb-8 max-w-2xl mx-auto text-gold-200/80">
              Join the matrix of medical intelligence. Your synthetic evolution begins now.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                asChild 
                className="bg-gradient-to-r from-gold-500 to-gold-600 hover:from-gold-400 hover:to-gold-500 text-black-950 font-bold py-3 px-8 rounded-lg shadow-xl animate-glow-pulse"
                size="xl"
              >
                <Link to="/signup">
                  <User className="mr-2 w-5 h-5" />
                  Enter the Matrix
                </Link>
              </Button>
              <Button 
                variant="outline"
                size="xl"
                className="border-gold-400 text-gold-400 hover:bg-gold-400/10 hover:border-gold-300"
              >
                <Mail className="mr-2 w-5 h-5" />
                Request Access
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}