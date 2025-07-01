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

const WaitlistModal = ({ isOpen = false, onClose }) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  
  const [formData, setFormData] = useState({
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

  const handleSubmit = async (e) => {
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

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  if (!isOpen) return null;

  if (isSuccess) {
    return (
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '16px',
        zIndex: 999999
      }}>
        <div style={{
          backgroundColor: 'white',
          borderRadius: '16px',
          padding: '48px',
          textAlign: 'center',
          maxWidth: '400px',
          width: '100%',
          boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1)'
        }}>
          <CheckCircle2 size={64} style={{ color: designSystem.colors.accent, margin: '0 auto 24px' }} />
          <h3 style={{
            fontSize: '24px',
            fontWeight: '600',
            color: designSystem.colors.neutral[900],
            marginBottom: '16px'
          }}>
            Welcome to the Waitlist!
          </h3>
          <p style={{
            color: designSystem.colors.neutral[600],
            fontSize: '16px',
            lineHeight: '1.5'
          }}>
            Thank you for your interest. We'll notify you as soon as early access becomes available.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '16px',
      zIndex: 999999
    }} onClick={onClose}>
      <div style={{
        backgroundColor: 'white',
        borderRadius: '16px',
        maxWidth: '600px',
        width: '100%',
        maxHeight: '90vh',
        overflowY: 'auto',
        boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
        position: 'relative'
      }} onClick={(e) => e.stopPropagation()}>
        
        {/* Header */}
        <div style={{
          padding: '24px 24px 0',
          borderBottom: `1px solid ${designSystem.colors.neutral[200]}`
        }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            marginBottom: '16px'
          }}>
            <h2 style={{
              fontSize: '24px',
              fontWeight: '700',
              color: designSystem.colors.neutral[900],
              margin: 0
            }}>
              Join the Waitlist
            </h2>
            <button
              onClick={onClose}
              style={{
                background: 'none',
                border: 'none',
                padding: '8px',
                borderRadius: '8px',
                cursor: 'pointer',
                color: designSystem.colors.neutral[500],
                transition: 'all 0.2s',
                ':hover': {
                  backgroundColor: designSystem.colors.neutral[100]
                }
              }}
            >
              <X size={20} />
            </button>
          </div>
          <p style={{
            color: designSystem.colors.neutral[600],
            fontSize: '16px',
            margin: '0 0 24px',
            lineHeight: '1.5'
          }}>
            Get early access to Synthetic Ascension's advanced EHR platform. We'll notify you when it's ready.
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} style={{ padding: '24px' }}>
          <div style={{ display: 'grid', gap: '20px' }}>
            
            {/* Basic Information Section */}
            <div>
              <h3 style={{
                fontSize: '18px',
                fontWeight: '600',
                color: designSystem.colors.neutral[900],
                marginBottom: '16px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}>
                <User size={20} style={{ color: designSystem.colors.primary }} />
                Basic Information
              </h3>
              
              <div style={{ display: 'grid', gap: '16px' }}>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                  <div>
                    <label style={{
                      display: 'block',
                      fontSize: '14px',
                      fontWeight: '500',
                      color: designSystem.colors.neutral[700],
                      marginBottom: '6px'
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
                        padding: '12px',
                        border: `1px solid ${designSystem.colors.neutral[300]}`,
                        borderRadius: '8px',
                        fontSize: '16px',
                        outline: 'none',
                        transition: 'border-color 0.2s',
                        ':focus': {
                          borderColor: designSystem.colors.primary
                        }
                      }}
                      placeholder="Your full name"
                    />
                  </div>
                  
                  <div>
                    <label style={{
                      display: 'block',
                      fontSize: '14px',
                      fontWeight: '500',
                      color: designSystem.colors.neutral[700],
                      marginBottom: '6px'
                    }}>
                      Work Email *
                    </label>
                    <input
                      type="email"
                      required
                      value={formData.email}
                      onChange={(e) => handleInputChange('email', e.target.value)}
                      style={{
                        width: '100%',
                        padding: '12px',
                        border: `1px solid ${designSystem.colors.neutral[300]}`,
                        borderRadius: '8px',
                        fontSize: '16px',
                        outline: 'none',
                        transition: 'border-color 0.2s'
                      }}
                      placeholder="work@company.com"
                    />
                  </div>
                </div>
                
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                  <div>
                    <label style={{
                      display: 'block',
                      fontSize: '14px',
                      fontWeight: '500',
                      color: designSystem.colors.neutral[700],
                      marginBottom: '6px'
                    }}>
                      Organization *
                    </label>
                    <input
                      type="text"
                      required
                      value={formData.organization}
                      onChange={(e) => handleInputChange('organization', e.target.value)}
                      style={{
                        width: '100%',
                        padding: '12px',
                        border: `1px solid ${designSystem.colors.neutral[300]}`,
                        borderRadius: '8px',
                        fontSize: '16px',
                        outline: 'none'
                      }}
                      placeholder="Company or institution"
                    />
                  </div>
                  
                  <div>
                    <label style={{
                      display: 'block',
                      fontSize: '14px',
                      fontWeight: '500',
                      color: designSystem.colors.neutral[700],
                      marginBottom: '6px'
                    }}>
                      Role
                    </label>
                    <input
                      type="text"
                      value={formData.role}
                      onChange={(e) => handleInputChange('role', e.target.value)}
                      style={{
                        width: '100%',
                        padding: '12px',
                        border: `1px solid ${designSystem.colors.neutral[300]}`,
                        borderRadius: '8px',
                        fontSize: '16px',
                        outline: 'none'
                      }}
                      placeholder="Your role or title"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Project Details Section */}
            <div>
              <h3 style={{
                fontSize: '18px',
                fontWeight: '600',
                color: designSystem.colors.neutral[900],
                marginBottom: '16px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}>
                <Building size={20} style={{ color: designSystem.colors.primary }} />
                Project Details
              </h3>
              
              <div style={{ display: 'grid', gap: '16px' }}>
                <div>
                  <label style={{
                    display: 'block',
                    fontSize: '14px',
                    fontWeight: '500',
                    color: designSystem.colors.neutral[700],
                    marginBottom: '6px'
                  }}>
                    Primary Use Cases
                  </label>
                  <textarea
                    value={formData.use_cases}
                    onChange={(e) => handleInputChange('use_cases', e.target.value)}
                    rows={3}
                    style={{
                      width: '100%',
                      padding: '12px',
                      border: `1px solid ${designSystem.colors.neutral[300]}`,
                      borderRadius: '8px',
                      fontSize: '16px',
                      outline: 'none',
                      resize: 'vertical'
                    }}
                    placeholder="Describe how you plan to use synthetic EHR data..."
                  />
                </div>
                
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                  <div>
                    <label style={{
                      display: 'block',
                      fontSize: '14px',
                      fontWeight: '500',
                      color: designSystem.colors.neutral[700],
                      marginBottom: '6px'
                    }}>
                      Company Size
                    </label>
                    <select
                      value={formData.company_size}
                      onChange={(e) => handleInputChange('company_size', e.target.value)}
                      style={{
                        width: '100%',
                        padding: '12px',
                        border: `1px solid ${designSystem.colors.neutral[300]}`,
                        borderRadius: '8px',
                        fontSize: '16px',
                        outline: 'none',
                        backgroundColor: 'white'
                      }}
                    >
                      <option value="">Select size</option>
                      <option value="1-10">1-10 employees</option>
                      <option value="11-50">11-50 employees</option>
                      <option value="51-200">51-200 employees</option>
                      <option value="201-1000">201-1000 employees</option>
                      <option value="1000+">1000+ employees</option>
                    </select>
                  </div>
                  
                  <div>
                    <label style={{
                      display: 'block',
                      fontSize: '14px',
                      fontWeight: '500',
                      color: designSystem.colors.neutral[700],
                      marginBottom: '6px'
                    }}>
                      Timeline
                    </label>
                    <select
                      value={formData.timeline}
                      onChange={(e) => handleInputChange('timeline', e.target.value)}
                      style={{
                        width: '100%',
                        padding: '12px',
                        border: `1px solid ${designSystem.colors.neutral[300]}`,
                        borderRadius: '8px',
                        fontSize: '16px',
                        outline: 'none',
                        backgroundColor: 'white'
                      }}
                    >
                      <option value="">When do you need this?</option>
                      <option value="immediately">Immediately</option>
                      <option value="1-3 months">1-3 months</option>
                      <option value="3-6 months">3-6 months</option>
                      <option value="6+ months">6+ months</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>

            {/* Design Partner Option */}
            <div style={{
              padding: '20px',
              backgroundColor: designSystem.colors.neutral[50],
              borderRadius: '12px',
              border: `1px solid ${designSystem.colors.neutral[200]}`
            }}>
              <label style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                cursor: 'pointer',
                fontSize: '16px',
                fontWeight: '500',
                color: designSystem.colors.neutral[800]
              }}>
                <input
                  type="checkbox"
                  checked={formData.interested_in_design_partner}
                  onChange={(e) => handleInputChange('interested_in_design_partner', e.target.checked)}
                  style={{
                    width: '18px',
                    height: '18px',
                    accentColor: designSystem.colors.primary
                  }}
                />
                Interested in becoming a design partner
              </label>
              <p style={{
                marginTop: '8px',
                marginLeft: '30px',
                fontSize: '14px',
                color: designSystem.colors.neutral[600],
                margin: '8px 0 0 30px'
              }}>
                Get early access and help shape the product roadmap
              </p>
            </div>
          </div>

          {/* Submit Button */}
          <div style={{ marginTop: '32px' }}>
            <button
              type="submit"
              disabled={isSubmitting}
              style={{
                width: '100%',
                padding: '14px 24px',
                backgroundColor: isSubmitting ? designSystem.colors.neutral[300] : designSystem.colors.primary,
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                fontSize: '16px',
                fontWeight: '600',
                cursor: isSubmitting ? 'not-allowed' : 'pointer',
                transition: 'all 0.2s',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px'
              }}
            >
              {isSubmitting ? (
                <>
                  <Loader size={20} style={{ animation: 'spin 1s linear infinite' }} />
                  Joining Waitlist...
                </>
              ) : (
                <>
                  <Mail size={20} />
                  Join Waitlist
                </>
              )}
            </button>
          </div>

          <p style={{
            textAlign: 'center',
            fontSize: '12px',
            color: designSystem.colors.neutral[500],
            marginTop: '16px',
            lineHeight: '1.5'
          }}>
            By joining, you agree to receive updates about Synthetic Ascension. We respect your privacy and won't spam you.
          </p>
        </form>
      </div>
    </div>
  );
};

export default WaitlistModal;