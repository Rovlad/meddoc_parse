"""API request models"""

from pydantic import BaseModel, Field
from typing import Optional


class AnalyzeRequest(BaseModel):
    """Request model for document analysis (for documentation purposes)"""
    
    file: bytes = Field(..., description="Image file to analyze (multipart/form-data)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "file": "binary image data"
            }
        }

