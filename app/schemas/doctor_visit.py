"""Doctor's visit summary document schema"""

from pydantic import BaseModel, Field
from typing import Optional, List


class ClinicInfo(BaseModel):
    """Clinic/Medical facility information"""
    
    clinic_name: str = Field(..., description="Name of the clinic or medical facility")
    clinic_location: Optional[str] = Field(None, description="Clinic address or location")
    clinic_contact: Optional[str] = Field(None, description="Clinic contact number or email")


class VisitMedication(BaseModel):
    """Medication prescribed during visit"""
    
    name: str = Field(..., description="Name of the medication")
    dosage: str = Field(..., description="Dosage amount")
    frequency: str = Field(..., description="How often to take")
    duration: str = Field(..., description="How long to take")


class DoctorVisitSchema(BaseModel):
    """Schema for doctor's visit summary documents"""
    
    # Patient Information
    patient_name: str = Field(..., description="Full name of the patient")
    patient_age: Optional[int] = Field(None, description="Age of the patient")
    patient_contact: Optional[str] = Field(None, description="Patient contact number or email")
    
    # Visit Information
    visit_date: str = Field(..., description="Date of the visit (YYYY-MM-DD format)")
    
    # Clinic Information
    clinic_info: Optional[ClinicInfo] = Field(None, description="Clinic or medical facility information")
    
    # Doctor Information
    doctor_name: str = Field(..., description="Full name of the doctor")
    doctor_specialty: Optional[str] = Field(None, description="Doctor's specialty")
    
    # Medical Information
    diagnosis: str = Field(..., description="Diagnosis or identified condition")
    procedures: Optional[List[str]] = Field(None, description="Procedures performed during visit")
    medications: Optional[List[VisitMedication]] = Field(None, description="Medications prescribed")
    recommendations: Optional[List[str]] = Field(None, description="Doctor's recommendations")
    
    # Follow-up
    follow_up: Optional[str] = Field(None, description="Follow-up instructions or next appointment")
    notes: Optional[str] = Field(None, description="Any additional notes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "patient_name": "Robert Williams",
                "patient_age": 52,
                "patient_contact": "+1-555-0400",
                "visit_date": "2025-10-17",
                "clinic_info": {
                    "clinic_name": "City Medical Center",
                    "clinic_location": "123 Healthcare Ave, Suite 200",
                    "clinic_contact": "+1-555-0500"
                },
                "doctor_name": "Dr. Emily Chen",
                "doctor_specialty": "Cardiologist",
                "diagnosis": "Hypertension",
                "procedures": [
                    "Blood pressure measurement",
                    "ECG"
                ],
                "medications": [
                    {
                        "name": "Lisinopril",
                        "dosage": "10mg",
                        "frequency": "once daily",
                        "duration": "ongoing"
                    }
                ],
                "recommendations": [
                    "Reduce sodium intake",
                    "Exercise 30 minutes daily",
                    "Monitor blood pressure at home"
                ],
                "follow_up": "Return in 3 months for follow-up",
                "notes": "Patient responding well to treatment"
            }
        }

