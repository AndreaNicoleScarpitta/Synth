import React, { useState, useRef, useEffect } from 'react';
import { HelpCircle, X } from 'lucide-react';

interface HelpBubbleProps {
  title?: string;
  content: string | { description: string; examples?: string[] };
  examples?: string[];
  position?: 'top' | 'bottom' | 'left' | 'right';
  trigger?: 'hover' | 'click';
  size?: 'sm' | 'md' | 'lg';
}

const HelpBubble: React.FC<HelpBubbleProps> = ({ 
  title, 
  content, 
  examples = [], 
  position = 'top',
  trigger = 'hover',
  size = 'md' 
}) => {
  const [isVisible, setIsVisible] = useState(false);
  const [actualPosition, setActualPosition] = useState(position);
  const bubbleRef = useRef<HTMLDivElement>(null);
  const triggerRef = useRef<HTMLDivElement>(null);

  // Auto-position bubble to stay within viewport
  useEffect(() => {
    if (isVisible && bubbleRef.current && triggerRef.current) {
      const bubble = bubbleRef.current;
      const trigger = triggerRef.current;
      const rect = trigger.getBoundingClientRect();
      const bubbleRect = bubble.getBoundingClientRect();
      
      // Check if bubble would go off-screen and adjust position
      let newPosition = position;
      
      if (position === 'top' && rect.top - bubbleRect.height < 20) {
        newPosition = 'bottom';
      } else if (position === 'bottom' && rect.bottom + bubbleRect.height > window.innerHeight - 20) {
        newPosition = 'top';
      } else if (position === 'left' && rect.left - bubbleRect.width < 20) {
        newPosition = 'right';
      } else if (position === 'right' && rect.right + bubbleRect.width > window.innerWidth - 20) {
        newPosition = 'left';
      }
      
      setActualPosition(newPosition);
    }
  }, [isVisible, position]);

  const handleMouseEnter = () => {
    if (trigger === 'hover') {
      setIsVisible(true);
    }
  };

  const handleMouseLeave = () => {
    if (trigger === 'hover') {
      setIsVisible(false);
    }
  };

  const handleClick = () => {
    if (trigger === 'click') {
      setIsVisible(!isVisible);
    }
  };

  const handleClose = () => {
    setIsVisible(false);
  };

  // Extract content details - handle null/undefined content
  const contentObj = typeof content === 'string' 
    ? { description: content, examples } 
    : (content || { description: '', examples: [] });
  const displayExamples = (contentObj?.examples || examples || []);

  // Size configurations
  const sizeConfig = {
    sm: {
      iconSize: 14,
      bubbleWidth: '200px',
      fontSize: '12px',
      padding: '8px 12px'
    },
    md: {
      iconSize: 16,
      bubbleWidth: '280px',
      fontSize: '13px',
      padding: '12px 16px'
    },
    lg: {
      iconSize: 18,
      bubbleWidth: '320px',
      fontSize: '14px',
      padding: '16px 20px'
    }
  };

  const config = sizeConfig[size];

  // Position styles
  const getPositionStyles = () => {
    const baseStyles: React.CSSProperties = {
      position: 'absolute',
      zIndex: 1000,
      width: config.bubbleWidth,
      background: 'rgba(17, 24, 39, 0.98)',
      color: 'white',
      borderRadius: '12px',
      padding: config.padding,
      fontSize: config.fontSize,
      lineHeight: '1.4',
      boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.1)',
      backdropFilter: 'blur(8px)',
      animation: 'fadeInScale 0.2s cubic-bezier(0.2, 0, 0.2, 1)',
      transformOrigin: 'center',
      pointerEvents: 'auto'
    };

    switch (actualPosition) {
      case 'top':
        return {
          ...baseStyles,
          bottom: '100%',
          left: '50%',
          transform: 'translateX(-50%)',
          marginBottom: '8px'
        };
      case 'bottom':
        return {
          ...baseStyles,
          top: '100%',
          left: '50%',
          transform: 'translateX(-50%)',
          marginTop: '8px'
        };
      case 'left':
        return {
          ...baseStyles,
          right: '100%',
          top: '50%',
          transform: 'translateY(-50%)',
          marginRight: '8px'
        };
      case 'right':
        return {
          ...baseStyles,
          left: '100%',
          top: '50%',
          transform: 'translateY(-50%)',
          marginLeft: '8px'
        };
      default:
        return baseStyles;
    }
  };

  const getArrowStyles = (): React.CSSProperties => {
    const arrowSize = 6;
    const baseArrowStyles: React.CSSProperties = {
      position: 'absolute',
      width: 0,
      height: 0,
      pointerEvents: 'none'
    };

    switch (actualPosition) {
      case 'top':
        return {
          ...baseArrowStyles,
          top: '100%',
          left: '50%',
          transform: 'translateX(-50%)',
          borderLeft: `${arrowSize}px solid transparent`,
          borderRight: `${arrowSize}px solid transparent`,
          borderTop: `${arrowSize}px solid rgba(17, 24, 39, 0.98)`
        };
      case 'bottom':
        return {
          ...baseArrowStyles,
          bottom: '100%',
          left: '50%',
          transform: 'translateX(-50%)',
          borderLeft: `${arrowSize}px solid transparent`,
          borderRight: `${arrowSize}px solid transparent`,
          borderBottom: `${arrowSize}px solid rgba(17, 24, 39, 0.98)`
        };
      case 'left':
        return {
          ...baseArrowStyles,
          left: '100%',
          top: '50%',
          transform: 'translateY(-50%)',
          borderTop: `${arrowSize}px solid transparent`,
          borderBottom: `${arrowSize}px solid transparent`,
          borderLeft: `${arrowSize}px solid rgba(17, 24, 39, 0.98)`
        };
      case 'right':
        return {
          ...baseArrowStyles,
          right: '100%',
          top: '50%',
          transform: 'translateY(-50%)',
          borderTop: `${arrowSize}px solid transparent`,
          borderBottom: `${arrowSize}px solid transparent`,
          borderRight: `${arrowSize}px solid rgba(17, 24, 39, 0.98)`
        };
      default:
        return baseArrowStyles;
    }
  };

  return (
    <>
      <style>{`
        @keyframes fadeInScale {
          from {
            opacity: 0;
            transform: scale(0.95) translateX(-50%);
          }
          to {
            opacity: 1;
            transform: scale(1) translateX(-50%);
          }
        }
      `}</style>
      <div 
        ref={triggerRef}
        style={{ 
          position: 'relative', 
          display: 'inline-block',
          cursor: trigger === 'click' ? 'pointer' : 'help'
        }}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onClick={handleClick}
      >
        <HelpCircle 
          size={config.iconSize} 
          style={{ 
            color: '#9ca3af',
            transition: 'color 0.2s ease',
            ':hover': {
              color: '#3b82f6'
            }
          }} 
        />
        
        {isVisible && (
          <div ref={bubbleRef} style={getPositionStyles()}>
            <div style={getArrowStyles()} />
            
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: title || trigger === 'click' ? '8px' : '0' }}>
              {title && (
                <h4 style={{ 
                  margin: 0,
                  fontSize: config.fontSize,
                  fontWeight: '600',
                  color: '#f3f4f6'
                }}>
                  {title}
                </h4>
              )}
              {trigger === 'click' && (
                <button
                  onClick={handleClose}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: '#9ca3af',
                    cursor: 'pointer',
                    padding: '0',
                    marginLeft: '8px'
                  }}
                >
                  <X size={14} />
                </button>
              )}
            </div>
            
            <p style={{ 
              margin: 0,
              color: '#d1d5db',
              marginBottom: displayExamples.length > 0 ? '8px' : '0'
            }}>
              {contentObj?.description || ''}
            </p>
            
            {displayExamples.length > 0 && (
              <div style={{ borderTop: '1px solid rgba(255, 255, 255, 0.1)', paddingTop: '8px' }}>
                <div style={{ 
                  fontSize: '11px',
                  fontWeight: '500',
                  color: '#9ca3af',
                  marginBottom: '4px'
                }}>
                  Examples:
                </div>
                <ul style={{ 
                  margin: 0,
                  paddingLeft: '12px',
                  fontSize: '11px',
                  color: '#d1d5db'
                }}>
                  {displayExamples.map((example, index) => (
                    <li key={index} style={{ marginBottom: '2px' }}>
                      {example}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </>
  );
};

export default HelpBubble;