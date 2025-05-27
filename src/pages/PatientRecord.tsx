import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, User, Heart, Activity, FlaskConical, Pill, Calendar, FileText, AlertCircle } from 'lucide-react'

const PatientRecord: React.FC = () => {
  const { patientId } = useParams<{ patientId: string }>()
  const navigate = useNavigate()
  const [patientData, setPatientData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeSection, setActiveSection] = useState('demographics')

  const handleBackClick = () => {
    navigate(-1)
  }

  useEffect(() => {
    // Fetch patient data from the enhanced API
    const fetchPatientData = async () => {
      try {
        const response = await fetch(`http://localhost:8080/api/patient/${patientId}`)
        if (response.ok) {
          const data = await response.json()
          setPatientData(data)
        } else {
          // Generate synthetic patient data for demonstration
          const syntheticData = generateSyntheticPatientData(patientId)
          setPatientData(syntheticData)
        }
      } catch (error) {
        // Generate synthetic patient data for demonstration
        const syntheticData = generateSyntheticPatientData(patientId)
        setPatientData(syntheticData)
      } finally {
        setLoading(false)
      }
    }

    if (patientId) {
      fetchPatientData()
    }
  }, [patientId])

  const generateSyntheticPatientData = (id) => {
    // Generate comprehensive synthetic EHR data matching hospital standards
    const baseAge = parseInt(id.split('-')[1]) || Math.floor(Math.random() * 18) + 1
    const gender = Math.random() > 0.5 ? 'Female' : 'Male'
    const birthDate = new Date(Date.now() - (baseAge * 365.25 * 24 * 60 * 60 * 1000))
    const weight = Math.round((15 + Math.random() * 45) * 10) / 10
    const height = Math.round(80 + Math.random() * 100)
    const bmi = Math.round((weight / ((height/100) ** 2)) * 10) / 10
    
    return {
      patient_id: id,
      demographics: {
        full_name: `Patient ${id.split('-')[2]}`,
        date_of_birth: birthDate.toISOString().split('T')[0],
        age: baseAge,
        sex: gender,
        gender_identity: gender,
        pronouns: gender === 'Male' ? 'He/Him' : 'She/Her',
        address: {
          street: `${Math.floor(Math.random() * 9999)} Medical Center Dr`,
          city: 'Children\'s Hospital City',
          state: 'CA',
          zip: '90210',
          country: 'USA'
        },
        contact: {
          phone: `(555) ${Math.floor(Math.random() * 900) + 100}-${Math.floor(Math.random() * 9000) + 1000}`,
          email: `guardian.${id.toLowerCase()}@email.com`,
          emergency_contact: 'Parent/Guardian',
          emergency_phone: `(555) ${Math.floor(Math.random() * 900) + 100}-${Math.floor(Math.random() * 9000) + 1000}`
        },
        race_ethnicity: {
          race: ['White', 'Black or African American', 'Asian', 'American Indian/Alaska Native', 'Native Hawaiian/Pacific Islander'][Math.floor(Math.random() * 5)],
          ethnicity: ['Not Hispanic or Latino', 'Hispanic or Latino'][Math.floor(Math.random() * 2)],
          primary_language: 'English'
        },
        insurance: {
          primary: 'Pediatric Health Plan',
          member_id: `PHP${Math.floor(Math.random() * 1000000)}`,
          group_number: 'GRP001',
          subscriber: 'Parent/Guardian'
        },
        anthropometrics: {
          weight_kg: weight,
          height_cm: height,
          bmi: bmi,
          bmi_percentile: Math.floor(Math.random() * 95) + 5,
          head_circumference_cm: baseAge < 3 ? Math.round(35 + Math.random() * 15) : null
        },
        medical_record_number: `MRN-${Math.floor(Math.random() * 1000000)}`
      },
      cardiac_profile: {
        primary_diagnosis: ['Tetralogy of Fallot', 'Ventricular Septal Defect', 'Atrial Septal Defect', 'Hypoplastic Left Heart Syndrome'][Math.floor(Math.random() * 4)],
        severity: ['Mild', 'Moderate', 'Severe'][Math.floor(Math.random() * 3)],
        surgical_history: [
          {
            procedure: 'Complete Intracardiac Repair',
            date: new Date(Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            surgeon: 'Dr. Johnson',
            outcome: 'Successful'
          }
        ],
        echo_findings: {
          ejection_fraction: Math.round((55 + Math.random() * 15) * 10) / 10,
          left_ventricular_function: ['Normal', 'Mildly Impaired', 'Moderately Impaired'][Math.floor(Math.random() * 3)],
          valve_function: 'Normal',
          wall_motion: 'Normal'
        }
      },
      problem_list: {
        active_diagnoses: [
          {
            condition: ['Tetralogy of Fallot', 'Ventricular Septal Defect', 'Atrial Septal Defect', 'Hypoplastic Left Heart Syndrome'][Math.floor(Math.random() * 4)],
            icd10_code: ['Q21.3', 'Q21.0', 'Q21.1', 'Q23.4'][Math.floor(Math.random() * 4)],
            onset_date: new Date(Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            status: 'Active',
            severity: ['Mild', 'Moderate', 'Severe'][Math.floor(Math.random() * 3)],
            certainty: 'Confirmed',
            domain: 'Cardiovascular'
          },
          {
            condition: 'Heart Failure',
            icd10_code: 'I50.9',
            onset_date: new Date(Date.now() - Math.random() * 180 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            status: 'Active',
            severity: 'Moderate',
            certainty: 'Confirmed',
            domain: 'Cardiovascular'
          }
        ]
      },
      allergies_adverse_reactions: [
        {
          allergen: 'Penicillin',
          type: 'Medication',
          reaction: 'Rash, Hives',
          severity: 'Moderate',
          onset_date: new Date(Date.now() - Math.random() * 1000 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          status: 'Active',
          triage_recommendation: 'Avoid - use alternative antibiotics'
        }
      ],
      laboratory_results: {
        panels: [
          {
            panel_name: 'Complete Blood Count with Differential',
            loinc_code: '58410-2',
            ordered_date: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            collected_date: new Date(Date.now() - Math.random() * 28 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            resulted_date: new Date(Date.now() - Math.random() * 27 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            ordering_provider: 'Dr. Sarah Chen, Pediatric Cardiology',
            status: 'Final',
            critical_flags: [],
            results: [
              {
                test: 'Hemoglobin',
                value: Math.round((11 + Math.random() * 4) * 10) / 10,
                unit: 'g/dL',
                reference_range: `${baseAge < 5 ? '11.0-14.0' : '12.0-15.5'} g/dL`,
                flag: ''
              },
              {
                test: 'Hematocrit',
                value: Math.round((33 + Math.random() * 12) * 10) / 10,
                unit: '%',
                reference_range: `${baseAge < 5 ? '33-41' : '36-46'}%`,
                flag: ''
              },
              {
                test: 'White Blood Cell Count',
                value: Math.round((4 + Math.random() * 8) * 100) / 100,
                unit: 'K/uL',
                reference_range: `${baseAge < 2 ? '6.0-17.5' : baseAge < 6 ? '5.0-15.5' : '4.5-13.5'} K/uL`,
                flag: ''
              },
              {
                test: 'Platelet Count',
                value: Math.round(150 + Math.random() * 300),
                unit: 'K/uL',
                reference_range: '150-450 K/uL',
                flag: ''
              }
            ]
          },
          {
            panel_name: 'Comprehensive Metabolic Panel',
            loinc_code: '24323-8',
            ordered_date: new Date(Date.now() - Math.random() * 21 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            collected_date: new Date(Date.now() - Math.random() * 20 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            resulted_date: new Date(Date.now() - Math.random() * 19 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            ordering_provider: 'Dr. Sarah Chen, Pediatric Cardiology',
            status: 'Final',
            critical_flags: [],
            results: [
              {
                test: 'Glucose',
                value: Math.round(70 + Math.random() * 50),
                unit: 'mg/dL',
                reference_range: '70-100 mg/dL',
                flag: ''
              },
              {
                test: 'Creatinine',
                value: Math.round((0.3 + Math.random() * 0.5) * 100) / 100,
                unit: 'mg/dL',
                reference_range: `${baseAge < 1 ? '0.2-0.4' : baseAge < 3 ? '0.3-0.7' : '0.5-1.0'} mg/dL`,
                flag: ''
              },
              {
                test: 'Sodium',
                value: Math.round(135 + Math.random() * 10),
                unit: 'mEq/L',
                reference_range: '135-145 mEq/L',
                flag: ''
              },
              {
                test: 'Potassium',
                value: Math.round((3.5 + Math.random() * 1.5) * 10) / 10,
                unit: 'mEq/L',
                reference_range: '3.5-5.0 mEq/L',
                flag: ''
              }
            ]
          },
          {
            panel_name: 'BNP (B-type Natriuretic Peptide)',
            loinc_code: '33762-6',
            ordered_date: new Date(Date.now() - Math.random() * 14 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            collected_date: new Date(Date.now() - Math.random() * 13 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            resulted_date: new Date(Date.now() - Math.random() * 12 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            ordering_provider: 'Dr. Sarah Chen, Pediatric Cardiology',
            status: 'Final',
            critical_flags: [],
            results: [
              {
                test: 'BNP',
                value: Math.round(20 + Math.random() * 180),
                unit: 'pg/mL',
                reference_range: '<100 pg/mL',
                flag: Math.random() > 0.7 ? 'H' : ''
              }
            ]
          }
        ]
      },
      medication_history: {
        current_medications: [
          {
            name: 'Furosemide (Lasix)',
            rxnorm_code: '4603',
            generic_name: 'Furosemide',
            brand_name: 'Lasix',
            dosage: `${Math.round((1 + Math.random() * 2) * 10) / 10} mg/kg/day`,
            dose_amount: `${Math.round((5 + Math.random() * 15) * 10) / 10} mg`,
            route: 'PO (By mouth)',
            frequency: 'BID (Twice daily)',
            start_date: new Date(Date.now() - Math.random() * 180 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            prescriber: 'Dr. Sarah Chen, Pediatric Cardiology',
            indication: 'Heart failure management - fluid retention',
            status: 'Active',
            pharmacy: 'Children\'s Hospital Pharmacy',
            last_filled: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            quantity_dispensed: '30 tablets',
            refills_remaining: Math.floor(Math.random() * 6)
          },
          {
            name: 'Enalapril (Vasotec)',
            rxnorm_code: '3827',
            generic_name: 'Enalapril',
            brand_name: 'Vasotec',
            dosage: '0.1 mg/kg/dose',
            dose_amount: `${Math.round((2.5 + Math.random() * 7.5) * 10) / 10} mg`,
            route: 'PO (By mouth)',
            frequency: 'BID (Twice daily)',
            start_date: new Date(Date.now() - Math.random() * 180 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            prescriber: 'Dr. Sarah Chen, Pediatric Cardiology',
            indication: 'Afterload reduction - ACE inhibitor therapy',
            status: 'Active',
            pharmacy: 'Children\'s Hospital Pharmacy',
            last_filled: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            quantity_dispensed: '60 tablets',
            refills_remaining: Math.floor(Math.random() * 6)
          }
        ],
        discontinued_medications: [
          {
            name: 'Digoxin',
            rxnorm_code: '3407',
            start_date: new Date(Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            stop_date: new Date(Date.now() - Math.random() * 90 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            reason_discontinued: 'Therapeutic levels achieved with current regimen',
            prescriber: 'Dr. Sarah Chen, Pediatric Cardiology'
          }
        ]
      },
      imaging_diagnostics: {
        studies: [
          {
            study_type: 'Echocardiogram (2D Echo with Doppler)',
            modality: 'Ultrasound',
            study_date: new Date(Date.now() - Math.random() * 60 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            ordering_provider: 'Dr. Sarah Chen, Pediatric Cardiology',
            performing_technologist: 'Jennifer Rodriguez, RDCS',
            interpreting_radiologist: 'Dr. Michael Thompson, Pediatric Cardiology',
            status: 'Final Report',
            indication: 'Follow-up congenital heart disease',
            technique: '2D, M-mode, and Doppler echocardiography',
            findings: {
              summary: 'Stable moderate ventricular septal defect with adequate biventricular function',
              ejection_fraction: `${Math.round((55 + Math.random() * 15) * 10) / 10}%`,
              left_ventricle: 'Normal size and systolic function',
              right_ventricle: 'Mildly dilated with normal function',
              valves: 'Tricuspid regurgitation - mild; other valves normal',
              septal_defect: `Moderate perimembranous VSD, ${Math.round((8 + Math.random() * 4) * 10) / 10}mm`
            },
            impression: 'Stable moderate VSD with good biventricular function. No significant change from prior study.',
            recommendations: 'Continue current medical management. Follow-up echo in 6 months.',
            comparison: 'Compared to prior echo dated 6 months ago - stable findings'
          },
          {
            study_type: 'Chest X-Ray (PA and Lateral)',
            modality: 'Radiography',
            study_date: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            ordering_provider: 'Dr. Sarah Chen, Pediatric Cardiology',
            interpreting_radiologist: 'Dr. Lisa Park, Pediatric Radiology',
            status: 'Final Report',
            indication: 'Evaluation of cardiac silhouette and pulmonary vasculature',
            technique: 'PA and lateral chest radiographs',
            findings: {
              heart: 'Normal cardiac silhouette, cardiothoracic ratio within normal limits',
              lungs: 'Clear bilateral lung fields, no acute infiltrates',
              bones: 'No acute osseous abnormalities',
              mediastinum: 'Normal mediastinal contours'
            },
            impression: 'Normal chest radiograph.',
            comparison: 'Stable compared to prior chest X-ray 3 months ago'
          }
        ]
      },
      clinical_encounters: [
        {
          date: new Date(Date.now() - Math.random() * 90 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          type: 'Cardiology Follow-up',
          provider: 'Dr. Smith, Pediatric Cardiologist',
          chief_complaint: 'Routine follow-up',
          assessment: 'Stable congenital heart disease',
          plan: 'Continue current medications, follow-up in 6 months'
        },
        {
          date: new Date(Date.now() - Math.random() * 180 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          type: 'Emergency Department Visit',
          provider: 'Dr. Williams, Emergency Medicine',
          chief_complaint: 'Shortness of breath',
          assessment: 'Acute heart failure exacerbation',
          plan: 'Admitted for diuresis and medication adjustment'
        }
      ],
      vital_signs: {
        recent_measurements: [
          {
            date: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            heart_rate: Math.round(80 + Math.random() * 40),
            blood_pressure_systolic: Math.round(90 + Math.random() * 30),
            blood_pressure_diastolic: Math.round(50 + Math.random() * 20),
            oxygen_saturation: Math.round((95 + Math.random() * 5) * 10) / 10,
            temperature_f: Math.round((97 + Math.random() * 4) * 10) / 10
          }
        ]
      },
      growth_data: {
        height_percentile: Math.round(Math.random() * 100),
        weight_percentile: Math.round(Math.random() * 100),
        bmi_percentile: Math.round(Math.random() * 100)
      }
    }
  }

  const renderSectionContent = () => {
    if (loading) {
      return (
        <div style={{ textAlign: 'center', padding: '64px' }}>
          <div style={{ fontSize: '18px', color: '#6b7280' }}>Loading patient data...</div>
        </div>
      )
    }

    if (!patientData) {
      return (
        <div style={{ textAlign: 'center', padding: '64px' }}>
          <div style={{ fontSize: '18px', color: '#ef4444' }}>Patient data not found</div>
        </div>
      )
    }

    switch (activeSection) {
      case 'demographics':
        return (
          <div style={styles.sectionContent}>
            <h3 style={styles.sectionTitle}>Demographics & Basic Information</h3>
            <div style={styles.dataGrid}>
              <div style={styles.dataItem}>
                <span style={styles.dataLabel}>Medical Record Number:</span>
                <span style={styles.dataValue}>{patientData.demographics.medical_record_number}</span>
              </div>
              <div style={styles.dataItem}>
                <span style={styles.dataLabel}>Age:</span>
                <span style={styles.dataValue}>{patientData.demographics.age} years old</span>
              </div>
              <div style={styles.dataItem}>
                <span style={styles.dataLabel}>Gender:</span>
                <span style={styles.dataValue}>{patientData.demographics.gender}</span>
              </div>
              <div style={styles.dataItem}>
                <span style={styles.dataLabel}>Date of Birth:</span>
                <span style={styles.dataValue}>{patientData.demographics.date_of_birth}</span>
              </div>
              <div style={styles.dataItem}>
                <span style={styles.dataLabel}>Ethnicity:</span>
                <span style={styles.dataValue}>{patientData.demographics.ethnicity}</span>
              </div>
              <div style={styles.dataItem}>
                <span style={styles.dataLabel}>Weight:</span>
                <span style={styles.dataValue}>{patientData.demographics.weight_kg} kg</span>
              </div>
              <div style={styles.dataItem}>
                <span style={styles.dataLabel}>Height:</span>
                <span style={styles.dataValue}>{patientData.demographics.height_cm} cm</span>
              </div>
            </div>
            
            <h4 style={styles.subsectionTitle}>Growth Percentiles</h4>
            <div style={styles.dataGrid}>
              <div style={styles.dataItem}>
                <span style={styles.dataLabel}>Height Percentile:</span>
                <span style={styles.dataValue}>{patientData.growth_data.height_percentile}th percentile</span>
              </div>
              <div style={styles.dataItem}>
                <span style={styles.dataLabel}>Weight Percentile:</span>
                <span style={styles.dataValue}>{patientData.growth_data.weight_percentile}th percentile</span>
              </div>
              <div style={styles.dataItem}>
                <span style={styles.dataLabel}>BMI Percentile:</span>
                <span style={styles.dataValue}>{patientData.growth_data.bmi_percentile}th percentile</span>
              </div>
            </div>
          </div>
        )
      
      case 'cardiac':
        return (
          <div style={styles.sectionContent}>
            <h3 style={styles.sectionTitle}>Cardiac Profile</h3>
            <div style={styles.dataGrid}>
              <div style={styles.dataItem}>
                <span style={styles.dataLabel}>Primary Diagnosis:</span>
                <span style={styles.dataValue}>{patientData.cardiac_profile.primary_diagnosis}</span>
              </div>
              <div style={styles.dataItem}>
                <span style={styles.dataLabel}>Severity:</span>
                <span style={styles.dataValue}>{patientData.cardiac_profile.severity}</span>
              </div>
            </div>
            
            <h4 style={styles.subsectionTitle}>Echocardiogram Findings</h4>
            <div style={styles.dataGrid}>
              <div style={styles.dataItem}>
                <span style={styles.dataLabel}>Ejection Fraction:</span>
                <span style={styles.dataValue}>{patientData.cardiac_profile.echo_findings.ejection_fraction}%</span>
              </div>
              <div style={styles.dataItem}>
                <span style={styles.dataLabel}>LV Function:</span>
                <span style={styles.dataValue}>{patientData.cardiac_profile.echo_findings.left_ventricular_function}</span>
              </div>
              <div style={styles.dataItem}>
                <span style={styles.dataLabel}>Valve Function:</span>
                <span style={styles.dataValue}>{patientData.cardiac_profile.echo_findings.valve_function}</span>
              </div>
              <div style={styles.dataItem}>
                <span style={styles.dataLabel}>Wall Motion:</span>
                <span style={styles.dataValue}>{patientData.cardiac_profile.echo_findings.wall_motion}</span>
              </div>
            </div>
            
            <h4 style={styles.subsectionTitle}>Surgical History</h4>
            {patientData.cardiac_profile.surgical_history.map((surgery, index) => (
              <div key={index} style={styles.surgeryCard}>
                <div style={styles.dataItem}>
                  <span style={styles.dataLabel}>Procedure:</span>
                  <span style={styles.dataValue}>{surgery.procedure}</span>
                </div>
                <div style={styles.dataItem}>
                  <span style={styles.dataLabel}>Date:</span>
                  <span style={styles.dataValue}>{surgery.date}</span>
                </div>
                <div style={styles.dataItem}>
                  <span style={styles.dataLabel}>Surgeon:</span>
                  <span style={styles.dataValue}>{surgery.surgeon}</span>
                </div>
                <div style={styles.dataItem}>
                  <span style={styles.dataLabel}>Outcome:</span>
                  <span style={styles.dataValue}>{surgery.outcome}</span>
                </div>
              </div>
            ))}
          </div>
        )
      
      case 'labs':
        return (
          <div style={styles.sectionContent}>
            <h3 style={styles.sectionTitle}>Laboratory Results</h3>
            {patientData.laboratory_results.map((lab, index) => (
              <div key={index} style={styles.labCard}>
                <div style={styles.labHeader}>
                  <h4 style={styles.labTitle}>{lab.test_name}</h4>
                  <div style={styles.labMeta}>
                    <span>LOINC: {lab.loinc_code}</span>
                    <span>Date: {lab.date_collected}</span>
                  </div>
                </div>
                <div style={styles.labResults}>
                  {Object.entries(lab.results).map(([key, value]) => (
                    <div key={key} style={styles.labResult}>
                      <span style={styles.dataLabel}>{key.replace(/_/g, ' ').toUpperCase()}:</span>
                      <span style={styles.dataValue}>{value}</span>
                      <span style={styles.referenceRange}>
                        (Ref: {lab.reference_ranges[key]})
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )
      
      case 'medications':
        return (
          <div style={styles.sectionContent}>
            <h3 style={styles.sectionTitle}>Current Medications</h3>
            {patientData.medications.map((med, index) => (
              <div key={index} style={styles.medicationCard}>
                <div style={styles.medHeader}>
                  <h4 style={styles.medName}>{med.name}</h4>
                  <span style={styles.rxnormCode}>RxNorm: {med.rxnorm_code}</span>
                </div>
                <div style={styles.medDetails}>
                  <div style={styles.dataItem}>
                    <span style={styles.dataLabel}>Dosage:</span>
                    <span style={styles.dataValue}>{med.dosage}</span>
                  </div>
                  <div style={styles.dataItem}>
                    <span style={styles.dataLabel}>Route:</span>
                    <span style={styles.dataValue}>{med.route}</span>
                  </div>
                  <div style={styles.dataItem}>
                    <span style={styles.dataLabel}>Frequency:</span>
                    <span style={styles.dataValue}>{med.frequency}</span>
                  </div>
                  <div style={styles.dataItem}>
                    <span style={styles.dataLabel}>Start Date:</span>
                    <span style={styles.dataValue}>{med.start_date}</span>
                  </div>
                  <div style={styles.dataItem}>
                    <span style={styles.dataLabel}>Indication:</span>
                    <span style={styles.dataValue}>{med.indication}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )
      
      case 'encounters':
        return (
          <div style={styles.sectionContent}>
            <h3 style={styles.sectionTitle}>Clinical Encounters</h3>
            {patientData.clinical_encounters.map((encounter, index) => (
              <div key={index} style={styles.encounterCard}>
                <div style={styles.encounterHeader}>
                  <h4 style={styles.encounterType}>{encounter.type}</h4>
                  <span style={styles.encounterDate}>{encounter.date}</span>
                </div>
                <div style={styles.encounterDetails}>
                  <div style={styles.dataItem}>
                    <span style={styles.dataLabel}>Provider:</span>
                    <span style={styles.dataValue}>{encounter.provider}</span>
                  </div>
                  <div style={styles.dataItem}>
                    <span style={styles.dataLabel}>Chief Complaint:</span>
                    <span style={styles.dataValue}>{encounter.chief_complaint}</span>
                  </div>
                  <div style={styles.dataItem}>
                    <span style={styles.dataLabel}>Assessment:</span>
                    <span style={styles.dataValue}>{encounter.assessment}</span>
                  </div>
                  <div style={styles.dataItem}>
                    <span style={styles.dataLabel}>Plan:</span>
                    <span style={styles.dataValue}>{encounter.plan}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )
      
      case 'vitals':
        return (
          <div style={styles.sectionContent}>
            <h3 style={styles.sectionTitle}>Vital Signs</h3>
            {patientData.vital_signs.recent_measurements.map((vitals, index) => (
              <div key={index} style={styles.vitalsCard}>
                <h4 style={styles.vitalsDate}>Recorded: {vitals.date}</h4>
                <div style={styles.vitalsGrid}>
                  <div style={styles.vitalSign}>
                    <span style={styles.vitalLabel}>Heart Rate</span>
                    <span style={styles.vitalValue}>{vitals.heart_rate} bpm</span>
                  </div>
                  <div style={styles.vitalSign}>
                    <span style={styles.vitalLabel}>Blood Pressure</span>
                    <span style={styles.vitalValue}>{vitals.blood_pressure_systolic}/{vitals.blood_pressure_diastolic} mmHg</span>
                  </div>
                  <div style={styles.vitalSign}>
                    <span style={styles.vitalLabel}>Oxygen Saturation</span>
                    <span style={styles.vitalValue}>{vitals.oxygen_saturation}%</span>
                  </div>
                  <div style={styles.vitalSign}>
                    <span style={styles.vitalLabel}>Temperature</span>
                    <span style={styles.vitalValue}>{vitals.temperature_f}°F</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )
      
      default:
        return null
    }
  }

  const sections = [
    { id: 'demographics', label: 'Demographics', icon: User },
    { id: 'cardiac', label: 'Cardiac Profile', icon: Heart },
    { id: 'labs', label: 'Laboratory Results', icon: FlaskConical },
    { id: 'medications', label: 'Medications', icon: Pill },
    { id: 'encounters', label: 'Clinical Encounters', icon: Calendar },
    { id: 'vitals', label: 'Vital Signs', icon: Activity }
  ]

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
      marginBottom: '32px'
    },
    patientTitle: {
      fontSize: '36px',
      fontWeight: '700',
      color: '#1f2937',
      marginBottom: '32px',
      textAlign: 'center' as const
    },
    contentArea: {
      display: 'flex',
      gap: '32px'
    },
    sidebar: {
      width: '280px',
      flexShrink: 0
    },
    sectionNav: {
      backgroundColor: '#ffffff',
      borderRadius: '12px',
      padding: '24px',
      boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
    },
    sectionNavTitle: {
      fontSize: '18px',
      fontWeight: '600',
      color: '#1f2937',
      marginBottom: '16px'
    },
    sectionButton: {
      width: '100%',
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
      padding: '12px 16px',
      marginBottom: '8px',
      backgroundColor: 'transparent',
      border: 'none',
      borderRadius: '8px',
      fontSize: '14px',
      fontWeight: '500',
      cursor: 'pointer',
      textAlign: 'left' as const,
      transition: 'all 0.2s'
    },
    sectionButtonActive: {
      backgroundColor: '#eff6ff',
      color: '#2563eb'
    },
    sectionButtonInactive: {
      color: '#6b7280'
    },
    mainContent: {
      flex: 1,
      backgroundColor: '#ffffff',
      borderRadius: '12px',
      padding: '32px',
      boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
    },
    sectionContent: {
      width: '100%'
    },
    sectionTitle: {
      fontSize: '24px',
      fontWeight: '600',
      color: '#1f2937',
      marginBottom: '24px'
    },
    subsectionTitle: {
      fontSize: '18px',
      fontWeight: '600',
      color: '#374151',
      marginTop: '32px',
      marginBottom: '16px'
    },
    dataGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
      gap: '16px',
      marginBottom: '24px'
    },
    dataItem: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: '12px',
      backgroundColor: '#f8fafc',
      borderRadius: '8px'
    },
    dataLabel: {
      fontSize: '14px',
      fontWeight: '500',
      color: '#6b7280'
    },
    dataValue: {
      fontSize: '14px',
      fontWeight: '600',
      color: '#1f2937'
    },
    surgeryCard: {
      backgroundColor: '#f8fafc',
      borderRadius: '8px',
      padding: '16px',
      marginBottom: '16px'
    },
    labCard: {
      backgroundColor: '#f8fafc',
      borderRadius: '12px',
      padding: '20px',
      marginBottom: '20px'
    },
    labHeader: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: '16px'
    },
    labTitle: {
      fontSize: '16px',
      fontWeight: '600',
      color: '#1f2937',
      margin: '0'
    },
    labMeta: {
      display: 'flex',
      gap: '16px',
      fontSize: '12px',
      color: '#6b7280'
    },
    labResults: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
      gap: '12px'
    },
    labResult: {
      display: 'flex',
      flexDirection: 'column' as const,
      gap: '4px'
    },
    referenceRange: {
      fontSize: '12px',
      color: '#6b7280',
      fontStyle: 'italic'
    },
    medicationCard: {
      backgroundColor: '#f8fafc',
      borderRadius: '12px',
      padding: '20px',
      marginBottom: '20px'
    },
    medHeader: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: '16px'
    },
    medName: {
      fontSize: '16px',
      fontWeight: '600',
      color: '#1f2937',
      margin: '0'
    },
    rxnormCode: {
      fontSize: '12px',
      color: '#6b7280',
      backgroundColor: '#e5e7eb',
      padding: '4px 8px',
      borderRadius: '4px'
    },
    medDetails: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
      gap: '12px'
    },
    encounterCard: {
      backgroundColor: '#f8fafc',
      borderRadius: '12px',
      padding: '20px',
      marginBottom: '20px'
    },
    encounterHeader: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: '16px'
    },
    encounterType: {
      fontSize: '16px',
      fontWeight: '600',
      color: '#1f2937',
      margin: '0'
    },
    encounterDate: {
      fontSize: '14px',
      color: '#6b7280'
    },
    encounterDetails: {
      display: 'flex',
      flexDirection: 'column' as const,
      gap: '12px'
    },
    vitalsCard: {
      backgroundColor: '#f8fafc',
      borderRadius: '12px',
      padding: '20px',
      marginBottom: '20px'
    },
    vitalsDate: {
      fontSize: '16px',
      fontWeight: '600',
      color: '#1f2937',
      margin: '0 0 16px 0'
    },
    vitalsGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
      gap: '16px'
    },
    vitalSign: {
      display: 'flex',
      flexDirection: 'column' as const,
      alignItems: 'center',
      padding: '16px',
      backgroundColor: '#ffffff',
      borderRadius: '8px',
      boxShadow: '0 1px 2px rgba(0,0,0,0.05)'
    },
    vitalLabel: {
      fontSize: '12px',
      fontWeight: '500',
      color: '#6b7280',
      marginBottom: '8px'
    },
    vitalValue: {
      fontSize: '18px',
      fontWeight: '700',
      color: '#1f2937'
    },
    blankMessage: {
      textAlign: 'center' as const,
      fontSize: '18px',
      color: '#6b7280',
      marginTop: '64px'
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
        <button style={styles.backButton} onClick={handleBackClick}>
          <ArrowLeft size={16} />
          Back to Results
        </button>

        <h1 style={styles.patientTitle}>
          Patient Record: {patientId || 'Unknown Patient'}
        </h1>

        <div style={styles.contentArea}>
          <div style={styles.sidebar}>
            <div style={styles.sectionNav}>
              <h3 style={styles.sectionNavTitle}>Medical Record Sections</h3>
              {sections.map((section) => {
                const IconComponent = section.icon
                const isActive = activeSection === section.id
                return (
                  <button
                    key={section.id}
                    onClick={() => setActiveSection(section.id)}
                    style={{
                      ...styles.sectionButton,
                      ...(isActive ? styles.sectionButtonActive : styles.sectionButtonInactive)
                    }}
                  >
                    <IconComponent size={16} />
                    {section.label}
                  </button>
                )
              })}
            </div>
          </div>

          <div style={styles.mainContent}>
            {renderSectionContent()}
          </div>
        </div>
      </main>
    </div>
  )
}

export default PatientRecord