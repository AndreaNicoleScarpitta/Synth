import React from 'react'

export const SyntheticLogo = ({ className = "" }: { className?: string }) => {
  return (
    <div className={`flex flex-col items-center ${className}`}>
      <svg 
        width="280" 
        height="120" 
        viewBox="0 0 280 120" 
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
        
        {/* DNA Strand 1 - positioned to match original PNG */}
        <path
          d="M80 80 Q110 60 140 40 Q170 20 200 15"
          stroke="url(#dnaGradient)"
          strokeWidth="4"
          fill="none"
          className="animate-pulse"
        />
        
        {/* DNA Strand 2 */}
        <path
          d="M80 15 Q110 35 140 55 Q170 75 200 80"
          stroke="url(#dnaGradient)"
          strokeWidth="4"
          fill="none"
          className="animate-pulse"
          style={{ animationDelay: '0.5s' }}
        />
        
        {/* Base pairs - scaled and positioned to match original */}
        <line x1="90" y1="70" x2="110" y2="50" stroke="#fbbf24" strokeWidth="3" opacity="0.8" />
        <line x1="110" y1="60" x2="130" y2="45" stroke="#fbbf24" strokeWidth="3" opacity="0.8" />
        <line x1="130" y1="50" x2="150" y2="35" stroke="#fbbf24" strokeWidth="3" opacity="0.8" />
        <line x1="150" y1="40" x2="170" y2="25" stroke="#fbbf24" strokeWidth="3" opacity="0.8" />
        <line x1="170" y1="30" x2="190" y2="20" stroke="#fbbf24" strokeWidth="3" opacity="0.8" />
        
        {/* Upward Arrow - positioned to match original PNG */}
        <path
          d="M205 80 L225 15 M210 25 L225 15 L240 25"
          stroke="#fbbf24"
          strokeWidth="5"
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="animate-bounce"
        />
        
        {/* Matrix code particles */}
        <circle cx="65" cy="25" r="1.5" fill="#fbbf24" opacity="0.6" className="animate-ping" />
        <circle cx="255" cy="35" r="1.5" fill="#fbbf24" opacity="0.4" className="animate-ping" style={{ animationDelay: '1s' }} />
        <circle cx="75" cy="85" r="1.5" fill="#fbbf24" opacity="0.8" className="animate-ping" style={{ animationDelay: '2s' }} />
        
        {/* Text positioned below DNA helix as in original PNG */}
        <text
          x="140"
          y="110"
          textAnchor="middle"
          fontSize="24"
          fontWeight="400"
          fill="#fbbf24"
          fontFamily="Hi Melody, Inter, system-ui, sans-serif"
          style={{ 
            filter: 'drop-shadow(0 0 8px rgba(251, 191, 36, 0.4))',
            letterSpacing: '2px'
          }}
        >
          synthetic ascendancy
        </text>
      </svg>
    </div>
  )
}