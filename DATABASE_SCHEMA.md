# 🗄️ Medical Documents Database Schema

## Overview

This database schema stores parsed data from medical documents processed by the API. It supports four types of medical documents with proper normalization and relationships.

---

## 📊 Database Structure

### Entity Relationship Diagram

```
┌─────────────────┐
│   documents     │ (Main table - stores all document metadata)
│─────────────────│
│ id (PK)         │
│ document_type   │
│ confidence      │
│ processed_at    │
│ ...             │
└────────┬────────┘
         │
         ├─────────────────────────────────────┐
         │                                      │
         │                                      │
    ┌────▼──────────┐                  ┌───────▼────────┐
    │ prescriptions │                  │  lab_reports   │
    │───────────────│                  │────────────────│
    │ id (PK)       │                  │ id (PK)        │
    │ document_id   │◄─1:1             │ document_id    │◄─1:1
    │ patient_name  │                  │ patient_name   │
    │ doctor_name   │                  │ lab_name       │
    │ ...           │                  │ ...            │
    └───────┬───────┘                  └────────┬───────┘
            │                                   │
            │ 1:N                               │ 1:N
            │                                   │
    ┌───────▼───────────────┐         ┌────────▼───────────┐
    │ prescription_medications│       │   test_results     │
    │───────────────────────│         │────────────────────│
    │ id (PK)               │         │ id (PK)            │
    │ prescription_id (FK)  │         │ lab_report_id (FK) │
    │ name                  │         │ test_name          │
    │ dosage                │         │ result_value       │
    │ ...                   │         │ status             │
    └───────────────────────┘         └────────────────────┘

         │                                      │
         │                                      │
    ┌────▼──────────┐                  ┌───────▼──────────────┐
    │ doctor_visits │                  │ diagnostic_results   │
    │───────────────│                  │──────────────────────│
    │ id (PK)       │                  │ id (PK)              │
    │ document_id   │◄─1:1             │ document_id          │◄─1:1
    │ patient_name  │                  │ patient_name         │
    │ clinic_name   │                  │ facility_name        │
    │ ...           │                  │ diagnostic_type      │
    └───────┬───────┘                  │ ...                  │
            │                          └──────────────────────┘
            │ 1:N
            │
    ┌───────▼─────────────┐
    │ visit_medications   │
    │─────────────────────│
    │ id (PK)             │
    │ doctor_visit_id (FK)│
    │ name                │
    │ dosage              │
    │ ...                 │
    └─────────────────────┘
```

---

## 📋 Table Descriptions

### 1. **documents** (Main Table)

**Purpose**: Central table storing metadata for all processed documents

**Key Fields**:
- `id` - Primary key
- `document_type` - Type: prescription, lab_report, doctor_visit, diagnostic_results, unknown
- `confidence` - Classification confidence (0.0 to 1.0)
- `processed_at` - When the document was processed
- `original_filename` - Original uploaded file name
- `image_path` - Optional path to stored image

**Relationships**: One-to-One with each specific document type table

---

### 2. **prescriptions**

**Purpose**: Stores prescription data

**Key Fields**:
- Patient info: `patient_name`, `patient_age`, `patient_contact`
- Doctor info: `doctor_name`, `doctor_specialty`, `doctor_contact`
- Dates: `prescription_date`, `validity_date`
- Medical: `diagnosis`, `notes`

**Relationships**: 
- One-to-One with `documents`
- One-to-Many with `prescription_medications`

---

### 3. **prescription_medications**

**Purpose**: Stores individual medications for prescriptions

**Key Fields**:
- `prescription_id` - Foreign key to prescriptions
- `name`, `dosage`, `frequency`, `duration`
- `instructions` - Additional instructions
- `position` - Order in the prescription

**Why separate table?**: A prescription can have multiple medications (1:N relationship)

---

### 4. **lab_reports**

**Purpose**: Stores laboratory test report data

**Key Fields**:
- Patient info: `patient_name`, `patient_age`, `patient_id`
- Lab info: `lab_name`, `lab_location`, `lab_contact`
- Dates: `report_date`, `collection_date`
- `doctor_name` - Referring physician

**Relationships**:
- One-to-One with `documents`
- One-to-Many with `test_results`

---

### 5. **test_results**

**Purpose**: Stores individual test results from lab reports

