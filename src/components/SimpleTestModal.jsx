import React from 'react';

const SimpleTestModal = ({ isOpen, onClose }) => {
  console.log('SimpleTestModal rendering, isOpen:', isOpen);
  
  if (!isOpen) return null;

  return (
    <div 
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 999999
      }}
      onClick={onClose}
    >
      <div 
        style={{
          backgroundColor: 'white',
          padding: '40px',
          borderRadius: '10px',
          maxWidth: '500px',
          width: '90%'
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <h2 style={{ color: 'black', marginBottom: '20px' }}>TEST MODAL</h2>
        <p style={{ color: 'black', marginBottom: '20px' }}>
          This is a simple test modal to verify rendering works.
        </p>
        <button 
          onClick={onClose}
          style={{
            backgroundColor: '#3b82f6',
            color: 'white',
            padding: '10px 20px',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          Close
        </button>
      </div>
    </div>
  );
};

export default SimpleTestModal;