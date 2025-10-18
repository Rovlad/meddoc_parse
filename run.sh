#!/bin/bash

# Script to run the Medical Documents OCR API server

echo "🏥 Starting Medical Documents OCR API Server..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   python -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "   Please create a .env file with your OPENAI_API_KEY"
    echo "   You can copy .env.example as a template"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run the server
echo "🚀 Server starting on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

