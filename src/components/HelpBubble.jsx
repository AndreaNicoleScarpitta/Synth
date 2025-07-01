import React, { useState, useRef, useEffect } from 'react';
import { HelpCircle, X } from 'lucide-react';

const HelpBubble = ({ 
  title, 
  content, 
  examples = [], 
  position = 'top',
  trigger = 'hover',
  size = 'md' 
}) => {
  const [isVisible, setIsVisible] = useState(false);
  const [actualPosition, setActualPosition] = useState(position);
  const bubbleRef = useRef(null);
  const triggerRef = useRef(null);

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

  // Size classes
  const sizeClasses = {
    sm: 'w-64',
    md: 'w-80',
    lg: 'w-96',
    xl: 'w-[28rem]'
  };

  // Position classes
  const positionClasses = {
    top: 'bottom-full left-1/2 transform -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 transform -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 transform -translate-y-1/2 mr-2',
    right: 'left-full top-1/2 transform -translate-y-1/2 ml-2'
  };

  // Arrow classes
  const arrowClasses = {
    top: 'top-full left-1/2 transform -translate-x-1/2 border-l-transparent border-r-transparent border-b-transparent border-t-white dark:border-t-neutral-800',
    bottom: 'bottom-full left-1/2 transform -translate-x-1/2 border-l-transparent border-r-transparent border-t-transparent border-b-white dark:border-b-neutral-800',
    left: 'left-full top-1/2 transform -translate-y-1/2 border-t-transparent border-b-transparent border-r-transparent border-l-white dark:border-l-neutral-800',
    right: 'right-full top-1/2 transform -translate-y-1/2 border-t-transparent border-b-transparent border-l-transparent border-r-white dark:border-r-neutral-800'
  };

  return (
    <div className="relative inline-block">
      {/* Trigger */}
      <button
        ref={triggerRef}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onClick={handleClick}
        className="inline-flex items-center justify-center w-5 h-5 text-neutral-400 hover:text-primary-500 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-opacity-50 rounded-full"
        type="button"
        aria-label="Show help information"
      >
        <HelpCircle className="w-4 h-4" />
      </button>

      {/* Help Bubble */}
      {isVisible && (
        <>
          {/* Backdrop for click trigger */}
          {trigger === 'click' && (
            <div
              className="fixed inset-0 z-40"
              onClick={handleClose}
            />
          )}
          
          <div
            ref={bubbleRef}
            className={`absolute z-50 ${sizeClasses[size]} ${positionClasses[actualPosition]}`}
          >
            {/* Arrow */}
            <div
              className={`absolute w-0 h-0 border-4 ${arrowClasses[actualPosition]}`}
            />
            
            {/* Content */}
            <div className="bg-white dark:bg-neutral-800 border border-neutral-200 dark:border-neutral-600 rounded-lg shadow-lg p-4">
              {/* Header */}
              <div className="flex items-start justify-between mb-2">
                <h4 className="text-sm font-semibold text-neutral-900 dark:text-white">
                  {title}
                </h4>
                {trigger === 'click' && (
                  <button
                    onClick={handleClose}
                    className="ml-2 text-neutral-400 hover:text-neutral-600 dark:hover:text-neutral-300 transition-colors"
                  >
                    <X className="w-4 h-4" />
                  </button>
                )}
              </div>

              {/* Content */}
              <div className="text-sm text-neutral-600 dark:text-neutral-300">
                {typeof content === 'string' ? (
                  <p>{content}</p>
                ) : (
                  content
                )}
              </div>

              {/* Examples */}
              {examples.length > 0 && (
                <div className="mt-3 pt-3 border-t border-neutral-200 dark:border-neutral-600">
                  <p className="text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-2">
                    Examples:
                  </p>
                  <ul className="text-xs text-neutral-600 dark:text-neutral-300 space-y-1">
                    {examples.map((example, index) => (
                      <li key={index} className="flex items-start">
                        <span className="text-neutral-400 mr-2">•</span>
                        <span>{example}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default HelpBubble;