**Key Fields**:
- `lab_report_id` - Foreign key to lab_reports
- `test_name` - Name of the test (e.g., "Hemoglobin")
- `result_value` - The measured value
- `unit` - Unit of measurement (e.g., "g/dL")
- `reference_range` - Normal range
- `status` - normal, abnormal, or critical
- `position` - Order in the report

**Why separate table?**: A lab report can have many test results (1:N relationship)

---

### 6. **doctor_visits**

**Purpose**: Stores doctor's visit summary data

**Key Fields**:
- Patient info: `patient_name`, `patient_age`, `patient_contact`
- Clinic info: `clinic_name`, `clinic_location`, `clinic_contact`
- Doctor info: `doctor_name`, `doctor_specialty`
- Medical: `diagnosis`, `procedures[]`, `recommendations[]`
- `visit_date`, `follow_up`, `notes`

**Note**: Uses PostgreSQL arrays for `procedures` and `recommendations`

**Relationships**:
- One-to-One with `documents`
- One-to-Many with `visit_medications`

---

### 7. **visit_medications**

**Purpose**: Stores medications prescribed during doctor visits

**Key Fields**:
- `doctor_visit_id` - Foreign key to doctor_visits
- `name`, `dosage`, `frequency`, `duration`
- `position` - Order in the visit

**Why separate table?**: A visit can prescribe multiple medications (1:N relationship)

---

### 8. **diagnostic_results**

**Purpose**: Stores diagnostic imaging results (X-ray, MRI, CT, Ultrasound)

**Key Fields**:
- Patient info: `patient_name`, `patient_age`, `patient_id`
- Study info: `diagnostic_type`, `study_date`
- Facility info: `facility_name`, `facility_location`, `facility_contact`
- Staff: `referring_physician`, `radiologist_name`
- Results: `body_part_examined`, `findings_summary`, `impression`, `recommendations`

**Relationships**: One-to-One with `documents`

---

## 🔍 Views

### v_all_documents

Unified view of all documents with basic patient info

```sql
SELECT * FROM v_all_documents 
WHERE patient_name = 'John Doe';
```

### v_prescription_details

Prescriptions with their medications

```sql
SELECT * FROM v_prescription_details 
WHERE patient_name = 'John Doe';
```

### v_lab_report_details

Lab reports with their test results

```sql
SELECT * FROM v_lab_report_details 
WHERE status = 'abnormal';
```

---

## 🎯 Design Decisions

### 1. **Normalization**

**Why separate tables for medications and test results?**
- Avoids storing arrays of JSON in single cells
- Easier to query individual items
- Better indexing and performance
- Follows database normalization principles

### 2. **documents as Central Table**

**Why not store everything in one table?**
- Different document types have different fields
- Prevents sparse columns (many NULLs)
- Easier to add new document types
- Maintains data integrity

### 3. **Audit Fields**

All main tables include:
- `created_at` - When record was created
- `updated_at` - When record was last modified (auto-updated via triggers)

### 4. **Constraints**

- CHECK constraints for valid values (e.g., document_type, status)
- CHECK constraints for logical consistency (e.g., validity_date >= prescription_date)
- Foreign key constraints with CASCADE delete

### 5. **Indexes**

Strategic indexes on:
- Common search fields (patient_name, doctor_name)
- Date fields (for date range queries)
- Foreign keys (for JOIN performance)
- Document types (for filtering)

---

## 📖 Usage Examples

### Insert a Complete Prescription

```sql
BEGIN;

-- 1. Insert document metadata
INSERT INTO documents (document_type, confidence, original_filename, processing_time_ms)
VALUES ('prescription', 0.95, 'prescription_001.jpg', 2500)
RETURNING id; -- Let's say this returns id=1

-- 2. Insert prescription
INSERT INTO prescriptions (
    document_id, patient_name, patient_age, doctor_name, 
    prescription_date, diagnosis
)
VALUES (
    1, 'Иван Петров', 45, 'Др. Анна Смирнова', 
    '2025-10-18', 'Бактериальная инфекция'
);
-- Returns id=1

-- 3. Insert medications
INSERT INTO prescription_medications (
    prescription_id, name, dosage, frequency, duration, position
)
VALUES 
    (1, 'Амоксициллин', '500мг', '3 раза в день', '7 дней', 1),
    (1, 'Парацетамол', '500мг', 'по необходимости', '5 дней', 2);

COMMIT;
```

### Insert a Lab Report with Results

