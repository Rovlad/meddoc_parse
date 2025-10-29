"""Main FastAPI application"""

import logging
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import List
from pathlib import Path

from app.config import settings
from app.models import (
    AnalyzeResponse,
    HealthResponse,
    SupportedDocumentsResponse,
    DocumentTypeInfo,
    ErrorResponse
)
from app.schemas.base import DocumentType
from app.services import OpenAIService, DocumentClassifier, DocumentParser
from app.utils import encode_image_to_base64, validate_image, get_file_extension
from app import __version__

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Global service instances
openai_service: OpenAIService = None
document_classifier: DocumentClassifier = None
document_parser: DocumentParser = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    # Startup
    logger.info("Starting Medical Documents OCR API...")
    global openai_service, document_classifier, document_parser
    
    # Initialize services
    openai_service = OpenAIService()
    document_classifier = DocumentClassifier(openai_service)
    document_parser = DocumentParser(openai_service)
    
    logger.info("Services initialized successfully")
    yield
    
    # Shutdown
    logger.info("Shutting down Medical Documents OCR API...")


# Create FastAPI app
app = FastAPI(
    title="Medical Documents OCR API",
    description="API for analyzing and extracting structured data from medical documents",
    version=__version__,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    f"{settings.api_v1_prefix}/health",
    response_model=HealthResponse,
    tags=["Health"]
)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=__version__
    )


@app.get(
    f"{settings.api_v1_prefix}/supported-documents",
    response_model=SupportedDocumentsResponse,
    tags=["Information"]
)
async def get_supported_documents():
    """Get list of supported document types"""
    supported_docs = [
        DocumentTypeInfo(
            type=DocumentType.PRESCRIPTION,
            name="Prescription",
            description=DocumentType.get_description(DocumentType.PRESCRIPTION)
        ),
        DocumentTypeInfo(
            type=DocumentType.LAB_REPORT,
            name="Lab Report",
            description=DocumentType.get_description(DocumentType.LAB_REPORT)
        ),
        DocumentTypeInfo(
            type=DocumentType.DOCTOR_VISIT,
            name="Doctor's Visit Summary",
            description=DocumentType.get_description(DocumentType.DOCTOR_VISIT)
        ),
        DocumentTypeInfo(
            type=DocumentType.DIAGNOSTIC_RESULTS,
            name="Diagnostic Results",
            description=DocumentType.get_description(DocumentType.DIAGNOSTIC_RESULTS)
        ),
    ]
    
    return SupportedDocumentsResponse(supported_documents=supported_docs)


@app.post(
    f"{settings.api_v1_prefix}/analyze",
    response_model=AnalyzeResponse,
    tags=["Analysis"],
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def analyze_document(file: UploadFile = File(...)):
    """
    Analyze a medical document image and extract structured data
    
    Args:
        file: Image file to analyze (JPG, PNG, or PDF)
        
    Returns:
        Analysis results with document type and extracted data
    """
    start_time = time.time()
    
    try:
        # Validate file extension
        file_ext = get_file_extension(file.filename)
        if file_ext not in settings.allowed_extensions_list:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "error": "Invalid file format",
                    "detail": f"Only {', '.join(settings.allowed_extensions_list).upper()} files are supported"
                }
            )
        
        # Read file content
        file_content = await file.read()
        
        # Validate image
        is_valid, error_msg = validate_image(
            file_content,
            settings.max_file_size_bytes,
            settings.allowed_extensions_list
        )
        
        if not is_valid:
            logger.error(f"Image validation failed for {file.filename}: {error_msg}")
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "error": "Invalid file",
                    "detail": error_msg
                }
            )
        
        # Encode image to base64
        try:
            base64_image = encode_image_to_base64(file_content, file.filename)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "error": "Failed to process image",
                    "detail": str(e)
                }
            )
        
        # Classify document
        logger.info(f"Classifying document: {file.filename}")
        document_type, confidence = await document_classifier.classify(base64_image)
        logger.info(f"Document classified as {document_type.value} with confidence {confidence}")
        
        # Parse document if not unknown
        parsed_data = None
        if document_type != DocumentType.UNKNOWN:
            logger.info(f"Parsing {document_type.value} document")
            parsed_data = await document_parser.parse(base64_image, document_type)
        
        # Calculate processing time
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        # Build response
        return AnalyzeResponse(
            success=True,
            document_type=document_type,
            confidence=confidence,
            data=parsed_data,
            raw_text=None,  # Could add OCR text extraction if needed
            processing_time_ms=processing_time_ms,
            error=None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing document: {str(e)}", exc_info=True)
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        return AnalyzeResponse(
            success=False,
            document_type=DocumentType.UNKNOWN,
            confidence=0.0,
            data=None,
            raw_text=None,
            processing_time_ms=processing_time_ms,
            error=str(e)
        )


@app.get("/test", response_class=HTMLResponse, tags=["Testing"])
async def test_page():
    """
    Web interface for testing document analysis
    
    Returns an HTML page with file upload form and results display
    """
    template_path = Path(__file__).parent / "templates" / "test.html"
    
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>Error: Template file not found</h1>",
            status_code=500
        )


@app.get("/debug/env", tags=["Debug"])
async def debug_env():
    """Debug endpoint to check environment variables"""
    import os
    return {
        "openai_api_key_set": bool(settings.openai_api_key),
        "openai_api_key_length": len(settings.openai_api_key) if settings.openai_api_key else 0,
        "openai_api_key_starts_with": settings.openai_api_key[:7] if settings.openai_api_key else "EMPTY",
        "env_vars_available": {
            "OPENAI_API_KEY": "SET" if os.getenv("OPENAI_API_KEY") else "NOT SET",
            "PORT": os.getenv("PORT", "NOT SET"),
            "RAILWAY_ENVIRONMENT": os.getenv("RAILWAY_ENVIRONMENT", "NOT SET"),
        },
        "all_env_vars": [key for key in os.environ.keys() if not key.startswith("_")]
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Medical Documents OCR API",
        "version": __version__,
        "status": "running",
        "endpoints": {
            "health": f"{settings.api_v1_prefix}/health",
            "supported_documents": f"{settings.api_v1_prefix}/supported-documents",
            "analyze": f"{settings.api_v1_prefix}/analyze",
            "test": "/test",
            "debug": "/debug/env"
        },
        "documentation": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

