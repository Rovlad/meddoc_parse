# Web Testing Interface Guide 🧪

## Overview

The web testing interface provides a beautiful, user-friendly way to test the Medical Documents OCR API without writing any code.

## Access

Simply visit: **http://localhost:8000/test** (after starting the server)

## Features

### 🎨 Modern, Beautiful UI
- Gradient purple background
- Clean white card design
- Responsive layout
- Professional styling

### 📤 Easy File Upload
1. Click the "📁 Выбрать файл" (Choose File) button
2. Select a medical document image (JPG, PNG, or PDF)
3. See an instant preview of your uploaded image
4. Click "🔍 Анализировать" (Analyze) to process

### ⏱️ Real-time Feedback
- Loading spinner while processing
- Progress messages
- Processing time display
- Confidence score visualization

### 📊 Beautiful Results Display

The results are displayed in a clean, organized format:

#### Header Section
- **Document Type Badge**: Shows the detected document type (Рецепт, Лабораторный анализ, etc.)
- **Confidence Score**: Displays accuracy percentage (e.g., "Точность: 95.0%")
- **Processing Time**: Shows how long the analysis took

#### Data Section
Each field is displayed in a nice card format with:
- **Clear labels** in Russian (e.g., "Имя пациента", "Диагноз")
- **Formatted values** with proper spacing
- **Special formatting** for:
  - Lists (medications, procedures, recommendations)
  - Nested objects (lab_info, facility_info)
  - Arrays of objects (test results with all details)

#### Medications Display
For prescriptions, medications are shown in individual cards with:
- Medication number
- Name
- Dosage
- Frequency
- Duration
- Instructions

#### Test Results Display
For lab reports, each test is shown with:
- Test name
- Result value
- Unit of measurement
- Reference range
- Status (normal/abnormal/critical)

### 🔄 JSON Toggle
Click "Показать JSON" (Show JSON) to see:
- Complete raw API response
- Nicely formatted JSON
- Syntax highlighting (green on dark background)
- Easy copy-paste for debugging

### ❌ Error Handling
- Clear error messages in red boxes
- Connection error detection
- Invalid file format warnings
- File size limit notifications

## Use Cases

### 1. Quick Testing
Perfect for:
- Testing the API without code
- Verifying document type detection
- Checking extraction accuracy
- Demo purposes

### 2. Development
Great for:
- Debugging extraction issues
- Testing different document types
- Comparing results
- Validating Russian language output

### 3. Presentation
Ideal for:
- Showing the API to stakeholders
- Client demonstrations
- User acceptance testing
- Training sessions

## Interface Layout

```
┌─────────────────────────────────────────────────┐
│     🏥 Тестирование OCR                         │
│     Загрузите медицинский документ для анализа  │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│                                                 │
│        Выберите документ                        │
│                                                 │
│         [📁 Выбрать файл]                       │
│                                                 │
│         Файл не выбран                          │
│                                                 │
│    [Preview of uploaded image appears here]     │
│                                                 │
│         [🔍 Анализировать]                      │
│                                                 │
└─────────────────────────────────────────────────┘

[After analysis, results appear below:]

┌─────────────────────────────────────────────────┐
│  Результаты анализа                             │
│  [Рецепт]                    Точность: 95.0%    │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │ Имя пациента                               │ │
│  │ Иван Петров                                │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │ Диагноз                                    │ │
│  │ Бактериальная инфекция                     │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  [More fields...]                               │
│                                                 │
│                  Время обработки: 1234мс        │
│                                                 │
│            [Показать JSON]                      │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Color Scheme

- **Primary**: Purple gradient (#667eea → #764ba2)
- **Success**: Green (#48bb78)
- **Background**: White cards on gradient
- **Text**: Dark gray (#2d3748)
- **Borders**: Light gray (#e2e8f0)
- **Error**: Red (#c53030)

## Browser Compatibility

Works on:
- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Mobile browsers

## Tips

1. **Best Image Quality**: Use clear, high-resolution images for best results
2. **File Size**: Keep images under 10MB
3. **Format**: JPG and PNG work best
4. **Language**: All results will be in Russian as configured
5. **JSON View**: Use for debugging or copying data programmatically

## Advantages Over API Testing

Compared to using cURL or Swagger UI:
- ✅ No technical knowledge required
- ✅ Beautiful, intuitive interface
- ✅ Image preview before upload
- ✅ Formatted, readable results
- ✅ Perfect for non-developers
- ✅ Great for presentations
- ✅ Mobile-friendly

## Next Steps

After testing:
1. If results are good → Use the API in your application
2. If accuracy needs improvement → Adjust prompts in `app/services/document_parser.py`
3. For integration → Check the example_client.py or use the API directly

Enjoy testing! 🎉

