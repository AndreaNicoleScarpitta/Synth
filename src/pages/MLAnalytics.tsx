import React from 'react'
import { Brain, Zap, Target, TrendingUp } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export function MLAnalytics() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-8">
        <h1 className="font-syne text-4xl font-bold text-ascension-blue mb-4">
          ML Insights & Validation
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl">
          Advanced machine learning analytics and AI-powered validation of synthetic data quality.
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Model Performance */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Brain className="w-5 h-5 text-signal-violet" />
              <span>Generation Model Performance</span>
            </CardTitle>
            <CardDescription>
              Performance metrics for the AI models used in synthetic data generation.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span>Patient Demographics Model</span>
                  <span className="text-biotech-green">96.8%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-biotech-green h-2 rounded-full" style={{ width: '96.8%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span>Medical History Model</span>
                  <span className="text-biotech-green">94.2%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-biotech-green h-2 rounded-full" style={{ width: '94.2%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span>Lab Results Model</span>
                  <span className="text-biotech-green">98.1%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-biotech-green h-2 rounded-full" style={{ width: '98.1%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span>Medication Model</span>
                  <span className="text-yellow-500">91.7%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-yellow-500 h-2 rounded-full" style={{ width: '91.7%' }}></div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Validation Scores */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Target className="w-5 h-5 text-biotech-green" />
              <span>AI Validation Scores</span>
            </CardTitle>
            <CardDescription>
              Automated quality assessment using advanced validation algorithms.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Realism Score</span>
                <div className="flex items-center space-x-2">
                  <span className="font-semibold text-biotech-green">9.4/10</span>
                  <div className="w-16 bg-gray-200 rounded-full h-2">
                    <div className="bg-biotech-green h-2 rounded-full" style={{ width: '94%' }}></div>
                  </div>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Consistency Score</span>
                <div className="flex items-center space-x-2">
                  <span className="font-semibold text-biotech-green">9.7/10</span>
                  <div className="w-16 bg-gray-200 rounded-full h-2">
                    <div className="bg-biotech-green h-2 rounded-full" style={{ width: '97%' }}></div>
                  </div>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Diversity Score</span>
                <div className="flex items-center space-x-2">
                  <span className="font-semibold text-yellow-500">8.9/10</span>
                  <div className="w-16 bg-gray-200 rounded-full h-2">
                    <div className="bg-yellow-500 h-2 rounded-full" style={{ width: '89%' }}></div>
                  </div>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Privacy Score</span>
                <div className="flex items-center space-x-2">
                  <span className="font-semibold text-biotech-green">10/10</span>
                  <div className="w-16 bg-gray-200 rounded-full h-2">
                    <div className="bg-biotech-green h-2 rounded-full" style={{ width: '100%' }}></div>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Feature Importance */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <TrendingUp className="w-5 h-5 text-ascension-blue" />
              <span>Feature Importance Analysis</span>
            </CardTitle>
            <CardDescription>
              Most influential features in the synthetic data generation process.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Age</span>
                  <span>0.23</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-signal-violet h-2 rounded-full" style={{ width: '23%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Medical History</span>
                  <span>0.19</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-signal-violet h-2 rounded-full" style={{ width: '19%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>BMI</span>
                  <span>0.16</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-signal-violet h-2 rounded-full" style={{ width: '16%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Geographic Location</span>
                  <span>0.14</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-signal-violet h-2 rounded-full" style={{ width: '14%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Insurance Type</span>
                  <span>0.12</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-signal-violet h-2 rounded-full" style={{ width: '12%' }}></div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Quality Metrics */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Zap className="w-5 h-5 text-yellow-500" />
              <span>Quality Metrics</span>
            </CardTitle>
            <CardDescription>
              Comprehensive quality assessment of generated synthetic data.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-biotech-green mb-1">A+</div>
                <div className="text-sm text-gray-600">Overall Grade</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-ascension-blue mb-1">0.03</div>
                <div className="text-sm text-gray-600">Error Rate</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-signal-violet mb-1">98.7%</div>
                <div className="text-sm text-gray-600">Accuracy</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-yellow-500 mb-1">1.2s</div>
                <div className="text-sm text-gray-600">Avg Gen Time</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Model Architecture */}
      <Card className="mt-8">
        <CardHeader>
          <CardTitle>AI Model Architecture</CardTitle>
          <CardDescription>
            Technical details of the machine learning models used for synthetic data generation.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-signal-violet to-purple-600 rounded-lg flex items-center justify-center mx-auto mb-3">
                <Brain className="w-8 h-8 text-white" />
              </div>
              <h3 className="font-semibold mb-2">Transformer Networks</h3>
              <p className="text-sm text-gray-600">
                Advanced attention mechanisms for realistic patient data generation
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-biotech-green to-green-600 rounded-lg flex items-center justify-center mx-auto mb-3">
                <Target className="w-8 h-8 text-white" />
              </div>
              <h3 className="font-semibold mb-2">GAN Architecture</h3>
              <p className="text-sm text-gray-600">
                Generative adversarial networks for high-quality synthetic data
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-ascension-blue to-blue-600 rounded-lg flex items-center justify-center mx-auto mb-3">
                <Zap className="w-8 h-8 text-white" />
              </div>
              <h3 className="font-semibold mb-2">Validation Models</h3>
              <p className="text-sm text-gray-600">
                Multi-layer validation for quality assurance and bias detection
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}