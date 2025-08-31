# OCR Troubleshooting Guide

If you're experiencing issues with the OCR (Optical Character Recognition) feature, follow this troubleshooting guide to resolve common problems.

## Common Issues and Solutions

### 1. "Tesseract not found" Error

**Symptoms**: 
- Error message mentioning "Tesseract not found" or "tesseract_cmd is not valid"
- OCR processing fails consistently

**Solutions**:
1. Ensure Tesseract OCR is installed on your system:
   - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
   - Mac: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`

2. Verify the Tesseract path in the code:
   - Check `app/ocr_service.py` - the path should be set to your Tesseract installation location
   - Default Windows path: `C:\Program Files\Tesseract-OCR\tesseract.exe`
   - You can modify this path to match your installation

3. Add Tesseract to your system PATH:
   - Windows: Add the Tesseract installation directory to your system environment variables
   - Restart your terminal or computer after making changes

4. Set environment variable (alternative method):
   - Set the `TESSERACT_PATH` environment variable to point to your Tesseract executable
   - For example: `set TESSERACT_PATH=C:\path\to\tesseract.exe` (Windows) or 
   - `export TESSERACT_PATH=/usr/local/bin/tesseract` (macOS/Linux)

### 2. "No text could be extracted" Error

**Symptoms**:
- OCR runs but returns no text or very little text
- Message stating "No text could be extracted from the document"

**Solutions**:
1. Check image quality:
   - Use clear, high-resolution images with good lighting
   - Ensure text is clearly visible with good contrast
   - Avoid blurry or distorted images

2. Image format:
   - Try converting your image to a different format (JPG, PNG)
   - Ensure the image is not corrupted

3. Try preprocessing the image:
   - The application now automatically converts color images to grayscale
   - It also enhances contrast and sharpens images for better OCR
   - For very low-quality images, consider using an external image editor

4. Check document language:
   - The default Tesseract configuration is for English
   - For other languages, you may need to install language packs for Tesseract

5. Try using the sample text:
   - The system will automatically use `sample_prescription.txt` as a fallback
   - You can modify this file with your own text to test AI summarization

### 3. API Connection Issues

**Symptoms**:
- OCR works but AI summarization fails
- Error related to Google Generative AI API

**Solutions**:
1. Check API key:
   - Verify the Google API key in `app/ai_service.py` is valid
   - Obtain a new API key if needed from https://ai.google.dev/

2. Set API key as environment variable:
   - Set the `GEMINI_API_KEY` environment variable with your API key
   - For example: `set GEMINI_API_KEY=your_api_key_here` (Windows) or
   - `export GEMINI_API_KEY=your_api_key_here` (macOS/Linux)

3. Network connectivity:
   - Ensure your computer has internet access
   - Check if any firewalls are blocking the connection
   - Try disabling VPN if you're using one

4. Use offline mode:
   - The system will automatically use a rule-based summarization if the API fails
   - This ensures you can still test the functionality without API access

### 4. Backend Server Not Running

**Symptoms**:
- "Failed to fetch" or connection errors in the browser console
- Frontend displays network error messages

**Solutions**:
1. Start the Flask server:
   ```
   cd Hackathon/backend
   pip install -r requirements.txt  # First time setup
   python app.py
   ```

2. Check for port conflicts:
   - Ensure no other service is using port 5000
   - If needed, modify the port in `app.py`

3. CORS issues:
   - If you see CORS errors in the browser console, ensure CORS is properly configured in the backend
   - The CORS configuration is already set up in the code

4. Check logs:
   - Look for error messages in the terminal where Flask is running
   - Check for any Python exceptions or startup errors

### 5. PDF Processing Issues

**Symptoms**:
- OCR works for images but fails for PDFs
- Error messages related to PDF processing

**Solutions**:
1. Check PDF validity:
   - Ensure the PDF is not password-protected or encrypted
   - Try opening the PDF in a viewer to verify it's not corrupted

2. PDF content type:
   - If the PDF contains only scanned images, the OCR will be applied automatically
   - If the PDF contains actual text, it should be extractable without OCR

3. PyMuPDF installation:
   - Verify that PyMuPDF is correctly installed
   - Try reinstalling it: `pip uninstall pymupdf && pip install pymupdf`

4. Large PDF handling:
   - Very large PDFs might cause memory issues
   - Try processing smaller PDFs or individual pages

## Testing the OCR Feature

For quick testing:
1. Place a sample image named `sample_prescription.jpg` in the `Hackathon/backend/static/test_docs/` directory
2. Start the Flask server
3. Visit http://localhost:5000/test-ocr in your browser to test the API directly
4. Or navigate to the Medical Document Analyzer page and use the UI

## Debugging

If you need to debug OCR issues:

1. Enable verbose logging:
   - The application now uses Python's logging module
   - Check the console output for detailed log messages
   - Look for messages from 'ocr_service' and 'ai_service' loggers

2. Check image preprocessing:
   - The system logs information about image format, size, and mode
   - It also logs the number of characters extracted

3. Check API responses:
   - The system logs API initialization and response information
   - It includes retry attempts and fallback to rule-based summarization

## Still Having Issues?

If you've tried all the above solutions and still encounter problems:

1. Check the system requirements:
   - Python 3.7 or later
   - All dependencies listed in requirements.txt
   - Tesseract OCR 4.0 or later

2. Verify file permissions:
   - Ensure the application has read/write access to its directories
   - Especially check the upload and temporary directories

3. Try with a known working example:
   - Use the provided sample_prescription.txt as a baseline
   - Compare your results with this known working example

4. Check Flask server logs:
   - All OCR and AI processing details are logged
   - Look for specific error messages that might indicate the root cause

# Tesseract OCR Setup Guide

This document provides step-by-step instructions for setting up Tesseract OCR, which is required for our medical document text extraction feature.

## Installing Tesseract OCR

### Windows Installation

1. Download the Tesseract installer from the UB Mannheim repository:
   - Go to: https://github.com/UB-Mannheim/tesseract/wiki
   - Download the appropriate version (typically the 64-bit version)
   - Current recommended version: `tesseract-ocr-w64-setup-v5.3.3.20231005.exe`

2. Run the installer:
   - Accept the license agreement
   - Choose the installation location (remember this path!)
   - **IMPORTANT**: In the "Additional language data" screen, select at least "English"
   - Complete the installation

3. After installation, you have two options to make Tesseract available to our application:

   **Option 1**: Add Tesseract to your PATH
   - Right-click on "This PC" or "My Computer" -> Properties
   - Click on "Advanced system settings"
   - Click the "Environment Variables" button
   - In the "System variables" section, find the "Path" variable and click "Edit"
   - Click "New" and add the Tesseract installation directory (e.g., `C:\Program Files\Tesseract-OCR`)
   - Click "OK" on all dialogs to save changes

   **Option 2**: Set the TESSERACT_PATH environment variable
   - Right-click on "This PC" or "My Computer" -> Properties
   - Click on "Advanced system settings"
   - Click the "Environment Variables" button
   - In the "System variables" section, click "New"
   - Variable name: `TESSERACT_PATH`
   - Variable value: Full path to tesseract.exe (e.g., `C:\Program Files\Tesseract-OCR\tesseract.exe`)
   - Click "OK" on all dialogs to save changes

   **Option 3**: Modify the code directly
   - Edit `app/ocr_service.py`
   - Find the `setup_tesseract()` function
   - Uncomment and modify the "HARDCODED PATH" section to match your Tesseract installation path

### macOS Installation

1. Install using Homebrew:
   ```
   brew install tesseract
   ```

2. Verify installation:
   ```
   tesseract --version
   ```

### Linux Installation

1. Ubuntu/Debian:
   ```
   sudo apt-get install tesseract-ocr
   ```

2. Fedora:
   ```
   sudo dnf install tesseract
   ```

3. Arch Linux:
   ```
   sudo pacman -S tesseract
   ```

4. Verify installation:
   ```
   tesseract --version
   ```

## Testing Your Installation

After installing Tesseract, run our diagnostic tools to verify everything works:

```
python tesseract_check.py
```

This will check if Tesseract is properly installed and accessible.

For a more comprehensive test:

```
python ocr_debug.py
```

This tests the complete OCR pipeline including sample document processing.

## Troubleshooting

### Common Issues

1. **Tesseract not found error**:
   - Make sure Tesseract is installed
   - Verify the path to tesseract.exe is correct
   - Try hardcoding the path in `app/ocr_service.py` as described in Option 3 above

2. **No text extracted**:
   - Ensure you have installed language data (at least English)
   - Try with a clearer image (high resolution, good contrast)
   - For PDFs, make sure they're not scanned as images at low quality

3. **Error about missing DLLs**:
   - Reinstall Tesseract and make sure to run the installer as administrator
   - Make sure your system's Visual C++ redistributables are up to date

4. **Import errors with pytesseract**:
   - Make sure you've installed all required Python packages:
     ```
     pip install pytesseract Pillow PyMuPDF
     ```

## Manual Testing

You can test Tesseract directly from the command line:

```
"C:\Program Files\Tesseract-OCR\tesseract.exe" path/to/your/image.jpg stdout
```

This should output the extracted text if Tesseract is working correctly.

---

If you continue to experience issues, please create a detailed bug report including:
- Your operating system version
- Tesseract version
- Python version
- Error messages
- Sample image (if possible) 