import pytesseract
import fitz  # PyMuPDF
import io
from PIL import Image
import os
import tempfile
import platform
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('ocr_service')

# Set Tesseract path based on OS
def setup_tesseract():
    """Configure Tesseract path based on operating system"""
    if platform.system() == 'Windows':
        # Default Windows path
        default_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pytesseract.pytesseract.tesseract_cmd = default_path
        
        # IMPORTANT - HARDCODED PATH - uncomment and set your actual path if needed
        # For example:
        # custom_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        # pytesseract.pytesseract.tesseract_cmd = custom_path
        # return True
        
        # Check if default path exists, otherwise try alternatives
        if not os.path.exists(default_path):
            logger.info("Default Tesseract path not found, trying alternatives")
            possible_paths = [
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                r'C:\Tesseract-OCR\tesseract.exe',
                r'C:\Users\Public\Tesseract-OCR\tesseract.exe',
                r'C:\Tesseract\tesseract.exe',
                r'C:\Users\diksh\AppData\Local\Tesseract-OCR\tesseract.exe',
                r'C:\Users\diksh\AppData\Local\Programs\Tesseract-OCR\tesseract.exe',
                # Add more potential paths if needed
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    logger.info(f"Found Tesseract at: {path}")
                    pytesseract.pytesseract.tesseract_cmd = path
                    return True
            
            # If environment variable is set, use that
            env_path = os.environ.get('TESSERACT_PATH')
            if env_path and os.path.exists(env_path):
                logger.info(f"Using Tesseract from environment variable: {env_path}")
                pytesseract.pytesseract.tesseract_cmd = env_path
                return True
                
            logger.warning("Tesseract not found in any expected location")
            logger.info("After installing Tesseract, edit this file to manually set the correct path")
            return False
        
        return True
    
    elif platform.system() == 'Darwin':  # macOS
        # Check common macOS locations
        possible_paths = [
            '/usr/local/bin/tesseract',
            '/opt/homebrew/bin/tesseract',
            '/usr/bin/tesseract'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                logger.info(f"Found Tesseract at: {path}")
                pytesseract.pytesseract.tesseract_cmd = path
                return True
        
        # If not found but presumed to be in PATH
        return True
    
    # For Linux, usually in PATH, but could check common locations
    return True

# Initialize Tesseract
tesseract_available = setup_tesseract()
if tesseract_available:
    try:
        version = pytesseract.get_tesseract_version()
        logger.info(f"Tesseract version: {version}")
    except Exception as e:
        logger.error(f"Failed to get Tesseract version: {str(e)}")
        tesseract_available = False
else:
    logger.warning("Tesseract not properly configured")

def extract_text(file_obj):
    """
    Extract text from images or PDF files
    
    Args:
        file_obj: File object opened in binary mode (rb)
        
    Returns:
        dict: Dictionary with extracted text and metadata
    """
    # Get the original filename from the file object if possible
    filename = getattr(file_obj, 'name', 'unknown')
    extension = os.path.splitext(filename)[1].lower() if filename != 'unknown' else ''
    
    result = {
        "text": "",
        "source": filename,
        "pages": 0,
        "success": False,
        "error": None
    }
    
    # Check if Tesseract is available
    if not tesseract_available:
        logger.error("Tesseract OCR is not properly configured")
        result["error"] = "Tesseract OCR not found or not configured correctly. See README-OCR-TROUBLESHOOTING.md for help."
        return result
    
    try:
        # Handle PDFs
        if extension == '.pdf':
            logger.info(f"Processing PDF file: {filename}")
            text = extract_from_pdf(file_obj)
            result["text"] = text
            
        # Handle images
        elif extension in ['.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif']:
            logger.info(f"Processing image file: {filename}")
            text = extract_from_image(file_obj)
            result["text"] = text
            
        # Unknown file type    
        else:
            logger.info(f"Treating unknown file type as image: {filename}")
            # Try to process as image by default
            text = extract_from_image(file_obj)
            result["text"] = text
            
        # Check if any text was extracted
        if not text or len(text.strip()) < 5:
            logger.warning("No significant text extracted from document")
            result["error"] = "No text could be extracted from the document. Try a clearer image or different file."
            result["success"] = False
            return result
            
        result["success"] = True
        return result
        
    except Exception as e:
        logger.error(f"OCR Error: {str(e)}")
        result["error"] = f"OCR processing error: {str(e)}"
        return result

def extract_from_pdf(file_obj):
    """Extract text from a PDF file"""
    try:
        # Create a temporary file to save the PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_file.write(file_obj.read())
            temp_path = temp_file.name
        
        try:
            # Open the PDF with PyMuPDF
            doc = fitz.open(temp_path)
            text = ""
            
            # Extract text from each page
            for page_num, page in enumerate(doc):
                logger.info(f"Processing PDF page {page_num+1}")
                page_text = page.get_text()
                text += page_text
            
            # If PyMuPDF couldn't extract text or extracted very little, try OCR
            if not text or len(text.strip()) < 20:
                logger.info("PDF text extraction yielded little text, trying OCR...")
                # Convert PDF to images and run OCR
                text = ""
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    
                    # Convert to grayscale for better OCR
                    if img.mode != 'L':
                        img = img.convert('L')
                        
                    # Use a better configuration for document OCR
                    custom_config = r'--oem 3 --psm 6'
                    page_text = pytesseract.image_to_string(img, config=custom_config)
                    text += page_text + "\n\n"
                    logger.info(f"OCR extracted {len(page_text)} characters from PDF page {page_num+1}")
            
            return text
        finally:
            # Clean up the temporary file
            try:
                os.unlink(temp_path)
            except Exception as e:
                logger.warning(f"Failed to delete temporary PDF file: {str(e)}")
    except Exception as e:
        logger.error(f"PDF extraction error: {str(e)}")
        raise Exception(f"Failed to extract text from PDF: {str(e)}")

def extract_from_image(file_obj):
    """Extract text from an image file using pytesseract"""
    try:
        # Read image data
        img_data = file_obj.read()
        
        # Open image with PIL
        image = Image.open(io.BytesIO(img_data))
        
        # Print image info for debugging
        logger.info(f"Image format: {image.format}, size: {image.size}, mode: {image.mode}")
        
        # Improve image quality for OCR
        # Convert to grayscale if color
        if image.mode != 'L':
            image = image.convert('L')
        
        # Apply some image enhancement for better OCR results
        from PIL import ImageEnhance, ImageFilter
        
        # Increase contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)
        
        # Apply slight sharpening
        image = image.filter(ImageFilter.SHARPEN)
        
        # Extract text using pytesseract with detailed config
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=custom_config)
        
        if not text or len(text.strip()) < 5:
            logger.warning("OCR yielded little or no text")
            
            # Try with different PSM mode for sparse text
            logger.info("Retrying with different PSM mode")
            custom_config = r'--oem 3 --psm 11'  # Sparse text with OSD
            text = pytesseract.image_to_string(image, config=custom_config)
        else:
            logger.info(f"OCR successful, extracted {len(text)} characters")
            
        return text
    except Exception as e:
        logger.error(f"Image OCR error: {str(e)}")
        raise Exception(f"Failed to extract text from image: {str(e)}") 