"""API response models"""

from pydantic import BaseModel, Field
from typing import Optional, Any, List, Dict
from app.schemas.base import DocumentType


class AnalyzeResponse(BaseModel):
    """Response model for document analysis"""
    
    success: bool = Field(..., description="Whether the analysis was successful")
    document_type: DocumentType = Field(..., description="Identified document type")
    confidence: float = Field(..., description="Confidence score for document type (0-1)")
    data: Optional[Dict[str, Any]] = Field(None, description="Parsed document data according to document-specific schema")
    raw_text: Optional[str] = Field(None, description="Raw extracted text from the document")
    processing_time_ms: int = Field(..., description="Processing time in milliseconds")
    error: Optional[str] = Field(None, description="Error message if analysis failed")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "document_type": "prescription",
                "confidence": 0.95,
                "data": {
                    "patient_name": "John Doe",
                    "patient_age": 45,
                    "doctor_name": "Dr. Sarah Smith",
                    "prescription_date": "2025-10-15",
                    "medications": [
                        {
                            "name": "Amoxicillin",
                            "dosage": "500mg",
                            "frequency": "3 times daily",
                            "duration": "7 days"
                        }
                    ]
                },
                "raw_text": "Original extracted text...",
                "processing_time_ms": 1234,
                "error": None
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0"
            }
        }


class DocumentTypeInfo(BaseModel):
    """Information about a supported document type"""
    
    type: DocumentType = Field(..., description="Document type identifier")
    name: str = Field(..., description="Human-readable name")
    description: str = Field(..., description="Description of the document type")


class SupportedDocumentsResponse(BaseModel):
    """Response listing supported document types"""
    
    supported_documents: List[DocumentTypeInfo] = Field(..., description="List of supported document types")
    
    class Config:
        json_schema_extra = {
            "example": {
                "supported_documents": [
                    {
                        "type": "prescription",
                        "name": "Prescription",
                        "description": "Medical prescription with medications and dosages"
                    },
                    {
                        "type": "lab_report",
                        "name": "Lab Report",
                        "description": "Laboratory test results"
                    }
                ]
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    
    success: bool = Field(False, description="Always false for errors")
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "Invalid file format",
                "detail": "Only JPG, PNG, and PDF files are supported"
            }
        }

