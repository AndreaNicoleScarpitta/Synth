import React, { useState } from 'react';
import { X, Mail, Building, User, Phone, CheckCircle2, Loader } from 'lucide-react';
import HelpBubble from './HelpBubble';
import { getFieldHelp } from '../config/medicalFieldHelp';

// Design system constants
const designSystem = {
  colors: {
    primary: '#1e40af',
    primaryLight: '#3b82f6',
    secondary: '#6b7280',
    accent: '#10b981',
    neutral: {
      50: '#f9fafb',
      100: '#f3f4f6',
      200: '#e5e7eb',
      300: '#d1d5db',
      500: '#6b7280',
      600: '#4b5563',
      700: '#374151',
      800: '#1f2937',
      900: '#111827'
    }
  }
};

interface WaitlistModalProps {
  isOpen?: boolean;
  onClose: () => void;
}

interface FormData {
  name: string;
  email: string;
  organization: string;
  role: string;
  use_cases: string;
  interested_in_design_partner: boolean;
  phone: string;
  company_size: string;
  industry: string;
  current_ehr_system: string;
  timeline: string;
  budget_range: string;
  specific_requirements: string;
}

const WaitlistModal: React.FC<WaitlistModalProps> = ({ isOpen = false, onClose }) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  
  const [formData, setFormData] = useState<FormData>({
    name: '',
    email: '',
    organization: '',
    role: '',
    use_cases: '',
    interested_in_design_partner: false,
    phone: '',
    company_size: '',
    industry: '',
    current_ehr_system: '',
    timeline: '',
    budget_range: '',
    specific_requirements: ''
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      const response = await fetch('http://localhost:8003/api/v2/leads', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          source: 'waitlist_modal',
          timestamp: new Date().toISOString(),
        }),
      });

      if (response.ok) {
        setIsSuccess(true);
        setTimeout(() => {
          setIsSuccess(false);
          setFormData({
            name: '',
            email: '',
            organization: '',
            role: '',
            use_cases: '',
            interested_in_design_partner: false,
            phone: '',
            company_size: '',
            industry: '',
            current_ehr_system: '',
            timeline: '',
            budget_range: '',
            specific_requirements: ''
          });
          onClose();
        }, 3000);
      } else {
        console.error('Failed to submit waitlist form');
      }
    } catch (error) {
      console.error('Error submitting form:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleInputChange = (field: keyof FormData, value: string | boolean) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  if (!isOpen) return null;
  console.log('Modal rendering, isOpen:', isOpen);

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.7)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 99999,
        padding: '1rem'
      }}
      onClick={(e) => {
        if (e.target === e.currentTarget) {
          onClose();
        }
      }}
    >
      <div
        style={{
          backgroundColor: 'white',
          borderRadius: '12px',
          padding: '0',
          maxWidth: '600px',
          width: '100%',
          maxHeight: '90vh',
          overflowY: 'auto',
          position: 'relative',
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
          border: `1px solid ${designSystem.colors.neutral[200]}`
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {isSuccess ? (
          <div style={{ padding: '3rem 2rem', textAlign: 'center' }}>
            <CheckCircle2 size={64} style={{ color: designSystem.colors.accent, margin: '0 auto 1.5rem' }} />
            <h3 style={{ 
              fontSize: '1.5rem', 
              fontWeight: '600', 
              color: designSystem.colors.neutral[800],
              marginBottom: '0.75rem'
            }}>
              Welcome to the waitlist!
            </h3>
            <p style={{ 
              color: designSystem.colors.neutral[600],
              fontSize: '1rem'
            }}>
              We'll be in touch soon with early access details.
            </p>
          </div>
        ) : (
          <>
            {/* Header */}
            <div style={{ 
              padding: '1.5rem 2rem', 
              borderBottom: `1px solid ${designSystem.colors.neutral[200]}`,
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}>
              <div>
                <h2 style={{ 
                  fontSize: '1.5rem', 
                  fontWeight: '600', 
                  color: designSystem.colors.neutral[800],
                  marginBottom: '0.25rem'
                }}>
                  Join the Waitlist
                </h2>
                <p style={{ 
                  color: designSystem.colors.neutral[600],
                  fontSize: '0.875rem'
                }}>
                  Get early access to Synthetic Ascension's AI-powered EHR platform
                </p>
              </div>
              <button
                onClick={onClose}
                style={{
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  padding: '0.5rem',
                  borderRadius: '6px',
                  color: designSystem.colors.neutral[500],
                  transition: 'all 0.2s'
                }}
                onMouseOver={(e) => {
                  e.currentTarget.style.backgroundColor = designSystem.colors.neutral[100];
                  e.currentTarget.style.color = designSystem.colors.neutral[700];
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.backgroundColor = 'transparent';
                  e.currentTarget.style.color = designSystem.colors.neutral[500];
                }}
              >
                <X size={20} />
              </button>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} style={{ padding: '2rem' }}>
              {/* Basic Information Section */}
              <div style={{ marginBottom: '2rem' }}>
                <h3 style={{ 
                  fontSize: '1.125rem', 
                  fontWeight: '600', 
                  color: designSystem.colors.neutral[800],
                  marginBottom: '1rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem'
                }}>
                  <User size={18} style={{ color: designSystem.colors.primary }} />
                  Basic Information
                </h3>
                
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
                  <div>
                    <label style={{ 
                      display: 'block', 
                      fontSize: '0.875rem', 
                      fontWeight: '500', 
                      color: designSystem.colors.neutral[700],
                      marginBottom: '0.5rem'
                    }}>
                      Full Name *
                    </label>
                    <input
                      type="text"
                      required
                      value={formData.name}
                      onChange={(e) => handleInputChange('name', e.target.value)}
                      style={{
                        width: '100%',
                        padding: '0.75rem',
                        border: `1px solid ${designSystem.colors.neutral[300]}`,
                        borderRadius: '6px',
                        fontSize: '0.875rem',
                        transition: 'all 0.2s'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = designSystem.colors.primary;
                        e.target.style.boxShadow = `0 0 0 3px rgba(30, 64, 175, 0.1)`;
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = designSystem.colors.neutral[300];
                        e.target.style.boxShadow = 'none';
                      }}
                    />
                  </div>
                  
                  <div>
                    <label style={{ 
                      display: 'block', 
                      fontSize: '0.875rem', 
                      fontWeight: '500', 
                      color: designSystem.colors.neutral[700],
                      marginBottom: '0.5rem'
                    }}>
                      Email Address *
                    </label>
                    <input
                      type="email"
                      required
                      value={formData.email}
                      onChange={(e) => handleInputChange('email', e.target.value)}
                      style={{
                        width: '100%',
                        padding: '0.75rem',
                        border: `1px solid ${designSystem.colors.neutral[300]}`,
                        borderRadius: '6px',
                        fontSize: '0.875rem',
                        transition: 'all 0.2s'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = designSystem.colors.primary;
                        e.target.style.boxShadow = `0 0 0 3px rgba(30, 64, 175, 0.1)`;
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = designSystem.colors.neutral[300];
                        e.target.style.boxShadow = 'none';
                      }}
                    />
                  </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                  <div>
                    <label style={{ 
                      display: 'block', 
                      fontSize: '0.875rem', 
                      fontWeight: '500', 
                      color: designSystem.colors.neutral[700],
                      marginBottom: '0.5rem'
                    }}>
                      Organization
                    </label>
                    <input
                      type="text"
                      value={formData.organization}
                      onChange={(e) => handleInputChange('organization', e.target.value)}
                      style={{
                        width: '100%',
                        padding: '0.75rem',
                        border: `1px solid ${designSystem.colors.neutral[300]}`,
                        borderRadius: '6px',
                        fontSize: '0.875rem',
                        transition: 'all 0.2s'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = designSystem.colors.primary;
                        e.target.style.boxShadow = `0 0 0 3px rgba(30, 64, 175, 0.1)`;
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = designSystem.colors.neutral[300];
                        e.target.style.boxShadow = 'none';
                      }}
                    />
                  </div>
                  
                  <div>
                    <label style={{ 
                      display: 'block', 
                      fontSize: '0.875rem', 
                      fontWeight: '500', 
                      color: designSystem.colors.neutral[700],
                      marginBottom: '0.5rem'
                    }}>
                      Professional Role
                    </label>
                    <input
                      type="text"
                      value={formData.role}
                      onChange={(e) => handleInputChange('role', e.target.value)}
                      placeholder="e.g., Clinical Researcher, Data Scientist"
                      style={{
                        width: '100%',
                        padding: '0.75rem',
                        border: `1px solid ${designSystem.colors.neutral[300]}`,
                        borderRadius: '6px',
                        fontSize: '0.875rem',
                        transition: 'all 0.2s'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = designSystem.colors.primary;
                        e.target.style.boxShadow = `0 0 0 3px rgba(30, 64, 175, 0.1)`;
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = designSystem.colors.neutral[300];
                        e.target.style.boxShadow = 'none';
                      }}
                    />
                  </div>
                </div>
              </div>

              {/* Project Details Section */}
              <div style={{ marginBottom: '2rem' }}>
                <h3 style={{ 
                  fontSize: '1.125rem', 
                  fontWeight: '600', 
                  color: designSystem.colors.neutral[800],
                  marginBottom: '1rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem'
                }}>
                  <Building size={18} style={{ color: designSystem.colors.primary }} />
                  Project Details
                </h3>
                
                <div style={{ marginBottom: '1rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                    <label style={{ 
                      fontSize: '0.875rem', 
                      fontWeight: '500', 
                      color: designSystem.colors.neutral[700]
                    }}>
                      Primary Use Cases
                    </label>
                    <HelpBubble content={getFieldHelp('use_cases')} />
                  </div>
                  <textarea
                    value={formData.use_cases}
                    onChange={(e) => handleInputChange('use_cases', e.target.value)}
                    placeholder="Describe your intended use cases for synthetic EHR data..."
                    rows={3}
                    style={{
                      width: '100%',
                      padding: '0.75rem',
                      border: `1px solid ${designSystem.colors.neutral[300]}`,
                      borderRadius: '6px',
                      fontSize: '0.875rem',
                      resize: 'vertical',
                      transition: 'all 0.2s'
                    }}
                    onFocus={(e) => {
                      e.target.style.borderColor = designSystem.colors.primary;
                      e.target.style.boxShadow = `0 0 0 3px rgba(30, 64, 175, 0.1)`;
                    }}
                    onBlur={(e) => {
                      e.target.style.borderColor = designSystem.colors.neutral[300];
                      e.target.style.boxShadow = 'none';
                    }}
                  />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                      <label style={{ 
                        fontSize: '0.875rem', 
                        fontWeight: '500', 
                        color: designSystem.colors.neutral[700]
                      }}>
                        Current EHR System
                      </label>
                      <HelpBubble content={getFieldHelp('current_ehr_system')} />
                    </div>
                    <input
                      type="text"
                      value={formData.current_ehr_system}
                      onChange={(e) => handleInputChange('current_ehr_system', e.target.value)}
                      placeholder="e.g., Epic, Cerner, Custom"
                      style={{
                        width: '100%',
                        padding: '0.75rem',
                        border: `1px solid ${designSystem.colors.neutral[300]}`,
                        borderRadius: '6px',
                        fontSize: '0.875rem',
                        transition: 'all 0.2s'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = designSystem.colors.primary;
                        e.target.style.boxShadow = `0 0 0 3px rgba(30, 64, 175, 0.1)`;
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = designSystem.colors.neutral[300];
                        e.target.style.boxShadow = 'none';
                      }}
                    />
                  </div>
                  
                  <div>
                    <label style={{ 
                      display: 'block', 
                      fontSize: '0.875rem', 
                      fontWeight: '500', 
                      color: designSystem.colors.neutral[700],
                      marginBottom: '0.5rem'
                    }}>
                      Implementation Timeline
                    </label>
                    <select
                      value={formData.timeline}
                      onChange={(e) => handleInputChange('timeline', e.target.value)}
                      style={{
                        width: '100%',
                        padding: '0.75rem',
                        border: `1px solid ${designSystem.colors.neutral[300]}`,
                        borderRadius: '6px',
                        fontSize: '0.875rem',
                        backgroundColor: 'white',
                        transition: 'all 0.2s'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = designSystem.colors.primary;
                        e.target.style.boxShadow = `0 0 0 3px rgba(30, 64, 175, 0.1)`;
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = designSystem.colors.neutral[300];
                        e.target.style.boxShadow = 'none';
                      }}
                    >
                      <option value="">Select timeline</option>
                      <option value="immediate">Immediate (1-3 months)</option>
                      <option value="short_term">Short-term (3-6 months)</option>
                      <option value="medium_term">Medium-term (6-12 months)</option>
                      <option value="long_term">Long-term (12+ months)</option>
                      <option value="exploring">Just exploring options</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Design Partner Interest */}
              <div style={{ marginBottom: '2rem', padding: '1rem', backgroundColor: designSystem.colors.neutral[50], borderRadius: '8px', border: `1px solid ${designSystem.colors.neutral[200]}` }}>
                <label style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '0.75rem',
                  cursor: 'pointer'
                }}>
                  <input
                    type="checkbox"
                    checked={formData.interested_in_design_partner}
                    onChange={(e) => handleInputChange('interested_in_design_partner', e.target.checked)}
                    style={{
                      width: '1.125rem',
                      height: '1.125rem',
                      accentColor: designSystem.colors.primary
                    }}
                  />
                  <div>
                    <span style={{ 
                      fontSize: '0.875rem', 
                      fontWeight: '500', 
                      color: designSystem.colors.neutral[800]
                    }}>
                      I'm interested in being a design partner
                    </span>
                    <p style={{ 
                      fontSize: '0.75rem', 
                      color: designSystem.colors.neutral[600],
                      margin: '0.25rem 0 0 0'
                    }}>
                      Work closely with our team to shape product direction and get priority access
                    </p>
                  </div>
                </label>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={isSubmitting}
                style={{
                  width: '100%',
                  padding: '0.875rem 1.5rem',
                  backgroundColor: isSubmitting ? designSystem.colors.neutral[400] : designSystem.colors.primary,
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  fontSize: '0.875rem',
                  fontWeight: '500',
                  cursor: isSubmitting ? 'not-allowed' : 'pointer',
                  transition: 'all 0.2s',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '0.5rem'
                }}
                onMouseOver={(e) => {
                  if (!isSubmitting) {
                    e.currentTarget.style.backgroundColor = designSystem.colors.primaryLight;
                  }
                }}
                onMouseOut={(e) => {
                  if (!isSubmitting) {
                    e.currentTarget.style.backgroundColor = designSystem.colors.primary;
                  }
                }}
              >
                {isSubmitting ? (
                  <>
                    <Loader size={16} style={{ animation: 'spin 1s linear infinite' }} />
                    Joining Waitlist...
                  </>
                ) : (
                  <>
                    <Mail size={16} />
                    Join Waitlist
                  </>
                )}
              </button>
            </form>
          </>
        )}
      </div>
    </div>
  );
};

export default WaitlistModal;