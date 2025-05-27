import React from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft, FileText } from 'lucide-react'

const AuditTrails = () => {
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
          Audit Trails
        </h1>
        <p className="text-gray-600 mt-2">
          Complete generation logs and validation audit trails
        </p>
      </div>

      <div className="bg-white rounded-lg shadow-sm border p-8 text-center">
        <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-gray-900 mb-2">
          Audit Trails Coming Soon
        </h2>
        <p className="text-gray-600 mb-6">
          This section will provide comprehensive audit logs, generation 
          transparency, and regulatory compliance documentation.
        </p>
        <div className="text-sm text-gray-500">
          Features in development:
          <ul className="mt-2 space-y-1">
            <li>• Complete generation audit logs</li>
            <li>• AI decision traceability</li>
            <li>• Regulatory compliance reports</li>
            <li>• Data lineage tracking</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default AuditTrails