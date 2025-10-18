"""Prescription document schema"""

from pydantic import BaseModel, Field
from typing import Optional, List


class Medication(BaseModel):
    """Individual medication details"""
    
    name: str = Field(..., description="Name of the medication")
    dosage: str = Field(..., description="Dosage amount (e.g., '500mg', '10ml')")
    frequency: str = Field(..., description="How often to take (e.g., '3 times daily', 'twice a day')")
    duration: str = Field(..., description="How long to take (e.g., '7 days', '2 weeks')")
    instructions: Optional[str] = Field(None, description="Additional instructions (e.g., 'after meals')")


class PrescriptionSchema(BaseModel):
    """Schema for prescription documents"""
    
    # Patient Information
    patient_name: str = Field(..., description="Full name of the patient")
    patient_age: Optional[int] = Field(None, description="Age of the patient")
    patient_contact: Optional[str] = Field(None, description="Patient contact number or email")
    
    # Doctor Information
    doctor_name: str = Field(..., description="Full name of the prescribing doctor")
    doctor_specialty: Optional[str] = Field(None, description="Doctor's specialty")
    doctor_contact: Optional[str] = Field(None, description="Doctor's contact details")
    
    # Dates
    prescription_date: str = Field(..., description="Date when prescription was issued (YYYY-MM-DD format)")
    validity_date: Optional[str] = Field(None, description="Prescription expiry/validity date (YYYY-MM-DD format)")
    
    # Medications
    medications: List[Medication] = Field(..., description="List of prescribed medications")
    
    # Additional Information
    diagnosis: Optional[str] = Field(None, description="Diagnosis or condition")
    notes: Optional[str] = Field(None, description="Any additional notes or instructions")
    
    class Config:
        json_schema_extra = {
            "example": {
                "patient_name": "John Doe",
                "patient_age": 45,
                "patient_contact": "+1-555-0100",
                "doctor_name": "Dr. Sarah Smith",
                "doctor_specialty": "General Physician",
                "doctor_contact": "+1-555-0200",
                "prescription_date": "2025-10-15",
                "validity_date": "2026-01-15",
                "medications": [
                    {
                        "name": "Amoxicillin",
                        "dosage": "500mg",
                        "frequency": "3 times daily",
                        "duration": "7 days",
                        "instructions": "Take after meals"
                    }
                ],
                "diagnosis": "Bacterial infection",
                "notes": "Follow up if symptoms persist"
            }
        }

