import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Beaker, BarChart3, Users, Brain, FileText, Home } from 'lucide-react'

const Navigation = () => {
  const location = useLocation()

  const navItems = [
    { path: '/', icon: Home, label: 'Home' },
    { path: '/demo', icon: Beaker, label: 'Demo Config' },
    { path: '/results', icon: BarChart3, label: 'Results' },
    { path: '/patients', icon: Users, label: 'Patients' },
    { path: '/analytics', icon: BarChart3, label: 'Analytics' },
    { path: '/ml', icon: Brain, label: 'ML/AI' },
    { path: '/audit', icon: FileText, label: 'Audit' }
  ]

  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">SA</span>
              </div>
              <span className="heading-syne text-xl font-bold text-gray-900">
                Synthetic Ascension
              </span>
            </Link>
          </div>
          
          <div className="flex items-center space-x-4">
            {navItems.map(({ path, icon: Icon, label }) => (
              <Link
                key={path}
                to={path}
                className={`flex items-center space-x-1 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  location.pathname === path
                    ? 'bg-primary-100 text-primary-700'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navigation