```sql
BEGIN;

-- 1. Insert document
INSERT INTO documents (document_type, confidence, original_filename)
VALUES ('lab_report', 0.98, 'lab_report_001.jpg')
RETURNING id; -- Returns id=2

-- 2. Insert lab report
INSERT INTO lab_reports (
    document_id, patient_name, patient_age, report_date,
    lab_name, lab_location
)
VALUES (
    2, 'Мария Иванова', 35, '2025-10-18',
    'Городская диагностическая лаборатория', 'ул. Ленина 123'
)
RETURNING id; -- Returns id=1

-- 3. Insert test results
INSERT INTO test_results (
    lab_report_id, test_name, result_value, unit, 
    reference_range, status, position
)
VALUES 
    (1, 'Гемоглобин', '145', 'г/л', '120-160', 'normal', 1),
    (1, 'Лейкоциты', '12.5', '10^9/л', '4.0-9.0', 'abnormal', 2),
    (1, 'Глюкоза', '5.2', 'ммоль/л', '3.9-5.8', 'normal', 3);

COMMIT;
```

### Query Examples

```sql
-- Find all abnormal lab results for a patient
SELECT 
    lr.patient_name,
    lr.report_date,
    tr.test_name,
    tr.result_value,
    tr.unit,
    tr.reference_range
FROM lab_reports lr
JOIN test_results tr ON lr.id = tr.lab_report_id
WHERE lr.patient_name = 'Мария Иванова'
  AND tr.status = 'abnormal'
ORDER BY lr.report_date DESC;

-- Get all prescriptions with medications for a date range
SELECT 
    p.patient_name,
    p.prescription_date,
    p.doctor_name,
    pm.name as medication,
    pm.dosage,
    pm.frequency
FROM prescriptions p
LEFT JOIN prescription_medications pm ON p.id = pm.prescription_id
WHERE p.prescription_date BETWEEN '2025-01-01' AND '2025-12-31'
ORDER BY p.prescription_date DESC, pm.position;

-- Count documents by type
SELECT 
    document_type,
    COUNT(*) as total,
    AVG(confidence) as avg_confidence
FROM documents
WHERE processed_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY document_type
ORDER BY total DESC;
```

---

## 🚀 Setting Up the Database

### Using PostgreSQL

```bash
# Create database
createdb medical_documents

# Run schema
psql medical_documents < database_schema.sql

# Verify tables
psql medical_documents -c "\dt"
```

### Using Docker

```bash
# Start PostgreSQL
docker run --name medical-db \
  -e POSTGRES_DB=medical_documents \
  -e POSTGRES_PASSWORD=yourpassword \
  -p 5432:5432 \
  -d postgres:15

# Apply schema
docker exec -i medical-db psql -U postgres medical_documents < database_schema.sql
```

---

## 🔧 Extending the Schema

### Adding a New Document Type

1. **Add to documents table** CHECK constraint
2. **Create new type-specific table** with document_id foreign key
3. **Create child tables** for arrays (if needed)
4. **Add to views** for unified querying
5. **Update triggers** if needed

Example:
```sql
-- Add "insurance_card" as new type
ALTER TABLE documents 
DROP CONSTRAINT documents_document_type_check;

ALTER TABLE documents
ADD CONSTRAINT documents_document_type_check
CHECK (document_type IN (
    'prescription', 'lab_report', 'doctor_visit', 
    'diagnostic_results', 'insurance_card', 'unknown'
));

-- Create insurance_cards table
CREATE TABLE insurance_cards (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL UNIQUE REFERENCES documents(id),
    -- add fields...
);
```

---

## 📊 Performance Considerations

1. **Indexes**: Already optimized for common queries
2. **Partitioning**: Consider partitioning `documents` by date for large datasets
3. **Archiving**: Old documents can be moved to archive tables
4. **Caching**: Use Redis for frequently accessed patient data
5. **Full-text search**: Add `tsvector` columns for searching notes/findings

---

## 🔐 Security Considerations

1. **Sensitive Data**: Consider encryption for patient names and IDs
2. **Access Control**: Implement row-level security (RLS) in PostgreSQL
3. **Audit Log**: Track all INSERT/UPDATE/DELETE operations
4. **Backup**: Regular backups of sensitive medical data
5. **HIPAA Compliance**: Ensure compliance if storing real patient data

---

This schema provides a robust foundation for storing medical document data with proper normalization, relationships, and indexing! 🎉

