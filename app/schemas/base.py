"""Base schema definitions"""

from enum import Enum


class DocumentType(str, Enum):
    """Supported medical document types"""
    
    PRESCRIPTION = "prescription"
    LAB_REPORT = "lab_report"
    DOCTOR_VISIT = "doctor_visit"
    DIAGNOSTIC_RESULTS = "diagnostic_results"
    UNKNOWN = "unknown"
    
    @classmethod
    def get_description(cls, doc_type: "DocumentType") -> str:
        """Get human-readable description of document type"""
        descriptions = {
            cls.PRESCRIPTION: "Medical Prescription",
            cls.LAB_REPORT: "Laboratory Test Report",
            cls.DOCTOR_VISIT: "Doctor's Visit Summary",
            cls.DIAGNOSTIC_RESULTS: "Diagnostic Imaging Results (X-ray, MRI, CT, Ultrasound)",
            cls.UNKNOWN: "Unknown Document Type"
        }
        return descriptions.get(doc_type, "Unknown")

