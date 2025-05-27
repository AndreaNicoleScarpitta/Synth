import React, { useState } from 'react'
import { Search, Filter, Eye, Download } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export function PatientExplorer() {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedPatient, setSelectedPatient] = useState<string | null>(null)

  // Mock patient data - would come from API in real implementation
  const patients = [
    {
      id: 'P001',
      name: 'Patient 001',
      age: 45,
      gender: 'Female',
      conditions: ['Hypertension', 'Type 2 Diabetes'],
      lastVisit: '2024-01-15'
    },
    {
      id: 'P002',
      name: 'Patient 002',
      age: 32,
      gender: 'Male',
      conditions: ['Asthma'],
      lastVisit: '2024-01-12'
    },
    {
      id: 'P003',
      name: 'Patient 003',
      age: 67,
      gender: 'Female',
      conditions: ['Cardiovascular Disease', 'Hypertension'],
      lastVisit: '2024-01-10'
    }
  ]

  const filteredPatients = patients.filter(patient =>
    patient.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
    patient.conditions.some(condition => 
      condition.toLowerCase().includes(searchTerm.toLowerCase())
    )
  )

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-8">
        <h1 className="font-syne text-4xl font-bold text-ascension-blue mb-4">
          Patient Explorer
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl">
          Browse and analyze individual synthetic patient records with detailed medical histories and demographics.
        </p>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Patient List */}
        <div className="lg:col-span-1 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Search Patients</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  type="text"
                  placeholder="Search by ID or condition..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-signal-violet focus:border-transparent"
                />
              </div>
              <div className="flex items-center space-x-2 mt-4">
                <Button variant="outline" size="sm">
                  <Filter className="w-4 h-4 mr-2" />
                  Filters
                </Button>
                <span className="text-sm text-gray-500">
                  {filteredPatients.length} patients
                </span>
              </div>
            </CardContent>
          </Card>

          <div className="space-y-3 max-h-96 overflow-y-auto">
            {filteredPatients.map((patient) => (
              <Card
                key={patient.id}
                className={`cursor-pointer transition-all duration-200 ${
                  selectedPatient === patient.id
                    ? 'ring-2 ring-signal-violet bg-signal-violet/5'
                    : 'hover:shadow-md'
                }`}
                onClick={() => setSelectedPatient(patient.id)}
              >
                <CardContent className="p-4">
                  <div className="flex justify-between items-start">
                    <div>
                      <div className="font-semibold text-ascension-blue">{patient.id}</div>
                      <div className="text-sm text-gray-600">
                        {patient.age}y • {patient.gender}
                      </div>
                    </div>
                    <div className="text-xs text-gray-500">{patient.lastVisit}</div>
                  </div>
                  <div className="mt-2">
                    {patient.conditions.map((condition, index) => (
                      <span
                        key={index}
                        className="inline-block bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs mr-1 mb-1"
                      >
                        {condition}
                      </span>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Patient Details */}
        <div className="lg:col-span-2">
          {selectedPatient ? (
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle className="text-2xl">Patient {selectedPatient}</CardTitle>
                      <CardDescription>Synthetic patient record</CardDescription>
                    </div>
                    <div className="flex space-x-2">
                      <Button variant="outline" size="sm">
                        <Eye className="w-4 h-4 mr-2" />
                        View Full Record
                      </Button>
                      <Button variant="outline" size="sm">
                        <Download className="w-4 h-4 mr-2" />
                        Export
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <h3 className="font-semibold text-ascension-blue mb-3">Demographics</h3>
                      <div className="space-y-2 text-sm">
                        <div><span className="text-gray-600">Age:</span> 45 years</div>
                        <div><span className="text-gray-600">Gender:</span> Female</div>
                        <div><span className="text-gray-600">Ethnicity:</span> Caucasian</div>
                        <div><span className="text-gray-600">BMI:</span> 28.3</div>
                      </div>
                    </div>
                    <div>
                      <h3 className="font-semibold text-ascension-blue mb-3">Contact Info</h3>
                      <div className="space-y-2 text-sm">
                        <div><span className="text-gray-600">City:</span> Springfield</div>
                        <div><span className="text-gray-600">State:</span> IL</div>
                        <div><span className="text-gray-600">Insurance:</span> Blue Cross</div>
                        <div><span className="text-gray-600">Provider:</span> Dr. Smith</div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Medical History</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="border-l-4 border-signal-violet pl-4">
                      <div className="font-semibold">Hypertension</div>
                      <div className="text-sm text-gray-600">Diagnosed: March 2022</div>
                      <div className="text-sm">Managed with Lisinopril 10mg daily</div>
                    </div>
                    <div className="border-l-4 border-biotech-green pl-4">
                      <div className="font-semibold">Type 2 Diabetes</div>
                      <div className="text-sm text-gray-600">Diagnosed: January 2023</div>
                      <div className="text-sm">HbA1c: 7.2%, Metformin 500mg BID</div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Recent Lab Results</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-3 gap-4">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-ascension-blue">7.2%</div>
                      <div className="text-sm text-gray-600">HbA1c</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-ascension-blue">145/90</div>
                      <div className="text-sm text-gray-600">Blood Pressure</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-ascension-blue">220</div>
                      <div className="text-sm text-gray-600">Total Cholesterol</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          ) : (
            <Card className="h-96 flex items-center justify-center">
              <CardContent className="text-center">
                <Eye className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-600 mb-2">
                  Select a Patient
                </h3>
                <p className="text-gray-500">
                  Choose a patient from the list to view their detailed medical record.
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}