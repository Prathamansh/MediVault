import os
import sys
import logging
from pathlib import Path

# Set up logging with more detailed output
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger('ocr_debug')

# Get the project root directory
current_dir = Path(__file__).parent
static_dir = current_dir / 'static' / 'test_docs'

# Make sure the test directories exist
os.makedirs(static_dir, exist_ok=True)

# Create a test text file if it doesn't exist
sample_text_path = static_dir / 'sample_prescription.txt'
if not sample_text_path.exists():
    logger.info(f"Creating sample text file at {sample_text_path}")
    with open(sample_text_path, 'w') as f:
        f.write("""
        Dr. Smith Medical Center
        Patient: John Doe
        Date: 04/15/2023
        
        Diagnosis: Seasonal allergies, mild hypertension
        
        Prescription:
        - Loratadine 10mg - Take 1 tablet daily
        - Amlodipine 5mg - Take 1 tablet in the morning
        
        Follow up in 3 months
        Dr. Jane Smith, MD
        """)

try:
    logger.info("Testing OCR availability...")
    # Try to import pytesseract to check if it's installed
    try:
        import pytesseract
        logger.info("pytesseract module is installed.")
    except ImportError:
        logger.error("pytesseract module is not installed. Install with: pip install pytesseract")
        sys.exit(1)

    # Now import our OCR service
    try:
        from app.ocr_service import setup_tesseract, extract_text
        logger.info("OCR service module imported successfully.")
    except ImportError as e:
        logger.error(f"Failed to import OCR service: {e}")
        sys.exit(1)

    # Test Tesseract configuration
    if setup_tesseract():
        try:
            version = pytesseract.get_tesseract_version()
            logger.info(f"Tesseract is configured properly. Version: {version}")
        except Exception as e:
            logger.error(f"Tesseract is configured but version check failed: {e}")
            logger.error("Tesseract might not be installed or executable not found in PATH")
    else:
        logger.error("Tesseract configuration failed. Make sure Tesseract OCR is installed.")
        logger.error("Download from: https://github.com/UB-Mannheim/tesseract/wiki")
        
        # Windows-specific help
        if sys.platform.startswith('win'):
            logger.info("On Windows, install from: https://github.com/UB-Mannheim/tesseract/wiki")
            logger.info("Then set the path in environment variable TESSERACT_PATH or edit the OCR service code.")
        
        # macOS-specific help
        elif sys.platform == 'darwin':
            logger.info("On macOS, install using: brew install tesseract")
        
        # Linux-specific help
        else:
            logger.info("On Linux, install using: sudo apt-get install tesseract-ocr")
            
    # Test AI service
    logger.info("\nTesting AI service...")
    try:
        from app.ai_service import initialize_genai, summarize_medical_text
        logger.info("AI service module imported successfully.")
        
        # Test API key availability
        gemini_api_key = os.environ.get('GEMINI_API_KEY')
        if gemini_api_key:
            logger.info("GEMINI_API_KEY environment variable is set.")
            
            # Test Gemini API initialization
            if initialize_genai(gemini_api_key):
                logger.info("Gemini API initialized successfully.")
            else:
                logger.error("Gemini API initialization failed. Check your API key.")
        else:
            logger.warning("GEMINI_API_KEY environment variable is not set.")
            logger.warning("The code will try to use a hardcoded fallback key, which might not work.")
            logger.info("Set your API key with: export GEMINI_API_KEY='your-api-key'")
        
        # Test summarization with a simple text
        logger.info("\nTesting text summarization...")
        test_text = "This is a test for the medical text summarization service. Patient John Doe has hypertension."
        result = summarize_medical_text(test_text, use_fake_data_on_error=True)
        
        if result["success"]:
            logger.info("Summarization successful!")
            logger.info(f"Summary: {result['summary'][:100]}...")
        else:
            logger.error(f"Summarization failed: {result['error']}")
            logger.info("Will fall back to rule-based summary.")
            
    except ImportError as e:
        logger.error(f"Failed to import AI service: {e}")
    except Exception as e:
        logger.error(f"Error testing AI service: {e}")
        import traceback
        traceback.print_exc()
    
    # Test file processing
    if 'extract_text' in locals():
        logger.info("\nTesting OCR file processing...")
        
        # Check if we have any sample images to test
        image_files = list(static_dir.glob('*.jpg')) + list(static_dir.glob('*.png')) + list(static_dir.glob('*.pdf'))
        
        if image_files:
            logger.info(f"Found {len(image_files)} sample image(s) for testing:")
            for img_file in image_files:
                logger.info(f"Testing OCR on: {img_file}")
                try:
                    with open(img_file, 'rb') as f:
                        ocr_result = extract_text(f)
                    
                    if ocr_result["success"]:
                        logger.info(f"OCR successful! Extracted {len(ocr_result['text'])} characters")
                        logger.info(f"First 100 chars: {ocr_result['text'][:100]}...")
                    else:
                        logger.error(f"OCR failed: {ocr_result['error']}")
                except Exception as e:
                    logger.error(f"Error processing {img_file}: {e}")
        else:
            logger.warning("No sample images found for testing. Create some sample images in static/test_docs/")
            logger.info("A simple test image with text would be sufficient for testing purposes.")
    
    logger.info("\nDebug complete!")
    logger.info("If OCR is not working, make sure Tesseract is installed and configured correctly.")
    logger.info("If AI summarization is not working, check your Gemini API key.")
    
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    import traceback
    traceback.print_exc() 