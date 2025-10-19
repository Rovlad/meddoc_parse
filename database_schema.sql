-- ============================================================================
-- Medical Documents Database Schema
-- ============================================================================
-- This schema stores parsed data from medical documents including:
-- - Prescriptions
-- - Lab Reports
-- - Doctor's Visit Summaries
-- - Diagnostic Results
-- ============================================================================

-- Drop existing tables (in correct order due to foreign keys)
DROP TABLE IF EXISTS diagnostic_results CASCADE;
DROP TABLE IF EXISTS visit_medications CASCADE;
DROP TABLE IF EXISTS doctor_visits CASCADE;
DROP TABLE IF EXISTS test_results CASCADE;
DROP TABLE IF EXISTS lab_reports CASCADE;
DROP TABLE IF EXISTS prescription_medications CASCADE;
DROP TABLE IF EXISTS prescriptions CASCADE;
DROP TABLE IF EXISTS documents CASCADE;

-- ============================================================================
-- Main Documents Table
-- ============================================================================
-- Stores common information about all processed documents
CREATE TABLE documents (
    -- Primary Key
    id SERIAL PRIMARY KEY,
    
    -- Document Metadata
    document_type VARCHAR(50) NOT NULL CHECK (document_type IN (
        'prescription', 
        'lab_report', 
        'doctor_visit', 
        'diagnostic_results', 
        'unknown'
    )),
    confidence DECIMAL(3,2) CHECK (confidence >= 0 AND confidence <= 1),
    
    -- File Information
    original_filename VARCHAR(255),
    file_size_bytes INTEGER,
    mime_type VARCHAR(100),
    
    -- Processing Information
    processed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    processing_time_ms INTEGER,
    
    -- Optional: Store original image reference
    image_path TEXT,
    
    -- Optional: Raw OCR text if needed
    raw_text TEXT,
    
    -- Audit fields
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    CONSTRAINT valid_confidence CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 1))
);

CREATE INDEX idx_documents_type ON documents(document_type);
CREATE INDEX idx_documents_processed_at ON documents(processed_at);
CREATE INDEX idx_documents_created_at ON documents(created_at);


-- ============================================================================
-- PRESCRIPTIONS
-- ============================================================================

CREATE TABLE prescriptions (
    -- Primary Key
    id SERIAL PRIMARY KEY,
    
    -- Foreign Key to documents
    document_id INTEGER NOT NULL UNIQUE REFERENCES documents(id) ON DELETE CASCADE,
    
    -- Patient Information
    patient_name VARCHAR(255) NOT NULL,
    patient_age INTEGER CHECK (patient_age > 0 AND patient_age < 150),
    patient_contact VARCHAR(255),
    
    -- Doctor Information
    doctor_name VARCHAR(255) NOT NULL,
    doctor_specialty VARCHAR(255),
    doctor_contact VARCHAR(255),
    
    -- Dates
    prescription_date DATE NOT NULL,
    validity_date DATE,
    
    -- Medical Information
    diagnosis TEXT,
    notes TEXT,
    
    -- Audit fields
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_prescription_dates CHECK (
        validity_date IS NULL OR validity_date >= prescription_date
    )
);

CREATE INDEX idx_prescriptions_patient_name ON prescriptions(patient_name);
CREATE INDEX idx_prescriptions_doctor_name ON prescriptions(doctor_name);
CREATE INDEX idx_prescriptions_date ON prescriptions(prescription_date);

