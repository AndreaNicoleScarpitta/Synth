import React from 'react'

export const SyntheticLogo = ({ className = "" }: { className?: string }) => {
  return (
    <div className={`flex items-center gap-3 ${className}`}>
      <svg 
        width="32" 
        height="32" 
        viewBox="0 0 100 100" 
        className="logo-icon"
      >
        {/* Simple DNA helix icon */}
        <defs>
          <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#0891b2" />
            <stop offset="100%" stopColor="#10b981" />
          </linearGradient>
        </defs>
        
        {/* DNA Strand 1 */}
        <path
          d="M30 80 Q40 60 50 40 Q60 20 70 20"
          stroke="url(#logoGradient)"
          strokeWidth="3"
          fill="none"
        />
        
        {/* DNA Strand 2 */}
        <path
          d="M30 20 Q40 40 50 60 Q60 80 70 80"
          stroke="url(#logoGradient)"
          strokeWidth="3"
          fill="none"
        />
        
        {/* Base pairs */}
        <line x1="35" y1="70" x2="45" y2="50" stroke="#0891b2" strokeWidth="2" opacity="0.8" />
        <line x1="40" y1="60" x2="50" y2="50" stroke="#0891b2" strokeWidth="2" opacity="0.8" />
        <line x1="45" y1="50" x2="55" y2="40" stroke="#0891b2" strokeWidth="2" opacity="0.8" />
        <line x1="50" y1="40" x2="60" y2="30" stroke="#0891b2" strokeWidth="2" opacity="0.8" />
      </svg>
      
      <span 
        className="text-xl font-semibold tracking-wide text-slate-800 dark:text-white"
        style={{ 
          fontFamily: 'Inter, system-ui, sans-serif'
        }}
      >
        Synthetic Ascendancy
      </span>
    </div>
  )
}