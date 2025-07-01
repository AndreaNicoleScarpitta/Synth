

interface DNALogoProps {
  className?: string
  size?: 'sm' | 'md' | 'lg' | 'xl'
}

export function DNALogo({ className = '', size = 'md' }: DNALogoProps) {
  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-12 h-12',
    lg: 'w-16 h-16',
    xl: 'w-24 h-24'
  }

  return (
    <div className={`${sizeClasses[size]} ${className} relative animate-dna-helix`}>
      <svg
        viewBox="0 0 100 100"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="w-full h-full"
      >
        {/* DNA Helix Structure */}
        <defs>
          <linearGradient id="goldGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#fbbf24" />
            <stop offset="50%" stopColor="#f59e0b" />
            <stop offset="100%" stopColor="#d97706" />
          </linearGradient>
          <linearGradient id="matrixGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#10b981" />
            <stop offset="50%" stopColor="#059669" />
            <stop offset="100%" stopColor="#047857" />
          </linearGradient>
        </defs>
        
        {/* Left helix strand */}
        <path
          d="M20 10 Q30 25 20 40 Q10 55 20 70 Q30 85 20 90"
          stroke="url(#goldGradient)"
          strokeWidth="3"
          fill="none"
          className="animate-pulse"
        />
        
        {/* Right helix strand */}
        <path
          d="M80 10 Q70 25 80 40 Q90 55 80 70 Q70 85 80 90"
          stroke="url(#goldGradient)"
          strokeWidth="3"
          fill="none"
          className="animate-pulse"
        />
        
        {/* Base pairs connecting the strands */}
        <g className="animate-float">
          <line x1="20" y1="20" x2="80" y2="20" stroke="url(#matrixGradient)" strokeWidth="2" opacity="0.8" />
          <line x1="25" y1="30" x2="75" y2="30" stroke="url(#matrixGradient)" strokeWidth="2" opacity="0.6" />
          <line x1="20" y1="40" x2="80" y2="40" stroke="url(#matrixGradient)" strokeWidth="2" opacity="0.8" />
          <line x1="15" y1="50" x2="85" y2="50" stroke="url(#matrixGradient)" strokeWidth="2" opacity="0.4" />
          <line x1="20" y1="60" x2="80" y2="60" stroke="url(#matrixGradient)" strokeWidth="2" opacity="0.8" />
          <line x1="25" y1="70" x2="75" y2="70" stroke="url(#matrixGradient)" strokeWidth="2" opacity="0.6" />
          <line x1="20" y1="80" x2="80" y2="80" stroke="url(#matrixGradient)" strokeWidth="2" opacity="0.8" />
        </g>
        
        {/* Matrix-style code particles */}
        <g className="opacity-60">
          <text x="85" y="25" fill="url(#matrixGradient)" fontSize="6" className="animate-pulse">01</text>
          <text x="5" y="35" fill="url(#matrixGradient)" fontSize="6" className="animate-pulse">10</text>
          <text x="90" y="45" fill="url(#matrixGradient)" fontSize="6" className="animate-pulse">11</text>
          <text x="2" y="65" fill="url(#matrixGradient)" fontSize="6" className="animate-pulse">00</text>
          <text x="88" y="75" fill="url(#matrixGradient)" fontSize="6" className="animate-pulse">01</text>
        </g>
      </svg>
    </div>
  )
}