# Step-by-Step Guide to Set Up OCR Functionality

Follow these steps to get OCR and AI summarization working for your medical documents:

## Step 1: Install Tesseract OCR

1. Download the installer from: https://github.com/UB-Mannheim/tesseract/wiki
   - Choose the 64-bit version: `tesseract-ocr-w64-setup-v5.3.3.20231005.exe`

2. Run the installer:
   - Accept the license agreement
   - Choose the default installation location (typically `C:\Program Files\Tesseract-OCR\`)
   - **IMPORTANT**: Make sure to select at least "English" in the additional language data screen
   - Complete the installation

## Step 2: Set the Tesseract Path

Choose ONE of these methods:

### Method A: Set Environment Variable (Recommended)
1. Right-click on "This PC" → Properties
2. Click "Advanced system settings"
3. Click the "Environment Variables" button
4. Under "System variables", click "New"
5. Variable name: `TESSERACT_PATH`
6. Variable value: `C:\Program Files\Tesseract-OCR\tesseract.exe` (adjust if installed elsewhere)
7. Click "OK" on all dialogs

### Method B: Edit the Code Directly
1. Open `app/ocr_service.py`
2. Find the `setup_tesseract()` function (around line 15)
3. Uncomment and modify these lines:
   ```python
   # IMPORTANT - HARDCODED PATH - uncomment and set your actual path if needed
   custom_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   pytesseract.pytesseract.tesseract_cmd = custom_path
   return True
   ```

## Step 3: Test Your Setup

1. Run the Tesseract checker:
   ```
   python tesseract_check.py
   ```
   This should show "✅ Tesseract found at: [your path]"

2. Test with a sample medical image:
   ```
   python ocr_debug.py
   ```
   This should process the test image and show the extracted text

## Step 4: Try the OCR API Endpoint

1. Make sure your Flask server is running:
   ```
   python app.py
   ```

2. Visit or call the test endpoint:
   ```
   http://localhost:5000/test-ocr
   ```
   This should process the sample image and return both the extracted text and a summary

## Step 5: Test with Your Own Documents

1. Use the OCR upload page in the frontend to upload your own medical documents
2. The system should extract text using Tesseract and then summarize it with AI

## Troubleshooting

If you encounter issues:

1. Check the console output for specific error messages
2. Verify that Tesseract is installed correctly
3. Make sure the path to Tesseract is set correctly
4. Check if your images are clear enough for OCR to work properly

For more detailed troubleshooting, refer to `README-OCR-TROUBLESHOOTING.md`. 