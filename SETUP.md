# Quick Setup Guide 🚀

## Step 1: Set up your environment

First, make sure you have your OpenAI API key ready. You'll need access to GPT-4o-mini.

## Step 2: Update your .env file

Open the `.env` file in the project root and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
MAX_FILE_SIZE_MB=10
ALLOWED_EXTENSIONS=jpg,jpeg,png,pdf
LOG_LEVEL=INFO
API_V1_PREFIX=/api/v1
CORS_ORIGINS=*
```

## Step 3: Create a virtual environment

```bash
python -m venv venv
```

## Step 4: Activate the virtual environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

## Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

## Step 6: Start the server

**Option A - Using the run script (recommended):**
```bash
./run.sh
```

**Option B - Using uvicorn directly:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Step 7: Test the API

Open your browser and go to:
- **Testing Interface**: http://localhost:8000/test (Best for quick testing!)
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Step 8: Test with an image

**Option A - Use the Web Interface (Easiest!):**
1. Go to http://localhost:8000/test
2. Click "Выбрать файл" (Choose File) and select a medical document image
3. Click "Анализировать" (Analyze)
4. View the results in the nice formatted display
5. Toggle "Показать JSON" to see the raw response

**Option B - Use the example client:**
```bash
python example_client.py /path/to/your/medical-document.jpg
```

**Option C - Use cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/medical-document.jpg"
```

**Option D - Use the Swagger UI:**
1. Go to http://localhost:8000/docs
2. Find the `/api/v1/analyze` endpoint
3. Click "Try it out"
4. Upload your image file
5. Click "Execute"

## Troubleshooting 🔧

### Issue: "Module not found" error
**Solution:** Make sure you're in the virtual environment and have installed all requirements:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: "OpenAI API key not found"
**Solution:** Check that your `.env` file exists and contains a valid `OPENAI_API_KEY`

### Issue: "Port already in use"
**Solution:** Either stop the other process using port 8000, or run on a different port:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### Issue: "Invalid image file"
**Solution:** Make sure your image is a valid JPG, PNG, or PDF file and is under 10MB

## Next Steps 🎯

1. Try analyzing different types of medical documents
2. Check the accuracy of extracted data
3. Adjust the prompts in `app/services/document_parser.py` if needed
4. Add your own custom document types by extending the schemas

## Support

If you encounter any issues, check:
1. The server logs for detailed error messages
2. The OpenAI API dashboard for usage and errors
3. That your API key has sufficient credits

Happy coding! 🎉

