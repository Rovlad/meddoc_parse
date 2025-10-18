"""Diagnostic imaging results document schema"""

from pydantic import BaseModel, Field
from typing import Optional


class FacilityInfo(BaseModel):
    """Diagnostic facility information"""
    
    facility_name: str = Field(..., description="Name of the diagnostic facility")
    facility_location: Optional[str] = Field(None, description="Facility address or location")
    facility_contact: Optional[str] = Field(None, description="Facility contact number or email")


class DiagnosticResultsSchema(BaseModel):
    """Schema for diagnostic imaging results (X-ray, MRI, CT, Ultrasound)"""
    
    # Patient Information
    patient_name: str = Field(..., description="Full name of the patient")
    patient_age: Optional[int] = Field(None, description="Age of the patient")
    patient_id: Optional[str] = Field(None, description="Patient ID or registration number")
    
    # Study Information
    diagnostic_type: str = Field(..., description="Type of diagnostic study: ultrasound, x-ray, mri, or ct")
    study_date: str = Field(..., description="Date when study was performed (YYYY-MM-DD format)")
    
    # Facility Information
    facility_info: FacilityInfo = Field(..., description="Diagnostic facility details")
    
    # Medical Staff
    referring_physician: Optional[str] = Field(None, description="Name of the referring physician")
    radiologist_name: Optional[str] = Field(None, description="Name of the radiologist who read the study")
    
    # Results
    body_part_examined: Optional[str] = Field(None, description="Body part or region examined")
    findings_summary: str = Field(..., description="Summary of findings from the diagnostic study")
    impression: Optional[str] = Field(None, description="Radiologist's impression or conclusion")
    recommendations: Optional[str] = Field(None, description="Recommendations for follow-up or additional studies")
    
    # Additional Information
    notes: Optional[str] = Field(None, description="Any additional notes or technical details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "patient_name": "Lisa Anderson",
                "patient_age": 48,
                "patient_id": "P789012",
                "diagnostic_type": "mri",
                "study_date": "2025-10-18",
                "facility_info": {
                    "facility_name": "Advanced Imaging Center",
                    "facility_location": "456 Medical Plaza, Suite 200",
                    "facility_contact": "+1-555-0500"
                },
                "referring_physician": "Dr. Robert Johnson",
                "radiologist_name": "Dr. David Lee",
                "body_part_examined": "Lumbar Spine",
                "findings_summary": "Mild degenerative disc disease at L4-L5. No herniation or spinal stenosis.",
                "impression": "Mild degenerative changes, no acute abnormalities",
                "recommendations": "Clinical correlation recommended. Follow-up as needed.",
                "notes": "MRI without contrast"
            }
        }

