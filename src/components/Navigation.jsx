import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Beaker, BarChart3, Users, Brain, FileText, Home } from 'lucide-react'
import ThemeToggle from './ThemeToggle'

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
    <nav className="shadow-sm border-b border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800 transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 rounded-lg bg-primary-500 flex items-center justify-center">
                <span className="text-white font-bold text-sm">SA</span>
              </div>
              <span className="font-heading text-xl font-bold text-neutral-900 dark:text-white">
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
                    ? 'text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/20'
                    : 'text-neutral-600 dark:text-neutral-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-neutral-100 dark:hover:bg-neutral-700'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{label}</span>
              </Link>
            ))}
            <ThemeToggle />
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navigation