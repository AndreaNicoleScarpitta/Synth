import React from 'react'
import { Link } from 'react-router-dom'
import { Download, Eye, BarChart3, Users, ArrowRight } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { useAppStore } from '@/store/useAppStore'

export function ResultsOverview() {
  const { cohortConfig, generatedData } = useAppStore()

  const stats = [
    { label: 'Total Patients', value: cohortConfig.size.toLocaleString(), icon: Users },
    { label: 'Age Range', value: `${cohortConfig.ageRange[0]}-${cohortConfig.ageRange[1]} years`, icon: BarChart3 },
    { label: 'Conditions', value: cohortConfig.conditions.length, icon: Eye },
    { label: 'Data Points', value: '45,230', icon: Download }
  ]

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center mb-12">
        <div className="inline-flex items-center space-x-2 bg-biotech-green/10 text-biotech-green px-4 py-2 rounded-full text-sm font-medium mb-4">
          <div className="w-2 h-2 bg-biotech-green rounded-full animate-pulse"></div>
          <span>Generation Complete</span>
        </div>
        <h1 className="font-syne text-4xl font-bold text-ascension-blue mb-4">
          Synthetic Cohort Generated Successfully
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Your synthetic patient cohort has been generated with advanced AI validation. 
          Explore the data, run analytics, and export results.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        {stats.map(({ label, value, icon: Icon }) => (
          <Card key={label} className="text-center">
            <CardContent className="pt-6">
              <div className="w-12 h-12 bg-gradient-to-br from-signal-violet to-purple-600 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Icon className="w-6 h-6 text-white" />
              </div>
              <div className="text-2xl font-bold text-ascension-blue mb-1">{value}</div>
              <div className="text-sm text-gray-600">{label}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Action Cards */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <Card className="group hover:shadow-xl transition-all duration-300">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Users className="w-5 h-5 text-signal-violet" />
              <span>Patient Explorer</span>
            </CardTitle>
            <CardDescription>
              Browse individual patient records and medical histories in detail.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild variant="brand" className="w-full">
              <Link to="/patients">
                Explore Patients
                <ArrowRight className="ml-2 w-4 h-4" />
              </Link>
            </Button>
          </CardContent>
        </Card>

        <Card className="group hover:shadow-xl transition-all duration-300">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <BarChart3 className="w-5 h-5 text-biotech-green" />
              <span>Advanced Analytics</span>
            </CardTitle>
            <CardDescription>
              Statistical analysis, distribution validation, and bias detection.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild variant="brandOutline" className="w-full">
              <Link to="/analytics">
                View Analytics
                <ArrowRight className="ml-2 w-4 h-4" />
              </Link>
            </Button>
          </CardContent>
        </Card>

        <Card className="group hover:shadow-xl transition-all duration-300">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Download className="w-5 h-5 text-ascension-blue" />
              <span>Export Data</span>
            </CardTitle>
            <CardDescription>
              Download your synthetic cohort in multiple formats for analysis.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            <Button variant="outline" className="w-full text-sm">
              Download CSV
            </Button>
            <Button variant="outline" className="w-full text-sm">
              Download JSON
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Data Quality Summary */}
      <Card className="mt-12">
        <CardHeader>
          <CardTitle>Data Quality Summary</CardTitle>
          <CardDescription>
            Comprehensive validation results for your synthetic cohort.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-biotech-green mb-2">98.7%</div>
              <div className="text-sm text-gray-600">Statistical Accuracy</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-biotech-green mb-2">0.03</div>
              <div className="text-sm text-gray-600">Bias Score</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-biotech-green mb-2">99.9%</div>
              <div className="text-sm text-gray-600">Privacy Compliance</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}