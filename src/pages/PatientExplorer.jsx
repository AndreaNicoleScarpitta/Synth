import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft, User } from 'lucide-react'

const PatientExplorer = () => {
  const [cohortData, setCohortData] = useState([])
  const [selectedPatient, setSelectedPatient] = useState(null)

  useEffect(() => {
    const storedData = localStorage.getItem('cohortData')
    if (storedData) {
      setCohortData(JSON.parse(storedData))
    }
  }, [])

  if (cohortData.length === 0) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <h1 className="heading-syne text-2xl font-bold text-gray-900 mb-4">
            No Patient Data Available
          </h1>
          <Link to="/demo" className="text-primary-600 hover:text-primary-500">
            Generate a cohort first
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <Link
          to="/results"
          className="inline-flex items-center text-primary-600 hover:text-primary-500 mb-4"
        >
          <ArrowLeft className="mr-2 w-4 h-4" />
          Back to Results Overview
        </Link>
        <h1 className="heading-syne text-3xl font-bold text-gray-900">
          Patient Record Explorer
        </h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Patient List */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-sm border">
            <div className="p-4 border-b">
              <h2 className="text-lg font-semibold">Patient Matrix</h2>
            </div>
            <div className="p-4 space-y-2">
              {cohortData.map((patient, index) => (
                <button
                  key={index}
                  onClick={() => setSelectedPatient(patient)}
                  className={`w-full text-left p-3 rounded-md transition-colors ${
                    selectedPatient === patient
                      ? 'bg-primary-100 border-primary-200'
                      : 'bg-gray-50 hover:bg-gray-100'
                  }`}
                >
                  <div className="flex items-center">
                    <User className="w-4 h-4 mr-2 text-gray-500" />
                    <div>
                      <div className="font-medium">Patient {index + 1}</div>
                      <div className="text-sm text-gray-500">
                        {patient.primary_diagnosis}
                      </div>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Patient Details */}
        <div className="lg:col-span-2">
          {selectedPatient ? (
            <div className="bg-white rounded-lg shadow-sm border">
              <div className="p-6">
                <h2 className="text-xl font-semibold mb-6">Patient Details</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="font-medium text-gray-900 mb-3">Demographics</h3>
                    <div className="space-y-2">
                      <div><span className="font-medium">Age:</span> {selectedPatient.age_months} months</div>
                      <div><span className="font-medium">Sex:</span> {selectedPatient.sex}</div>
                      <div><span className="font-medium">Weight:</span> {selectedPatient.weight_kg?.toFixed(1)} kg</div>
                      <div><span className="font-medium">Height:</span> {selectedPatient.height_cm?.toFixed(1)} cm</div>
                    </div>
                  </div>
                  <div>
                    <h3 className="font-medium text-gray-900 mb-3">Clinical Status</h3>
                    {selectedPatient.hemodynamics && (
                      <div className="space-y-2">
                        <div><span className="font-medium">Heart Rate:</span> {selectedPatient.hemodynamics.heart_rate_bpm} bpm</div>
                        <div><span className="font-medium">Blood Pressure:</span> {selectedPatient.hemodynamics.systolic_bp}/{selectedPatient.hemodynamics.diastolic_bp} mmHg</div>
                        <div><span className="font-medium">O2 Saturation:</span> {selectedPatient.hemodynamics.oxygen_saturation}%</div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-lg shadow-sm border p-6 text-center text-gray-500">
              Select a patient from the list to view details
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default PatientExplorer