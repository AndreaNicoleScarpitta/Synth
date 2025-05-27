import React from 'react'
import { FileText, Clock, User, Shield } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export function AuditTrails() {
  const auditLogs = [
    {
      id: '1',
      timestamp: '2024-01-15 14:32:18',
      action: 'Cohort Generation Started',
      user: 'System',
      details: 'Initiated generation of 1,000 patient cohort',
      status: 'completed'
    },
    {
      id: '2',
      timestamp: '2024-01-15 14:34:22',
      action: 'Data Validation',
      user: 'AI Validator',
      details: 'Statistical validation completed with 98.7% accuracy',
      status: 'completed'
    },
    {
      id: '3',
      timestamp: '2024-01-15 14:35:10',
      action: 'Bias Detection',
      user: 'AI Validator',
      details: 'Bias analysis completed, overall score: 0.05',
      status: 'completed'
    },
    {
      id: '4',
      timestamp: '2024-01-15 14:35:45',
      action: 'Privacy Compliance Check',
      user: 'System',
      details: 'HIPAA compliance verified for all generated records',
      status: 'completed'
    },
    {
      id: '5',
      timestamp: '2024-01-15 14:36:12',
      action: 'Data Export',
      user: 'user@example.com',
      details: 'Patient cohort exported in CSV format',
      status: 'completed'
    }
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-biotech-green'
      case 'pending':
        return 'text-yellow-500'
      case 'failed':
        return 'text-red-500'
      default:
        return 'text-gray-500'
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-8">
        <h1 className="font-syne text-4xl font-bold text-ascension-blue mb-4">
          Audit Trails & Compliance
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl">
          Complete audit trail of all activities, ensuring full transparency and regulatory compliance.
        </p>
      </div>

      <div className="grid lg:grid-cols-4 gap-6 mb-8">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-3">
              <FileText className="w-8 h-8 text-signal-violet" />
              <div>
                <div className="text-2xl font-bold text-ascension-blue">127</div>
                <div className="text-sm text-gray-600">Total Events</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-3">
              <Clock className="w-8 h-8 text-biotech-green" />
              <div>
                <div className="text-2xl font-bold text-ascension-blue">24h</div>
                <div className="text-sm text-gray-600">Retention</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-3">
              <User className="w-8 h-8 text-ascension-blue" />
              <div>
                <div className="text-2xl font-bold text-ascension-blue">3</div>
                <div className="text-sm text-gray-600">Active Users</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-3">
              <Shield className="w-8 h-8 text-biotech-green" />
              <div>
                <div className="text-2xl font-bold text-biotech-green">100%</div>
                <div className="text-sm text-gray-600">Compliant</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Audit Log */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Recent Activity</CardTitle>
              <CardDescription>
                Chronological log of all system activities and user actions.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4 max-h-96 overflow-y-auto">
                {auditLogs.map((log) => (
                  <div key={log.id} className="border-l-4 border-signal-violet pl-4 py-2">
                    <div className="flex justify-between items-start">
                      <div>
                        <div className="font-semibold text-ascension-blue">{log.action}</div>
                        <div className="text-sm text-gray-600 mt-1">{log.details}</div>
                        <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                          <span className="flex items-center space-x-1">
                            <Clock className="w-3 h-3" />
                            <span>{log.timestamp}</span>
                          </span>
                          <span className="flex items-center space-x-1">
                            <User className="w-3 h-3" />
                            <span>{log.user}</span>
                          </span>
                        </div>
                      </div>
                      <div className={`text-sm font-medium ${getStatusColor(log.status)}`}>
                        {log.status.toUpperCase()}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Compliance Status */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Compliance Status</CardTitle>
              <CardDescription>
                Current compliance with healthcare regulations.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <Shield className="w-5 h-5 text-biotech-green" />
                  <div>
                    <div className="font-semibold">HIPAA Compliant</div>
                    <div className="text-sm text-gray-600">Privacy rules verified</div>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <Shield className="w-5 h-5 text-biotech-green" />
                  <div>
                    <div className="font-semibold">SOX Compliant</div>
                    <div className="text-sm text-gray-600">Financial controls in place</div>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <Shield className="w-5 h-5 text-biotech-green" />
                  <div>
                    <div className="font-semibold">GDPR Compliant</div>
                    <div className="text-sm text-gray-600">Data protection verified</div>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <Shield className="w-5 h-5 text-biotech-green" />
                  <div>
                    <div className="font-semibold">21 CFR Part 11</div>
                    <div className="text-sm text-gray-600">Electronic records compliant</div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Data Lineage</CardTitle>
              <CardDescription>
                Complete traceability of data generation process.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-signal-violet rounded-full"></div>
                  <span className="text-sm">Source Model: GPT-4 Medical</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-biotech-green rounded-full"></div>
                  <span className="text-sm">Validation: Statistical Models</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-ascension-blue rounded-full"></div>
                  <span className="text-sm">Output: Synthetic Cohort v1.0</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                  <span className="text-sm">Storage: Encrypted Database</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Security Events</CardTitle>
              <CardDescription>
                Security-related activities and alerts.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8">
                <Shield className="w-12 h-12 text-biotech-green mx-auto mb-3" />
                <div className="text-sm text-gray-600">
                  No security incidents detected
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  Last scan: 2 minutes ago
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}