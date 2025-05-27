import React from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Heart, TestTube, FileText, Activity, Calendar, User, Pill } from 'lucide-react'

const PatientRecord: React.FC = () => {
  const { patientId } = useParams<{ patientId: string }>()
  const navigate = useNavigate()

  // Function to generate realistic patient photo based on demographics
  const generatePatientPhoto = (demographics, patientId) => {
    // Using This Person Does Not Exist API to generate realistic photos
    // Based on demographic characteristics for authentic representation
    const seed = patientId.replace(/\D/g, '') // Extract numbers for consistent seed
    const genderParam = demographics.gender.toLowerCase() === 'female' ? 'women' : 'men'
    const ageGroup = demographics.age < 12 ? 'child' : demographics.age < 18 ? 'teen' : 'adult'
    
    // Generate realistic photo URL based on demographics
    return `https://this-person-does-not-exist.com/img/avatar-${seed}${genderParam.charAt(0)}.jpg`
  }

  // Comprehensive patient data with all modalities
  const patientData = {
    'CHD-2024-001': {
      patient_id: "CHD-2024-001",
      demographics: {
        age: 8,
        gender: "Female",
        ethnicity: "Hispanic/Latino",
        date_of_birth: "2016-03-15",
        weight: "25.2 kg",
        height: "125 cm",
        bmi: "16.1 kg/m²"
      },
      photo: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150&h=150&fit=crop&crop=face&q=80",
      medical_images: [
        {
          type: "Echocardiogram Video",
          url: "https://via.placeholder.com/400x300/4F46E5/FFFFFF?text=Echo+Video+Replay",
          description: "Apical 4-chamber view showing post-surgical anatomy"
        },
        {
          type: "Chest X-Ray",
          url: "https://via.placeholder.com/300x400/059669/FFFFFF?text=Chest+X-Ray",
          description: "Post-operative chest radiograph"
        },
        {
          type: "Cardiac MRI",
          url: "https://via.placeholder.com/350x350/DC2626/FFFFFF?text=Cardiac+MRI",
          description: "Cardiac function assessment"
        }
      ],
      primary_diagnosis: "Tetralogy of Fallot",
      secondary_conditions: ["Pulmonary Stenosis", "Iron Deficiency Anemia"],
      surgical_history: [
        {
          date: "2018-05-22",
          procedure: "Complete intracardiac repair",
          surgeon: "Dr. Sarah Chen",
          hospital: "Children's Hospital of Philadelphia",
          notes: "Successful VSD closure and pulmonary valve repair. No complications."
        }
      ],
      medications: [
        { name: "Aspirin", dose: "81mg daily", indication: "Antiplatelet therapy", started: "2018-05-25" },
        { name: "Iron sulfate", dose: "325mg twice daily", indication: "Iron deficiency anemia", started: "2023-01-10" },
        { name: "Furosemide", dose: "20mg daily", indication: "Fluid management", started: "2023-06-15" }
      ],
      laboratory_results: [
        {
          date: "2024-05-15",
          test: "Complete Blood Count",
          results: {
            hemoglobin: "10.2 g/dL",
            hematocrit: "30.8%",
            platelet_count: "285,000/μL",
            wbc_count: "7,200/μL"
          },
          interpretation: "Mild anemia consistent with iron deficiency"
        },
        {
          date: "2024-05-15",
          test: "Iron Studies",
          results: {
            serum_iron: "45 μg/dL",
            tibc: "420 μg/dL",
            ferritin: "12 ng/mL",
            transferrin_saturation: "11%"
          },
          interpretation: "Iron deficiency confirmed"
        },
        {
          date: "2024-05-15",
          test: "BNP",
          results: {
            bnp: "125 pg/mL"
          },
          interpretation: "Mildly elevated, consistent with mild heart failure"
        }
      ],
      echocardiography: [
        {
          date: "2024-05-10",
          technician: "Sarah Johnson, RDCS",
          findings: {
            left_ventricular_ef: "58%",
            right_ventricular_function: "Normal",
            pulmonary_valve: "Mild regurgitation",
            tricuspid_valve: "Trace regurgitation",
            aortic_valve: "Normal",
            mitral_valve: "Normal"
          },
          measurements: {
            lvedd: "3.8 cm",
            lvesd: "2.4 cm",
            ivs: "0.8 cm",
            pw: "0.7 cm"
          },
          interpretation: "Good post-surgical result with preserved biventricular function"
        }
      ],
      clinical_notes: [
        {
          date: "2024-05-15",
          provider: "Dr. Michael Rodriguez, MD",
          type: "Cardiology Follow-up",
          soap: {
            subjective: "Patient reports good exercise tolerance. No chest pain, shortness of breath, or palpitations. Mother notes improved energy levels since starting iron supplementation.",
            objective: "Vital signs stable. Heart rate 85 bpm, BP 95/60 mmHg. Physical exam reveals regular rate and rhythm with soft systolic murmur at LUSB. No peripheral edema. Weight gain appropriate for age.",
            assessment: "Tetralogy of Fallot s/p complete repair with good hemodynamic result. Iron deficiency anemia improving with supplementation.",
            plan: "Continue current medications. Repeat echo in 6 months. Iron studies in 3 months. Encourage regular physical activity with sports clearance."
          }
        },
        {
          date: "2024-02-20",
          provider: "Dr. Jennifer Liu, MD",
          type: "Hematology Consultation",
          soap: {
            subjective: "Referred for evaluation of persistent anemia. Fatigue and decreased exercise tolerance over past 6 months.",
            objective: "Pale conjunctiva noted. Heart murmur consistent with known CHD. Lab results show microcytic hypochromic anemia.",
            assessment: "Iron deficiency anemia in setting of CHD. Likely nutritional deficiency.",
            plan: "Initiate oral iron supplementation. Dietary counseling. Follow-up in 3 months with repeat CBC and iron studies."
          }
        }
      ],
      follow_up_status: "Active",
      risk_score: "Medium",
      next_appointment: "2024-11-15",
      care_team: [
        { name: "Dr. Michael Rodriguez", role: "Pediatric Cardiologist", primary: true },
        { name: "Dr. Jennifer Liu", role: "Pediatric Hematologist", primary: false },
        { name: "Sarah Johnson", role: "Cardiac Sonographer", primary: false }
      ]
    },
    'CHD-2024-002': {
      patient_id: "CHD-2024-002",
      demographics: {
        age: 15,
        gender: "Male",
        ethnicity: "Caucasian",
        date_of_birth: "2009-08-12",
        weight: "58.5 kg",
        height: "168 cm",
        bmi: "20.7 kg/m²"
      },
      photo: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face&q=80",
      medical_images: [
        {
          type: "Fontan MRI Video",
          url: "https://via.placeholder.com/400x300/8B5CF6/FFFFFF?text=Fontan+MRI+Cine",
          description: "Fontan circulation flow assessment"
        },
        {
          type: "Chest X-Ray Series",
          url: "https://via.placeholder.com/300x400/10B981/FFFFFF?text=CXR+Series",
          description: "Serial chest radiographs showing Fontan anatomy"
        },
        {
          type: "Echo Doppler",
          url: "https://via.placeholder.com/350x350/F59E0B/FFFFFF?text=Echo+Doppler",
          description: "Doppler assessment of systemic ventricular function"
        }
      ],
      primary_diagnosis: "Hypoplastic Left Heart Syndrome",
      secondary_conditions: ["Protein-losing Enteropathy", "Thrombocytopenia"],
      surgical_history: [
        {
          date: "2009-08-20",
          procedure: "Norwood procedure",
          surgeon: "Dr. James Park",
          hospital: "Boston Children's Hospital",
          notes: "Stage 1 palliation completed successfully"
        },
        {
          date: "2010-02-15",
          procedure: "Glenn shunt",
          surgeon: "Dr. James Park",
          hospital: "Boston Children's Hospital",
          notes: "Stage 2 palliation with bidirectional cavopulmonary connection"
        },
        {
          date: "2012-11-30",
          procedure: "Fontan completion",
          surgeon: "Dr. James Park",
          hospital: "Boston Children's Hospital",
          notes: "Extracardiac conduit Fontan with fenestration"
        }
      ],
      medications: [
        { name: "Warfarin", dose: "2.5mg daily", indication: "Anticoagulation", started: "2012-12-05" },
        { name: "Enalapril", dose: "5mg twice daily", indication: "Heart failure management", started: "2013-01-15" },
        { name: "Albumin supplements", dose: "25g IV weekly", indication: "Protein-losing enteropathy", started: "2023-03-20" }
      ],
      laboratory_results: [
        {
          date: "2024-05-20",
          test: "Complete Blood Count",
          results: {
            hemoglobin: "11.8 g/dL",
            hematocrit: "35.4%",
            platelet_count: "145,000/μL",
            wbc_count: "6,800/μL"
          },
          interpretation: "Mild thrombocytopenia, hemoglobin low-normal"
        },
        {
          date: "2024-05-20",
          test: "Comprehensive Metabolic Panel",
          results: {
            albumin: "2.8 g/dL",
            total_protein: "5.2 g/dL",
            creatinine: "0.9 mg/dL",
            bun: "18 mg/dL"
          },
          interpretation: "Hypoproteinemia consistent with protein-losing enteropathy"
        },
        {
          date: "2024-05-20",
          test: "Coagulation Studies",
          results: {
            pt: "16.2 seconds",
            ptt: "28 seconds",
            inr: "1.8"
          },
          interpretation: "Therapeutic anticoagulation on warfarin"
        }
      ],
      echocardiography: [
        {
          date: "2024-05-18",
          technician: "Mark Thompson, RDCS",
          findings: {
            systemic_ventricular_ef: "45%",
            av_valve_function: "Moderate regurgitation",
            fontan_pathway: "Unobstructed",
            pulmonary_arteries: "Good size and flow"
          },
          measurements: {
            systemic_ventricle: "Mildly dilated",
            av_valve_annulus: "2.8 cm"
          },
          interpretation: "Stable Fontan physiology with mild systemic ventricular dysfunction"
        }
      ],
      clinical_notes: [
        {
          date: "2024-05-20",
          provider: "Dr. Amanda Foster, MD",
          type: "Fontan Follow-up",
          soap: {
            subjective: "Patient reports stable exercise tolerance. Occasionally feels short of breath with strenuous activity. No chest pain or syncope. Compliance with medications good.",
            objective: "Appears well. O2 saturation 88% on room air (baseline). Heart rate 70 bpm, BP 105/65 mmHg. Cardiac exam reveals single S2, no murmur. Mild lower extremity edema.",
            assessment: "HLHS s/p Fontan with stable physiology. Protein-losing enteropathy controlled with albumin supplementation.",
            plan: "Continue current regimen. Consider heart transplant evaluation if ventricular function deteriorates further. Follow-up in 3 months."
          }
        }
      ],
      follow_up_status: "Active",
      risk_score: "High",
      next_appointment: "2024-08-20",
      care_team: [
        { name: "Dr. Amanda Foster", role: "Pediatric Cardiologist", primary: true },
        { name: "Dr. Robert Kim", role: "Heart Failure Specialist", primary: false },
        { name: "Mark Thompson", role: "Cardiac Sonographer", primary: false }
      ]
    }
  }

  const patient = patientData[patientId as keyof typeof patientData]

  if (!patient) {
    return (
      <div style={{ minHeight: '100vh', backgroundColor: '#f8fafc', padding: '64px 24px', textAlign: 'center' }}>
        <h1 style={{ fontSize: '24px', fontWeight: '600', color: '#374151', marginBottom: '16px' }}>
          Patient Not Found
        </h1>
        <p style={{ fontSize: '16px', color: '#6b7280', marginBottom: '32px' }}>
          The patient record you're looking for doesn't exist.
        </p>
        <button
          onClick={() => navigate('/results')}
          style={{
            backgroundColor: '#3b82f6',
            color: 'white',
            padding: '12px 24px',
            borderRadius: '8px',
            border: 'none',
            fontWeight: '500',
            cursor: 'pointer'
          }}
        >
          Back to Results
        </button>
      </div>
    )
  }

  const styles = {
    container: {
      minHeight: '100vh',
      backgroundColor: '#f8fafc',
      fontFamily: 'Inter, system-ui, sans-serif'
    },
    header: {
      backgroundColor: '#ffffff',
      borderBottom: '1px solid #e5e7eb',
      padding: '16px 0'
    },
    nav: {
      maxWidth: '1200px',
      margin: '0 auto',
      padding: '0 24px',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    },
    logo: {
      display: 'flex',
      alignItems: 'center',
      gap: '12px'
    },
    logoIcon: {
      width: '32px',
      height: '32px',
      backgroundColor: '#3b82f6',
      color: 'white',
      borderRadius: '8px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontWeight: 'bold',
      fontSize: '14px'
    },
    logoText: {
      fontSize: '20px',
      fontWeight: '600',
      color: '#1f2937'
    },
    main: {
      maxWidth: '1200px',
      margin: '0 auto',
      padding: '32px 24px'
    },
    backButton: {
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      backgroundColor: '#f3f4f6',
      color: '#374151',
      padding: '8px 16px',
      borderRadius: '8px',
      border: 'none',
      fontWeight: '500',
      cursor: 'pointer',
      fontSize: '14px',
      marginBottom: '24px'
    },
    patientHeader: {
      backgroundColor: '#ffffff',
      padding: '24px',
      borderRadius: '12px',
      border: '1px solid #e5e7eb',
      marginBottom: '24px'
    },
    patientTitle: {
      fontSize: '28px',
      fontWeight: '700',
      color: '#1f2937',
      marginBottom: '8px'
    },
    patientSubtitle: {
      fontSize: '18px',
      color: '#6b7280',
      marginBottom: '16px'
    },
    demographicsGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
      gap: '16px'
    },
    demographicItem: {
      display: 'flex',
      justifyContent: 'space-between',
      fontSize: '14px'
    },
    sectionGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
      gap: '24px'
    },
    card: {
      backgroundColor: '#ffffff',
      padding: '24px',
      borderRadius: '12px',
      border: '1px solid #e5e7eb',
      marginBottom: '24px'
    },
    cardTitle: {
      fontSize: '20px',
      fontWeight: '600',
      color: '#1f2937',
      marginBottom: '16px',
      display: 'flex',
      alignItems: 'center',
      gap: '8px'
    },
    riskBadge: {
      padding: '4px 12px',
      borderRadius: '16px',
      fontSize: '12px',
      fontWeight: '500',
      display: 'inline-block'
    }
  }

  const getRiskBadgeStyle = (risk: string) => {
    const baseStyle = styles.riskBadge
    switch (risk) {
      case 'High':
        return { ...baseStyle, backgroundColor: '#fef2f2', color: '#dc2626' }
      case 'Medium':
        return { ...baseStyle, backgroundColor: '#fef3c7', color: '#d97706' }
      case 'Low':
        return { ...baseStyle, backgroundColor: '#f0fdf4', color: '#16a34a' }
      default:
        return { ...baseStyle, backgroundColor: '#f3f4f6', color: '#374151' }
    }
  }

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <nav style={styles.nav}>
          <div style={styles.logo}>
            <div style={styles.logoIcon}>SA</div>
            <span style={styles.logoText}>Synthetic Ascension</span>
          </div>
          <div>
            <span style={{ fontSize: '14px', color: '#6b7280' }}>
              Patient Record View
            </span>
          </div>
        </nav>
      </header>

      <main style={styles.main}>
        <button style={styles.backButton} onClick={() => navigate('/results')}>
          <ArrowLeft size={16} />
          Back to Results
        </button>

        {/* Patient Header */}
        <div style={styles.patientHeader}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'start', gap: '24px' }}>
              {/* Patient Photo */}
              <div style={{
                width: '120px',
                height: '120px',
                borderRadius: '12px',
                overflow: 'hidden',
                border: '3px solid #e5e7eb',
                flexShrink: 0
              }}>
                <img 
                  src={patient.photo}
                  alt={`Patient ${patient.patient_id}`}
                  style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover'
                  }}
                  onError={(e) => {
                    e.target.src = `https://ui-avatars.com/api/?name=${patient.demographics.gender}&background=3b82f6&color=ffffff&size=120`
                  }}
                />
              </div>
              
              <div>
                <h1 style={styles.patientTitle}>Patient {patient.patient_id}</h1>
                <p style={styles.patientSubtitle}>{patient.primary_diagnosis}</p>
                <div style={{ fontSize: '14px', color: '#6b7280', marginTop: '8px' }}>
                  {patient.demographics.age}-year-old {patient.demographics.ethnicity} {patient.demographics.gender.toLowerCase()}
                </div>
              </div>
            </div>
            <span style={getRiskBadgeStyle(patient.risk_score)}>
              {patient.risk_score} Risk
            </span>
          </div>

          <div style={styles.demographicsGrid}>
            <div style={styles.demographicItem}>
              <span style={{ fontWeight: '500' }}>Age:</span>
              <span style={{ color: '#6b7280' }}>{patient.demographics.age} years</span>
            </div>
            <div style={styles.demographicItem}>
              <span style={{ fontWeight: '500' }}>Gender:</span>
              <span style={{ color: '#6b7280' }}>{patient.demographics.gender}</span>
            </div>
            <div style={styles.demographicItem}>
              <span style={{ fontWeight: '500' }}>Ethnicity:</span>
              <span style={{ color: '#6b7280' }}>{patient.demographics.ethnicity}</span>
            </div>
            <div style={styles.demographicItem}>
              <span style={{ fontWeight: '500' }}>Weight:</span>
              <span style={{ color: '#6b7280' }}>{patient.demographics.weight}</span>
            </div>
            <div style={styles.demographicItem}>
              <span style={{ fontWeight: '500' }}>Height:</span>
              <span style={{ color: '#6b7280' }}>{patient.demographics.height}</span>
            </div>
            <div style={styles.demographicItem}>
              <span style={{ fontWeight: '500' }}>BMI:</span>
              <span style={{ color: '#6b7280' }}>{patient.demographics.bmi}</span>
            </div>
          </div>
        </div>

        {/* Medical Images Gallery */}
        {patient.medical_images && patient.medical_images.length > 0 && (
          <div style={{
            backgroundColor: 'white',
            borderRadius: '12px',
            padding: '24px',
            marginBottom: '24px',
            border: '1px solid #e5e7eb'
          }}>
            <h3 style={{
              margin: '0 0 20px 0',
              fontSize: '18px',
              fontWeight: '600',
              color: '#1f2937',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}>
              <span style={{
                width: '24px',
                height: '24px',
                backgroundColor: '#3b82f6',
                borderRadius: '6px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                fontSize: '12px'
              }}>📸</span>
              Medical Images & Videos
            </h3>
            
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
              gap: '20px'
            }}>
              {patient.medical_images.map((image, index) => (
                <div key={index} style={{
                  border: '2px solid #e5e7eb',
                  borderRadius: '12px',
                  overflow: 'hidden',
                  backgroundColor: '#f9fafb',
                  transition: 'all 0.2s ease',
                  cursor: 'pointer'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.borderColor = '#3b82f6'
                  e.currentTarget.style.transform = 'scale(1.02)'
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = '#e5e7eb'
                  e.currentTarget.style.transform = 'scale(1)'
                }}
                onClick={() => window.open(image.url, '_blank')}
                >
                  <div style={{
                    height: '200px',
                    backgroundColor: '#f3f4f6',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    position: 'relative'
                  }}>
                    <img 
                      src={image.url}
                      alt={image.type}
                      style={{
                        maxWidth: '100%',
                        maxHeight: '100%',
                        objectFit: 'contain'
                      }}
                    />
                    {image.type.toLowerCase().includes('video') && (
                      <div style={{
                        position: 'absolute',
                        top: '50%',
                        left: '50%',
                        transform: 'translate(-50%, -50%)',
                        backgroundColor: 'rgba(0,0,0,0.7)',
                        borderRadius: '50%',
                        width: '60px',
                        height: '60px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: 'white',
                        fontSize: '24px'
                      }}>
                        ▶️
                      </div>
                    )}
                  </div>
                  
                  <div style={{ padding: '16px' }}>
                    <h4 style={{
                      margin: '0 0 8px 0',
                      fontSize: '16px',
                      fontWeight: '600',
                      color: '#1f2937'
                    }}>
                      {image.type}
                    </h4>
                    <p style={{
                      margin: '0',
                      fontSize: '14px',
                      color: '#6b7280',
                      lineHeight: '1.4'
                    }}>
                      {image.description}
                    </p>
                    <div style={{
                      marginTop: '12px',
                      fontSize: '12px',
                      color: '#3b82f6',
                      fontWeight: '500'
                    }}>
                      Click to view full size
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Clinical Data Sections */}
        <div style={styles.sectionGrid}>
          {/* Current Medications */}
          <div style={styles.card}>
            <h3 style={styles.cardTitle}>
              <Pill className="w-5 h-5 text-green-600" />
              Current Medications
            </h3>
            <div style={{ display: 'grid', gap: '12px' }}>
              {patient.medications.map((med, index) => (
                <div key={index} style={{ 
                  padding: '12px', 
                  backgroundColor: '#f9fafb', 
                  borderRadius: '8px',
                  border: '1px solid #e5e7eb'
                }}>
                  <div style={{ fontSize: '14px', fontWeight: '500', color: '#374151', marginBottom: '4px' }}>
                    {med.name} - {med.dose}
                  </div>
                  <div style={{ fontSize: '12px', color: '#6b7280', marginBottom: '2px' }}>
                    <strong>Indication:</strong> {med.indication}
                  </div>
                  <div style={{ fontSize: '12px', color: '#6b7280' }}>
                    <strong>Started:</strong> {med.started}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Laboratory Results */}
          <div style={styles.card}>
            <h3 style={styles.cardTitle}>
              <TestTube className="w-5 h-5 text-purple-600" />
              Latest Laboratory Results
            </h3>
            <div style={{ display: 'grid', gap: '16px' }}>
              {patient.laboratory_results.map((lab, index) => (
                <div key={index} style={{ 
                  padding: '16px', 
                  backgroundColor: '#f9fafb', 
                  borderRadius: '8px',
                  border: '1px solid #e5e7eb'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px' }}>
                    <div style={{ fontSize: '14px', fontWeight: '500', color: '#374151' }}>
                      {lab.test}
                    </div>
                    <div style={{ fontSize: '12px', color: '#6b7280' }}>
                      {lab.date}
                    </div>
                  </div>
                  <div style={{ display: 'grid', gap: '4px', marginBottom: '8px' }}>
                    {Object.entries(lab.results).map(([key, value]) => (
                      <div key={key} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px' }}>
                        <span style={{ color: '#6b7280' }}>{key.replace(/_/g, ' ').toUpperCase()}:</span>
                        <span style={{ fontWeight: '500' }}>{value}</span>
                      </div>
                    ))}
                  </div>
                  <div style={{ fontSize: '12px', color: '#059669', fontWeight: '500' }}>
                    {lab.interpretation}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Echocardiography */}
          <div style={styles.card}>
            <h3 style={styles.cardTitle}>
              <Heart className="w-5 h-5 text-red-600" />
              Latest Echocardiogram
            </h3>
            {patient.echocardiography.map((echo, index) => (
              <div key={index} style={{ 
                padding: '16px', 
                backgroundColor: '#f9fafb', 
                borderRadius: '8px',
                border: '1px solid #e5e7eb'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px' }}>
                  <div style={{ fontSize: '14px', fontWeight: '500', color: '#374151' }}>
                    Echocardiogram Report
                  </div>
                  <div style={{ fontSize: '12px', color: '#6b7280' }}>
                    {echo.date}
                  </div>
                </div>
                <div style={{ fontSize: '12px', color: '#6b7280', marginBottom: '12px' }}>
                  <strong>Technician:</strong> {echo.technician}
                </div>
                
                <div style={{ marginBottom: '12px' }}>
                  <div style={{ fontSize: '13px', fontWeight: '500', color: '#374151', marginBottom: '8px' }}>
                    Key Findings:
                  </div>
                  <div style={{ display: 'grid', gap: '4px' }}>
                    {Object.entries(echo.findings).map(([key, value]) => (
                      <div key={key} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px' }}>
                        <span style={{ color: '#6b7280' }}>{key.replace(/_/g, ' ').toUpperCase()}:</span>
                        <span style={{ fontWeight: '500' }}>{value}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div style={{ fontSize: '12px', color: '#059669', fontWeight: '500' }}>
                  {echo.interpretation}
                </div>
              </div>
            ))}
          </div>

          {/* Clinical Notes */}
          <div style={styles.card}>
            <h3 style={styles.cardTitle}>
              <FileText className="w-5 h-5 text-blue-600" />
              Recent Clinical Notes
            </h3>
            <div style={{ display: 'grid', gap: '16px' }}>
              {patient.clinical_notes.map((note, index) => (
                <div key={index} style={{ 
                  padding: '16px', 
                  backgroundColor: '#f9fafb', 
                  borderRadius: '8px',
                  border: '1px solid #e5e7eb'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px' }}>
                    <div>
                      <div style={{ fontSize: '14px', fontWeight: '500', color: '#374151' }}>
                        {note.type}
                      </div>
                      <div style={{ fontSize: '12px', color: '#6b7280' }}>
                        {note.provider}
                      </div>
                    </div>
                    <div style={{ fontSize: '12px', color: '#6b7280' }}>
                      {note.date}
                    </div>
                  </div>
                  
                  <div style={{ display: 'grid', gap: '8px' }}>
                    <div>
                      <div style={{ fontSize: '12px', fontWeight: '500', color: '#374151', marginBottom: '4px' }}>
                        SUBJECTIVE:
                      </div>
                      <div style={{ fontSize: '12px', color: '#6b7280' }}>
                        {note.soap.subjective}
                      </div>
                    </div>
                    <div>
                      <div style={{ fontSize: '12px', fontWeight: '500', color: '#374151', marginBottom: '4px' }}>
                        OBJECTIVE:
                      </div>
                      <div style={{ fontSize: '12px', color: '#6b7280' }}>
                        {note.soap.objective}
                      </div>
                    </div>
                    <div>
                      <div style={{ fontSize: '12px', fontWeight: '500', color: '#374151', marginBottom: '4px' }}>
                        ASSESSMENT:
                      </div>
                      <div style={{ fontSize: '12px', color: '#6b7280' }}>
                        {note.soap.assessment}
                      </div>
                    </div>
                    <div>
                      <div style={{ fontSize: '12px', fontWeight: '500', color: '#374151', marginBottom: '4px' }}>
                        PLAN:
                      </div>
                      <div style={{ fontSize: '12px', color: '#6b7280' }}>
                        {note.soap.plan}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Surgical History */}
          <div style={styles.card}>
            <h3 style={styles.cardTitle}>
              <Activity className="w-5 h-5 text-orange-600" />
              Surgical History
            </h3>
            <div style={{ display: 'grid', gap: '12px' }}>
              {patient.surgical_history.map((surgery, index) => (
                <div key={index} style={{ 
                  padding: '12px', 
                  backgroundColor: '#f9fafb', 
                  borderRadius: '8px',
                  border: '1px solid #e5e7eb'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <div style={{ fontSize: '14px', fontWeight: '500', color: '#374151' }}>
                      {surgery.procedure}
                    </div>
                    <div style={{ fontSize: '12px', color: '#6b7280' }}>
                      {surgery.date}
                    </div>
                  </div>
                  <div style={{ fontSize: '12px', color: '#6b7280', marginBottom: '4px' }}>
                    <strong>Surgeon:</strong> {surgery.surgeon}
                  </div>
                  <div style={{ fontSize: '12px', color: '#6b7280', marginBottom: '4px' }}>
                    <strong>Hospital:</strong> {surgery.hospital}
                  </div>
                  <div style={{ fontSize: '12px', color: '#6b7280' }}>
                    <strong>Notes:</strong> {surgery.notes}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Care Team */}
          <div style={styles.card}>
            <h3 style={styles.cardTitle}>
              <User className="w-5 h-5 text-indigo-600" />
              Care Team
            </h3>
            <div style={{ display: 'grid', gap: '8px' }}>
              {patient.care_team.map((member, index) => (
                <div key={index} style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between', 
                  alignItems: 'center',
                  padding: '8px 12px', 
                  backgroundColor: member.primary ? '#eff6ff' : '#f9fafb', 
                  borderRadius: '8px',
                  border: `1px solid ${member.primary ? '#bfdbfe' : '#e5e7eb'}`
                }}>
                  <div>
                    <div style={{ fontSize: '14px', fontWeight: '500', color: '#374151' }}>
                      {member.name}
                    </div>
                    <div style={{ fontSize: '12px', color: '#6b7280' }}>
                      {member.role}
                    </div>
                  </div>
                  {member.primary && (
                    <span style={{
                      backgroundColor: '#dbeafe',
                      color: '#1d4ed8',
                      padding: '2px 8px',
                      borderRadius: '12px',
                      fontSize: '10px',
                      fontWeight: '500'
                    }}>
                      PRIMARY
                    </span>
                  )}
                </div>
              ))}
            </div>
            
            <div style={{ marginTop: '16px', padding: '12px', backgroundColor: '#f0fdf4', borderRadius: '8px', border: '1px solid #bbf7d0' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                <Calendar className="w-4 h-4 text-green-600" />
                <span style={{ fontSize: '14px', fontWeight: '500', color: '#16a34a' }}>
                  Next Appointment
                </span>
              </div>
              <div style={{ fontSize: '12px', color: '#059669' }}>
                {patient.next_appointment} with {patient.care_team.find(m => m.primary)?.name}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default PatientRecord