-- Medications for prescriptions (one-to-many relationship)
CREATE TABLE prescription_medications (
    -- Primary Key
    id SERIAL PRIMARY KEY,
    
    -- Foreign Key
    prescription_id INTEGER NOT NULL REFERENCES prescriptions(id) ON DELETE CASCADE,
    
    -- Medication Details
    name VARCHAR(255) NOT NULL,
    dosage VARCHAR(100) NOT NULL,
    frequency VARCHAR(100) NOT NULL,
    duration VARCHAR(100) NOT NULL,
    instructions TEXT,
    
    -- Order in the prescription
    position INTEGER NOT NULL DEFAULT 1,
    
    -- Audit fields
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_prescription_medications_prescription_id ON prescription_medications(prescription_id);
CREATE INDEX idx_prescription_medications_name ON prescription_medications(name);


-- ============================================================================
-- LAB REPORTS
-- ============================================================================

CREATE TABLE lab_reports (
    -- Primary Key
    id SERIAL PRIMARY KEY,
    
    -- Foreign Key to documents
    document_id INTEGER NOT NULL UNIQUE REFERENCES documents(id) ON DELETE CASCADE,
    
    -- Patient Information
    patient_name VARCHAR(255) NOT NULL,
    patient_age INTEGER CHECK (patient_age > 0 AND patient_age < 150),
    patient_id VARCHAR(100),
    
    -- Dates
    report_date DATE NOT NULL,
    collection_date DATE,
    
    -- Lab Information
    lab_name VARCHAR(255) NOT NULL,
    lab_location TEXT,
    lab_contact VARCHAR(255),
    
    -- Doctor Information
    doctor_name VARCHAR(255),
    
    -- Additional Information
    notes TEXT,
    
    -- Audit fields
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_lab_dates CHECK (
        collection_date IS NULL OR collection_date <= report_date
    )
);

CREATE INDEX idx_lab_reports_patient_name ON lab_reports(patient_name);
CREATE INDEX idx_lab_reports_patient_id ON lab_reports(patient_id);
CREATE INDEX idx_lab_reports_report_date ON lab_reports(report_date);
CREATE INDEX idx_lab_reports_lab_name ON lab_reports(lab_name);

-- Test results (one-to-many relationship)
CREATE TABLE test_results (
    -- Primary Key
    id SERIAL PRIMARY KEY,
    
    -- Foreign Key
    lab_report_id INTEGER NOT NULL REFERENCES lab_reports(id) ON DELETE CASCADE,
    
    -- Test Details
    test_name VARCHAR(255) NOT NULL,
    result_value VARCHAR(100) NOT NULL,
    unit VARCHAR(50),
    reference_range VARCHAR(100),
    status VARCHAR(20) CHECK (status IN ('normal', 'abnormal', 'critical', NULL)),
    
    -- Order in the report
    position INTEGER NOT NULL DEFAULT 1,
    
    -- Audit fields
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_test_results_lab_report_id ON test_results(lab_report_id);
CREATE INDEX idx_test_results_test_name ON test_results(test_name);
CREATE INDEX idx_test_results_status ON test_results(status);


-- ============================================================================
-- DOCTOR'S VISITS
-- ============================================================================

CREATE TABLE doctor_visits (
    -- Primary Key
    id SERIAL PRIMARY KEY,
    
    -- Foreign Key to documents
    document_id INTEGER NOT NULL UNIQUE REFERENCES documents(id) ON DELETE CASCADE,
    
    -- Patient Information
    patient_name VARCHAR(255) NOT NULL,
    patient_age INTEGER CHECK (patient_age > 0 AND patient_age < 150),
    patient_contact VARCHAR(255),
    
    -- Visit Information
    visit_date DATE NOT NULL,
    
    -- Clinic Information
    clinic_name VARCHAR(255),
    clinic_location TEXT,
    clinic_contact VARCHAR(255),
    
    -- Doctor Information
    doctor_name VARCHAR(255) NOT NULL,
    doctor_specialty VARCHAR(255),
    
    -- Medical Information
    diagnosis TEXT NOT NULL,
    procedures TEXT[], -- Array of procedures
    recommendations TEXT[], -- Array of recommendations
    
    -- Follow-up
    follow_up TEXT,
    notes TEXT,
    
    -- Audit fields
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_doctor_visits_patient_name ON doctor_visits(patient_name);
CREATE INDEX idx_doctor_visits_doctor_name ON doctor_visits(doctor_name);
CREATE INDEX idx_doctor_visits_date ON doctor_visits(visit_date);
CREATE INDEX idx_doctor_visits_clinic_name ON doctor_visits(clinic_name);

-- Medications prescribed during visit (one-to-many relationship)
CREATE TABLE visit_medications (
    -- Primary Key
    id SERIAL PRIMARY KEY,
    
    -- Foreign Key
    doctor_visit_id INTEGER NOT NULL REFERENCES doctor_visits(id) ON DELETE CASCADE,
    
    -- Medication Details
    name VARCHAR(255) NOT NULL,
    dosage VARCHAR(100) NOT NULL,
    frequency VARCHAR(100) NOT NULL,
    duration VARCHAR(100) NOT NULL,
    
    -- Order in the visit
    position INTEGER NOT NULL DEFAULT 1,
    
    -- Audit fields
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_visit_medications_visit_id ON visit_medications(doctor_visit_id);
CREATE INDEX idx_visit_medications_name ON visit_medications(name);


-- ============================================================================
-- DIAGNOSTIC RESULTS
-- ============================================================================

CREATE TABLE diagnostic_results (
    -- Primary Key
    id SERIAL PRIMARY KEY,
    
    -- Foreign Key to documents
    document_id INTEGER NOT NULL UNIQUE REFERENCES documents(id) ON DELETE CASCADE,
    
    -- Patient Information
    patient_name VARCHAR(255) NOT NULL,
    patient_age INTEGER CHECK (patient_age > 0 AND patient_age < 150),
    patient_id VARCHAR(100),
    
    -- Study Information
    diagnostic_type VARCHAR(50) NOT NULL CHECK (diagnostic_type IN (
        'ultrasound', 'x-ray', 'mri', 'ct'
    )),
    study_date DATE NOT NULL,
    
    -- Facility Information
    facility_name VARCHAR(255) NOT NULL,
    facility_location TEXT,
    facility_contact VARCHAR(255),
    
    -- Medical Staff
    referring_physician VARCHAR(255),
    radiologist_name VARCHAR(255),
    
    -- Results
    body_part_examined VARCHAR(255),
    findings_summary TEXT NOT NULL,
    impression TEXT,
    recommendations TEXT,
    
    -- Additional Information
    notes TEXT,
    
    -- Audit fields
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_diagnostic_results_patient_name ON diagnostic_results(patient_name);
CREATE INDEX idx_diagnostic_results_patient_id ON diagnostic_results(patient_id);
CREATE INDEX idx_diagnostic_results_study_date ON diagnostic_results(study_date);
CREATE INDEX idx_diagnostic_results_diagnostic_type ON diagnostic_results(diagnostic_type);
CREATE INDEX idx_diagnostic_results_facility_name ON diagnostic_results(facility_name);


-- ============================================================================
-- VIEWS FOR EASY QUERYING
-- ============================================================================

-- View: All documents with their specific data
CREATE VIEW v_all_documents AS
SELECT 
    d.id,
    d.document_type,
    d.confidence,
    d.processed_at,
    d.original_filename,
    CASE 
        WHEN d.document_type = 'prescription' THEN p.patient_name
        WHEN d.document_type = 'lab_report' THEN lr.patient_name
        WHEN d.document_type = 'doctor_visit' THEN dv.patient_name
        WHEN d.document_type = 'diagnostic_results' THEN dr.patient_name
    END as patient_name,
    CASE 
        WHEN d.document_type = 'prescription' THEN p.prescription_date::TEXT
        WHEN d.document_type = 'lab_report' THEN lr.report_date::TEXT
        WHEN d.document_type = 'doctor_visit' THEN dv.visit_date::TEXT
        WHEN d.document_type = 'diagnostic_results' THEN dr.study_date::TEXT
    END as document_date
FROM documents d
LEFT JOIN prescriptions p ON d.id = p.document_id
LEFT JOIN lab_reports lr ON d.id = lr.document_id
LEFT JOIN doctor_visits dv ON d.id = dv.document_id
LEFT JOIN diagnostic_results dr ON d.id = dr.document_id;

-- View: Prescription details with medications
CREATE VIEW v_prescription_details AS
SELECT 
    p.id as prescription_id,
    p.patient_name,
    p.patient_age,
    p.doctor_name,
    p.prescription_date,
    pm.name as medication_name,
    pm.dosage,
    pm.frequency,
    pm.duration,
    pm.instructions,
    d.processed_at,
    d.confidence
FROM prescriptions p
JOIN documents d ON p.document_id = d.id
LEFT JOIN prescription_medications pm ON p.id = pm.prescription_id
ORDER BY p.prescription_date DESC, pm.position;

-- View: Lab report details with test results
CREATE VIEW v_lab_report_details AS
SELECT 
    lr.id as lab_report_id,
    lr.patient_name,
    lr.patient_age,
    lr.report_date,
    lr.lab_name,
    tr.test_name,
    tr.result_value,
    tr.unit,
    tr.reference_range,
    tr.status,
    d.processed_at,
    d.confidence
FROM lab_reports lr
JOIN documents d ON lr.document_id = d.id
LEFT JOIN test_results tr ON lr.id = tr.lab_report_id
ORDER BY lr.report_date DESC, tr.position;


-- ============================================================================
-- UTILITY FUNCTIONS
-- ============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers to automatically update updated_at
CREATE TRIGGER update_documents_updated_at 
    BEFORE UPDATE ON documents 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_prescriptions_updated_at 
    BEFORE UPDATE ON prescriptions 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_lab_reports_updated_at 
    BEFORE UPDATE ON lab_reports 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_doctor_visits_updated_at 
    BEFORE UPDATE ON doctor_visits 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_diagnostic_results_updated_at 
    BEFORE UPDATE ON diagnostic_results 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


-- ============================================================================
-- SAMPLE QUERIES
-- ============================================================================

-- Get all documents for a specific patient
-- SELECT * FROM v_all_documents WHERE patient_name = 'John Doe';

-- Get all prescriptions for a patient with medications
-- SELECT * FROM v_prescription_details WHERE patient_name = 'John Doe';

-- Get all lab reports with abnormal results
-- SELECT DISTINCT lr.* 
-- FROM lab_reports lr
-- JOIN test_results tr ON lr.id = tr.lab_report_id
-- WHERE tr.status = 'abnormal';

-- Get all documents processed in the last 7 days
-- SELECT * FROM v_all_documents 
-- WHERE processed_at >= CURRENT_DATE - INTERVAL '7 days';

-- Count documents by type
-- SELECT document_type, COUNT(*) 
-- FROM documents 
-- GROUP BY document_type;

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================

