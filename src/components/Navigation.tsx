import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { 
  Beaker, 
  BarChart3, 
  Users, 
  Brain, 
  FileText, 
  Settings,
  Activity
} from 'lucide-react'
import { cn } from '@/lib/utils'

const navItems = [
  { path: '/', icon: Activity, label: 'Overview' },
  { path: '/demo', icon: Settings, label: 'Configure' },
  { path: '/results', icon: BarChart3, label: 'Results' },
  { path: '/patients', icon: Users, label: 'Patients' },
  { path: '/analytics', icon: Beaker, label: 'Analytics' },
  { path: '/ml', icon: Brain, label: 'ML Insights' },
  { path: '/audit', icon: FileText, label: 'Audit' }
]

export function Navigation() {
  const location = useLocation()

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-md border-b border-gray-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center space-x-8">
            <Link to="/" className="flex items-center space-x-3">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-signal-violet to-ascension-blue flex items-center justify-center">
                <span className="text-white font-bold text-sm">SA</span>
              </div>
              <div className="font-syne font-bold text-xl text-ascension-blue">
                Synthetic Ascension
              </div>
            </Link>
            
            <div className="hidden md:flex items-center space-x-1">
              {navItems.map(({ path, icon: Icon, label }) => (
                <Link
                  key={path}
                  to={path}
                  className={cn(
                    "flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200",
                    location.pathname === path
                      ? 'bg-signal-violet text-white shadow-lg shadow-signal-violet/25'
                      : 'text-gray-600 hover:text-signal-violet hover:bg-gray-50'
                  )}
                >
                  <Icon className="w-4 h-4" />
                  <span>{label}</span>
                </Link>
              ))}
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="hidden sm:flex items-center space-x-2 text-sm text-gray-500">
              <div className="w-2 h-2 bg-biotech-green rounded-full animate-pulse"></div>
              <span>System Online</span>
            </div>
          </div>
        </div>
      </div>
    </nav>
  )
}