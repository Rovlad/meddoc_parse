"""API endpoint tests"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert data["name"] == "Medical Documents OCR API"


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_supported_documents():
    """Test supported documents endpoint"""
    response = client.get("/api/v1/supported-documents")
    assert response.status_code == 200
    data = response.json()
    assert "supported_documents" in data
    assert len(data["supported_documents"]) > 0
    
    # Check that all required document types are present
    doc_types = [doc["type"] for doc in data["supported_documents"]]
    assert "prescription" in doc_types
    assert "lab_report" in doc_types
    assert "doctor_visit" in doc_types
    assert "diagnostic_results" in doc_types


def test_analyze_no_file():
    """Test analyze endpoint without file"""
    response = client.post("/api/v1/analyze")
    assert response.status_code == 422  # Validation error


def test_analyze_invalid_file_type():
    """Test analyze endpoint with invalid file type"""
    files = {"file": ("test.txt", b"Not an image", "text/plain")}
    response = client.post("/api/v1/analyze", files=files)
    assert response.status_code == 400


# Note: Additional tests would require mock images or test fixtures
# For full integration tests, you would need actual medical document images

