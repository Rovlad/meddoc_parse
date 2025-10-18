# Medical Documents OCR API 🏥

A FastAPI-powered API server that analyzes medical document images using OpenAI's GPT-4o-mini vision model. The API automatically identifies document types and extracts structured information according to document-specific schemas.

## Features ✨

- **Automatic Document Classification** - Identifies the type of medical document
- **Structured Data Extraction** - Extracts relevant information based on document type
- **Multiple Document Types Supported**:
  - 💊 Prescriptions
  - 🔬 Lab Reports
  - 👨‍⚕️ Doctor's Visit Summaries
  - 🏥 Diagnostic Results (X-ray, MRI, CT, Ultrasound)
- **RESTful API** with automatic OpenAPI documentation
- **Image Optimization** - Automatic image resizing and format conversion
- **Validation** - File size and format validation
- **CORS Support** - Ready for web client integration

## Prerequisites 📋

- Python 3.8+
- OpenAI API key with access to GPT-4o-mini

## Installation 🚀

1. **Clone the repository**
```bash
cd meddocs_ocr
```

2. **Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
MAX_FILE_SIZE_MB=10
ALLOWED_EXTENSIONS=jpg,jpeg,png,pdf
LOG_LEVEL=INFO
API_V1_PREFIX=/api/v1
CORS_ORIGINS=*
```

## Usage 🎯

### Start the Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The server will start at `http://localhost:8000`

### Testing Interface

Once the server is running, visit the **interactive testing page**:
- **Test Page**: http://localhost:8000/test

This provides a user-friendly web interface where you can:
- Upload medical document images
- See real-time analysis results
- View extracted data in a formatted display
- Toggle JSON view for raw response data

### API Documentation

For developers, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### 0. Testing Interface (Web UI)
```
GET /test
```
Opens an interactive web interface for testing document analysis. Simply visit http://localhost:8000/test in your browser.

#### 1. Health Check
```bash
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

#### 2. Supported Documents
```bash
GET /api/v1/supported-documents
```

**Response:**
```json
{
  "supported_documents": [
    {
      "type": "prescription",
      "name": "Prescription",
      "description": "Medical Prescription"
    },
    ...
  ]
}
```

#### 3. Analyze Document (Main Endpoint)
```bash
POST /api/v1/analyze
Content-Type: multipart/form-data

file: [image file]
```

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@prescription.jpg"
```

**Example using Python:**
```python
import requests

url = "http://localhost:8000/api/v1/analyze"
files = {"file": open("prescription.jpg", "rb")}

response = requests.post(url, files=files)
print(response.json())
```

**Example Response:**
```json
{
  "success": true,
  "document_type": "prescription",
  "confidence": 0.95,
  "data": {
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
  },
  "raw_text": null,
  "processing_time_ms": 1234,
  "error": null
}
```

## Document Schemas 📄

### Prescription
Extracts: patient info, doctor info, prescription date, validity date, medications with dosage/frequency/duration, diagnosis, notes

### Lab Report
Extracts: patient info, report dates, lab information (name, location, contact), referring doctor, test results with reference ranges, notes

### Doctor's Visit Summary
Extracts: patient info, visit date, doctor info, diagnosis, procedures performed, medications prescribed, recommendations, follow-up instructions

### Diagnostic Results
Extracts: patient info, diagnostic type (X-ray/MRI/CT/Ultrasound), study date, facility information, physicians, body part examined, findings summary, impression, recommendations

## Project Structure 📁

```
meddocs_ocr/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── config.py                  # Configuration
│   ├── models/
│   │   ├── requests.py            # Request models
│   │   └── responses.py           # Response models
│   ├── schemas/
│   │   ├── base.py                # Base schemas
│   │   ├── prescription.py        # Prescription schema
│   │   ├── lab_report.py          # Lab report schema
│   │   ├── doctor_visit.py        # Doctor visit schema
│   │   └── diagnostic_results.py  # Diagnostic results schema
│   ├── services/
│   │   ├── openai_service.py      # OpenAI integration
│   │   ├── document_classifier.py # Document classification
│   │   └── document_parser.py     # Data extraction
│   └── utils/
│       └── image_utils.py         # Image processing
├── .env                           # Environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## Configuration ⚙️

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `MAX_FILE_SIZE_MB` | Maximum upload size in MB | 10 |
| `ALLOWED_EXTENSIONS` | Comma-separated file extensions | jpg,jpeg,png,pdf |
| `LOG_LEVEL` | Logging level | INFO |
| `API_V1_PREFIX` | API version prefix | /api/v1 |
| `CORS_ORIGINS` | CORS allowed origins | * |

## Error Handling 🔧

The API returns appropriate HTTP status codes:

- **200**: Success
- **400**: Bad request (invalid file, format, size)
- **500**: Server error

Error response format:
```json
{
  "success": false,
  "error": "Error message",
  "detail": "Detailed error information"
}
```

## Development 💻

### Run Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black app/
```

### Type Checking
```bash
mypy app/
```

## Limitations & Considerations ⚠️

1. **Accuracy**: OCR accuracy depends on image quality and document clarity
2. **Language**: Currently optimized for English documents
3. **Privacy**: No images are stored; processing is done in memory
4. **Rate Limits**: Subject to OpenAI API rate limits
5. **Cost**: Each API call uses OpenAI tokens (GPT-4o-mini)

## Security 🔒

- API keys are stored in environment variables
- No image data is persisted
- File size and type validation
- CORS configuration for production use

## Future Enhancements 🚀

- [ ] Add support for more document types
- [ ] Implement batch processing
- [ ] Add authentication and API keys
- [ ] Support for multi-page PDFs
- [ ] Add confidence thresholds
- [ ] Implement caching for repeated documents
- [ ] Add webhook notifications
- [ ] Support for multiple languages

## License 📝

MIT License - feel free to use this project for your own purposes.

## Support 💬

For issues, questions, or contributions, please open an issue on the repository.

---

Built with ❤️ using FastAPI and OpenAI GPT-4o-mini

