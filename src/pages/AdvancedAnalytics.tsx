import React from 'react'
import { BarChart3, TrendingUp, AlertTriangle, CheckCircle } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export function AdvancedAnalytics() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-8">
        <h1 className="font-syne text-4xl font-bold text-ascension-blue mb-4">
          Advanced Analytics
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl">
          Comprehensive statistical analysis and validation of your synthetic patient cohort.
        </p>
      </div>

      {/* Validation Status */}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-3">
              <CheckCircle className="w-8 h-8 text-biotech-green" />
              <div>
                <div className="text-2xl font-bold text-biotech-green">Pass</div>
                <div className="text-sm text-gray-600">Data Quality</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-3">
              <CheckCircle className="w-8 h-8 text-biotech-green" />
              <div>
                <div className="text-2xl font-bold text-biotech-green">Pass</div>
                <div className="text-sm text-gray-600">Bias Detection</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-3">
              <AlertTriangle className="w-8 h-8 text-yellow-500" />
              <div>
                <div className="text-2xl font-bold text-yellow-500">Review</div>
                <div className="text-sm text-gray-600">Distribution</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-3">
              <CheckCircle className="w-8 h-8 text-biotech-green" />
              <div>
                <div className="text-2xl font-bold text-biotech-green">Pass</div>
                <div className="text-sm text-gray-600">Privacy</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Statistical Summary */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <BarChart3 className="w-5 h-5 text-signal-violet" />
              <span>Statistical Summary</span>
            </CardTitle>
            <CardDescription>
              Key metrics for data validation and quality assessment.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Sample Size</span>
                <span className="font-semibold">1,000 patients</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Mean Age</span>
                <span className="font-semibold">41.3 years</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Gender Distribution</span>
                <span className="font-semibold">52% F, 48% M</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Completion Rate</span>
                <span className="font-semibold text-biotech-green">99.8%</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Data Consistency</span>
                <span className="font-semibold text-biotech-green">98.7%</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Bias Detection */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <AlertTriangle className="w-5 h-5 text-yellow-500" />
              <span>Bias Detection</span>
            </CardTitle>
            <CardDescription>
              Analysis of potential biases in the synthetic data generation.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Age Bias Score</span>
                <span className="font-semibold text-biotech-green">0.02</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Gender Bias Score</span>
                <span className="font-semibold text-biotech-green">0.04</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Ethnic Bias Score</span>
                <span className="font-semibold text-yellow-500">0.12</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Geographic Bias Score</span>
                <span className="font-semibold text-biotech-green">0.03</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Overall Bias Score</span>
                <span className="font-semibold text-biotech-green">0.05</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Distribution Analysis */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <TrendingUp className="w-5 h-5 text-biotech-green" />
              <span>Distribution Analysis</span>
            </CardTitle>
            <CardDescription>
              Statistical distribution validation against real-world data.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span>Age Distribution</span>
                  <span className="text-biotech-green">98.3% Match</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-biotech-green h-2 rounded-full" style={{ width: '98.3%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span>BMI Distribution</span>
                  <span className="text-biotech-green">97.1% Match</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-biotech-green h-2 rounded-full" style={{ width: '97.1%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span>Condition Prevalence</span>
                  <span className="text-yellow-500">89.7% Match</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-yellow-500 h-2 rounded-full" style={{ width: '89.7%' }}></div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Privacy Compliance */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <CheckCircle className="w-5 h-5 text-biotech-green" />
              <span>Privacy Compliance</span>
            </CardTitle>
            <CardDescription>
              HIPAA and privacy regulation compliance verification.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <CheckCircle className="w-5 h-5 text-biotech-green" />
                <span className="text-sm">No real patient data used</span>
              </div>
              <div className="flex items-center space-x-3">
                <CheckCircle className="w-5 h-5 text-biotech-green" />
                <span className="text-sm">Synthetic data only</span>
              </div>
              <div className="flex items-center space-x-3">
                <CheckCircle className="w-5 h-5 text-biotech-green" />
                <span className="text-sm">HIPAA compliant generation</span>
              </div>
              <div className="flex items-center space-x-3">
                <CheckCircle className="w-5 h-5 text-biotech-green" />
                <span className="text-sm">Audit trail maintained</span>
              </div>
              <div className="flex items-center space-x-3">
                <CheckCircle className="w-5 h-5 text-biotech-green" />
                <span className="text-sm">Data anonymization verified</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}