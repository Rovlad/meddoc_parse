#!/usr/bin/env python
"""
Example client for testing the Medical Documents OCR API

Usage:
    python example_client.py <path_to_image>
"""

import sys
import requests
import json
from pathlib import Path


def analyze_document(image_path: str, api_url: str = "http://localhost:8000"):
    """
    Analyze a medical document image
    
    Args:
        image_path: Path to the image file
        api_url: Base URL of the API
    """
    # Check if file exists
    if not Path(image_path).exists():
        print(f"❌ Error: File not found: {image_path}")
        return
    
    # Prepare the file
    with open(image_path, 'rb') as f:
        files = {'file': f}
        
        print(f"📤 Uploading {image_path}...")
        print(f"🔗 API URL: {api_url}/api/v1/analyze")
        
        try:
            # Make the request
            response = requests.post(
                f"{api_url}/api/v1/analyze",
                files=files,
                timeout=60
            )
            
            # Check response
            if response.status_code == 200:
                result = response.json()
                
                print("\n✅ Analysis Complete!")
                print("=" * 60)
                print(f"Document Type: {result['document_type']}")
                print(f"Confidence: {result['confidence']:.2%}")
                print(f"Processing Time: {result['processing_time_ms']}ms")
                print("\n📋 Extracted Data:")
                print(json.dumps(result['data'], indent=2))
                print("=" * 60)
            else:
                print(f"\n❌ Error: {response.status_code}")
                print(response.json())
                
        except requests.exceptions.ConnectionError:
            print(f"\n❌ Error: Could not connect to API at {api_url}")
            print("   Make sure the server is running!")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


def check_health(api_url: str = "http://localhost:8000"):
    """Check API health"""
    try:
        response = requests.get(f"{api_url}/api/v1/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API is healthy (version {data['version']})")
            return True
        else:
            print("❌ API health check failed")
            return False
    except:
        print("❌ Cannot connect to API")
        return False


def main():
    """Main function"""
    print("🏥 Medical Documents OCR API - Example Client")
    print()
    
    # Check health first
    if not check_health():
        print("\nPlease start the server first:")
        print("   uvicorn app.main:app --reload")
        return
    
    # Check arguments
    if len(sys.argv) < 2:
        print("\nUsage:")
        print(f"   python {sys.argv[0]} <path_to_image>")
        print("\nExample:")
        print(f"   python {sys.argv[0]} prescription.jpg")
        return
    
    # Analyze the document
    image_path = sys.argv[1]
    analyze_document(image_path)


if __name__ == "__main__":
    main()

