import React from 'react'

export const SyntheticLogo = ({ className = "" }: { className?: string }) => {
  return (
    <div className={`flex items-center gap-3 ${className}`}>
      <svg 
        width="40" 
        height="40" 
        viewBox="0 0 100 100" 
        className="dna-logo"
        style={{ filter: 'drop-shadow(0 0 10px rgba(251, 191, 36, 0.5))' }}
      >
        {/* DNA Helix with upward arrow */}
        <defs>
          <linearGradient id="dnaGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#fbbf24" />
            <stop offset="100%" stopColor="#f59e0b" />
          </linearGradient>
        </defs>
        
        {/* DNA Strand 1 */}
        <path
          d="M20 80 Q30 60 40 40 Q50 20 60 20"
          stroke="url(#dnaGradient)"
          strokeWidth="3"
          fill="none"
          className="animate-pulse"
        />
        
        {/* DNA Strand 2 */}
        <path
          d="M20 20 Q30 40 40 60 Q50 80 60 80"
          stroke="url(#dnaGradient)"
          strokeWidth="3"
          fill="none"
          className="animate-pulse"
          style={{ animationDelay: '0.5s' }}
        />
        
        {/* Base pairs */}
        <line x1="25" y1="70" x2="35" y2="50" stroke="#fbbf24" strokeWidth="2" opacity="0.8" />
        <line x1="30" y1="60" x2="40" y2="50" stroke="#fbbf24" strokeWidth="2" opacity="0.8" />
        <line x1="35" y1="50" x2="45" y2="40" stroke="#fbbf24" strokeWidth="2" opacity="0.8" />
        <line x1="40" y1="40" x2="50" y2="30" stroke="#fbbf24" strokeWidth="2" opacity="0.8" />
        <line x1="45" y1="30" x2="55" y2="30" stroke="#fbbf24" strokeWidth="2" opacity="0.8" />
        
        {/* Upward Arrow */}
        <path
          d="M65 75 L75 15 M65 25 L75 15 L85 25"
          stroke="#fbbf24"
          strokeWidth="4"
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="animate-bounce"
        />
        
        {/* Matrix code particles */}
        <circle cx="15" cy="25" r="1" fill="#fbbf24" opacity="0.6" className="animate-ping" />
        <circle cx="85" cy="35" r="1" fill="#fbbf24" opacity="0.4" className="animate-ping" style={{ animationDelay: '1s' }} />
        <circle cx="25" cy="85" r="1" fill="#fbbf24" opacity="0.8" className="animate-ping" style={{ animationDelay: '2s' }} />
      </svg>
      
      <span 
        className="text-2xl font-bold tracking-wider"
        style={{ 
          fontFamily: 'Hi, Inter, system-ui, sans-serif',
          color: '#fbbf24',
          textShadow: '0 0 10px rgba(251, 191, 36, 0.3)'
        }}
      >
        synthetic ascendancy
      </span>
    </div>
  )
}