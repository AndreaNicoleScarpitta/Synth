import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Users, BarChart3, Brain, FileText, ArrowLeft } from 'lucide-react'

const ResultsOverview = () => {
  const [cohortData, setCohortData] = useState([])

  useEffect(() => {
    // Load cohort data from localStorage
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
            No Cohort Data Available
          </h1>
          <p className="text-gray-600 mb-6">
            Please generate a cohort first to view results.
          </p>
          <Link
            to="/demo"
            className="inline-flex items-center px-4 py-2 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
          >
            <ArrowLeft className="mr-2 w-4 h-4" />
            Go to Demo Configuration
          </Link>
        </div>
      </div>
    )
  }

  // Calculate metrics
  const totalPatients = cohortData.length
  const conditions = cohortData.map(p => p.primary_diagnosis)
  const uniqueConditions = [...new Set(conditions)].length
  const ages = cohortData.map(p => p.age_months).filter(age => age != null)
  const avgAge = ages.length > 0 ? (ages.reduce((a, b) => a + b, 0) / ages.length).toFixed(1) : 'N/A'
  const maleCount = cohortData.filter(p => p.sex === 'Male').length
  const femaleCount = totalPatients - maleCount

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="heading-syne text-3xl font-bold text-gray-900">
              Cohort Results Overview
            </h1>
            <p className="text-gray-600 mt-2">
              Synthetic patient cohort generated successfully
            </p>
          </div>
          <Link
            to="/demo"
            className="inline-flex items-center px-4 py-2 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            <ArrowLeft className="mr-2 w-4 h-4" />
            Back to Configuration
          </Link>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <MetricCard
          title="Total Patients"
          value={totalPatients}
          icon={<Users className="w-6 h-6" />}
        />
        <MetricCard
          title="Unique Conditions"
          value={uniqueConditions}
          icon={<BarChart3 className="w-6 h-6" />}
        />
        <MetricCard
          title="Avg Age (months)"
          value={avgAge}
          icon={<Brain className="w-6 h-6" />}
        />
        <MetricCard
          title="Male/Female"
          value={`${maleCount}/${femaleCount}`}
          icon={<FileText className="w-6 h-6" />}
        />
      </div>

      {/* Navigation Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <NavigationCard
          title="Patient Record Explorer"
          description="Browse individual synthetic patient records with detailed clinical data"
          icon={<Users className="w-8 h-8" />}
          href="/patients"
          primary
        />
        <NavigationCard
          title="Advanced Analytics"
          description="Statistical analysis and demographic distribution charts"
          icon={<BarChart3 className="w-8 h-8" />}
          href="/analytics"
        />
        <NavigationCard
          title="ML/AI Analytics"
          description="Machine learning insights and AI agent reasoning patterns"
          icon={<Brain className="w-8 h-8" />}
          href="/ml"
        />
        <NavigationCard
          title="Audit Trails"
          description="Complete generation logs and validation audit trails"
          icon={<FileText className="w-8 h-8" />}
          href="/audit"
        />
      </div>
    </div>
  )
}

const MetricCard = ({ title, value, icon }) => {
  return (
    <div className="bg-white rounded-lg p-6 shadow-sm border">
      <div className="flex items-center">
        <div className="text-primary-600 mr-4">{icon}</div>
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
      </div>
    </div>
  )
}

const NavigationCard = ({ title, description, icon, href, primary = false }) => {
  return (
    <Link
      to={href}
      className={`block p-6 rounded-lg border transition-all hover:shadow-md ${
        primary 
          ? 'bg-primary-50 border-primary-200 hover:bg-primary-100' 
          : 'bg-white border-gray-200 hover:border-gray-300'
      }`}
    >
      <div className={`${primary ? 'text-primary-600' : 'text-gray-600'} mb-4`}>
        {icon}
      </div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </Link>
  )
}

export default ResultsOverview