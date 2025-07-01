import React, { useState, useEffect } from 'react';

interface DynamicToastProps {
  message: string;
  type?: 'info' | 'success' | 'warning' | 'error';
  duration?: number;
  onClose?: () => void;
}

const DynamicToast: React.FC<DynamicToastProps> = ({ 
  message, 
  type = 'info', 
  duration = 4000, 
  onClose 
}) => {
  const [isVisible, setIsVisible] = useState(false);
  const [isLeaving, setIsLeaving] = useState(false);

  useEffect(() => {
    // Show toast
    setIsVisible(true);
    
    // Auto-hide after duration
    const timer = setTimeout(() => {
      handleClose();
    }, duration);

    return () => clearTimeout(timer);
  }, [duration]);

  const handleClose = () => {
    setIsLeaving(true);
    setTimeout(() => {
      setIsVisible(false);
      onClose?.();
    }, 300); // Match animation duration
  };

  if (!isVisible) return null;

  const getToastStyles = (): React.CSSProperties => {
    const baseStyles: React.CSSProperties = {
      position: 'fixed',
      bottom: '24px',
      left: '50%',
      transform: 'translateX(-50%)',
      zIndex: 9999,
      padding: '16px 24px',
      borderRadius: '12px',
      boxShadow: '0 8px 32px rgba(0, 0, 0, 0.12)',
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
      maxWidth: '480px',
      minWidth: '320px',
      fontSize: '14px',
      fontWeight: '500',
      backdropFilter: 'blur(8px)',
      border: '1px solid rgba(255, 255, 255, 0.1)',
      transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
      animation: isLeaving 
        ? 'slideOut 0.3s cubic-bezier(0.4, 0, 0.2, 1) forwards' 
        : 'slideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1) forwards'
    };

    switch (type) {
      case 'success':
        return {
          ...baseStyles,
          backgroundColor: 'rgba(16, 185, 129, 0.95)',
          color: 'white',
        };
      case 'warning':
        return {
          ...baseStyles,
          backgroundColor: 'rgba(245, 158, 11, 0.95)',
          color: 'white',
        };
      case 'error':
        return {
          ...baseStyles,
          backgroundColor: 'rgba(239, 68, 68, 0.95)',
          color: 'white',
        };
      default: // info
        return {
          ...baseStyles,
          backgroundColor: 'rgba(59, 130, 246, 0.95)',
          color: 'white',
        };
    }
  };

  const getIcon = () => {
    switch (type) {
      case 'success':
        return '✓';
      case 'warning':
        return '⚠';
      case 'error':
        return '✕';
      default:
        return 'ℹ';
    }
  };

  return (
    <>
      <style>{`
        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateX(-50%) translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
          }
        }
        
        @keyframes slideOut {
          from {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
          }
          to {
            opacity: 0;
            transform: translateX(-50%) translateY(-20px);
          }
        }
      `}</style>
      <div style={getToastStyles()}>
        <span style={{ fontSize: '16px' }}>{getIcon()}</span>
        <span>{message}</span>
        <button
          onClick={handleClose}
          style={{
            background: 'none',
            border: 'none',
            color: 'inherit',
            cursor: 'pointer',
            fontSize: '18px',
            marginLeft: 'auto',
            opacity: 0.7,
            transition: 'opacity 0.2s'
          }}
          onMouseOver={(e) => e.currentTarget.style.opacity = '1'}
          onMouseOut={(e) => e.currentTarget.style.opacity = '0.7'}
        >
          ×
        </button>
      </div>
    </>
  );
};

// Toast state management hook
export const useToast = () => {
  const [toasts, setToasts] = useState<Array<{
    id: number;
    message: string;
    type: 'info' | 'success' | 'warning' | 'error';
    duration?: number;
  }>>([]);

  const addToast = (message: string, type: 'info' | 'success' | 'warning' | 'error' = 'info', duration?: number) => {
    const id = Date.now();
    setToasts(prev => [...prev, { id, message, type, duration }]);
  };

  const removeToast = (id: number) => {
    setToasts(prev => prev.filter(toast => toast.id !== id));
  };

  const ToastContainer = () => (
    <>
      {toasts.map(toast => (
        <DynamicToast
          key={toast.id}
          message={toast.message}
          type={toast.type}
          duration={toast.duration}
          onClose={() => removeToast(toast.id)}
        />
      ))}
    </>
  );

  return { addToast, ToastContainer };
};

export default DynamicToast;