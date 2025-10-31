"""Lab report document schema"""

from pydantic import BaseModel, Field
from typing import Optional, List


class LabInfo(BaseModel):
    """Laboratory information"""
    
    lab_name: str = Field(..., description="Name of the laboratory")
    lab_location: Optional[str] = Field(None, description="Laboratory address or location")
    lab_contact: Optional[str] = Field(None, description="Laboratory contact number or email")


class TestResult(BaseModel):
    """Individual test result"""
    
    test_name: str = Field(..., description="Name of the test")
    result_value: str = Field(..., description="Test result value")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    reference_range: Optional[str] = Field(None, description="Normal reference range")
    status: Optional[str] = Field(None, description="Status: normal, abnormal, or critical")


class LabReportSchema(BaseModel):
    """Schema for laboratory test reports"""
    
    # Summary
    summary: str = Field(..., description="One-sentence summary of the lab report")
    
    # Patient Information
    patient_name: str = Field(..., description="Full name of the patient")
    patient_age: Optional[int] = Field(None, description="Age of the patient")
    patient_id: Optional[str] = Field(None, description="Patient ID or registration number")
    
    # Dates
    visit_date: Optional[str] = Field(None, description="Date when patient visited the medical institution (YYYY-MM-DD format)")
    report_date: str = Field(..., description="Date when report was generated (YYYY-MM-DD format)")
    collection_date: Optional[str] = Field(None, description="Date when samples were collected (YYYY-MM-DD format)")
    
    # Lab Information
    lab_info: LabInfo = Field(..., description="Laboratory details")
    
    # Doctor Information
    doctor_name: Optional[str] = Field(None, description="Referring doctor's name")
    
    # Test Results
    test_results: List[TestResult] = Field(..., description="List of test results")
    
    # Additional Information
    notes: Optional[str] = Field(None, description="Any additional notes or comments")
    
    class Config:
        json_schema_extra = {
            "example": {
                "summary": "Blood test results showing normal hemoglobin and slightly elevated glucose levels",
                "patient_name": "Jane Smith",
                "patient_age": 35,
                "patient_id": "P123456",
                "visit_date": "2025-10-15",
                "report_date": "2025-10-16",
                "collection_date": "2025-10-15",
                "lab_info": {
                    "lab_name": "City Diagnostics Center",
                    "lab_location": "123 Main St, Suite 100",
                    "lab_contact": "+1-555-0300"
                },
                "doctor_name": "Dr. Michael Johnson",
                "test_results": [
                    {
                        "test_name": "Hemoglobin",
                        "result_value": "14.5",
                        "unit": "g/dL",
                        "reference_range": "12.0-16.0",
                        "status": "normal"
                    },
                    {
                        "test_name": "Blood Glucose",
                        "result_value": "110",
                        "unit": "mg/dL",
                        "reference_range": "70-100",
                        "status": "abnormal"
                    }
                ],
                "notes": "Fasting sample"
            }
        }

