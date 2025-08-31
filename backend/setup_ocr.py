#!/usr/bin/env python
"""
MediVault OCR Setup Script
This script helps set up and test the OCR and AI services.
"""

import os
import sys
import platform
import subprocess
import tempfile
import shutil
from pathlib import Path
import webbrowser

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_step(text):
    """Print a step in the process"""
    print(f"\n>> {text}")

def check_python_version():
    """Check if Python version is compatible"""
    print_step("Checking Python version")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"⚠️  Warning: Python {version.major}.{version.minor} detected. Python 3.7+ is recommended.")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected (compatible)")
        return True

def install_requirements():
    """Install required Python packages"""
    print_step("Installing required packages")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found. Creating basic requirements file...")
        with open(requirements_file, "w") as f:
            f.write("""Flask==2.0.1
flask-cors==3.0.10
twilio==7.16.0
python-dotenv==0.19.1
Pillow==9.4.0
pytesseract==0.3.10
PyMuPDF==1.21.1
google-generativeai==0.2.0
Werkzeug==2.0.1
""")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], check=True)
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        print("   Try installing manually with: pip install -r requirements.txt")
        return False

def detect_tesseract():
    """Detect Tesseract OCR installation"""
    print_step("Detecting Tesseract OCR")
    
    # Try to import pytesseract
    try:
        import pytesseract
        print("✅ pytesseract package is installed")
    except ImportError:
        print("❌ pytesseract package is not installed")
        print("   Run: pip install pytesseract")
        return False
    
    # Check if Tesseract is in PATH
    tesseract_found = False
    tesseract_path = ""
    tesseract_version = "Unknown"
    
    system = platform.system()
    
    # Define possible paths based on OS
    if system == "Windows":
        possible_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Tesseract-OCR\tesseract.exe",
            r"C:\Users\Public\Tesseract-OCR\tesseract.exe",
        ]
        
        # Check each path
        for path in possible_paths:
            if os.path.exists(path):
                tesseract_path = path
                tesseract_found = True
                break
                
    elif system == "Darwin":  # macOS
        # Check common macOS locations
        possible_paths = [
            "/usr/local/bin/tesseract",
            "/opt/homebrew/bin/tesseract",
            "/usr/bin/tesseract"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                tesseract_path = path
                tesseract_found = True
                break
    
    elif system == "Linux":
        # Try to find tesseract in PATH
        try:
            tesseract_path = subprocess.check_output(["which", "tesseract"]).decode().strip()
            if tesseract_path:
                tesseract_found = True
        except:
            pass
    
    # Try running tesseract --version
    if tesseract_found or tesseract_path:
        try:
            version_output = subprocess.check_output([tesseract_path, "--version"]).decode()
            tesseract_version = version_output.split()[1] if len(version_output.split()) > 1 else "Unknown"
            tesseract_found = True
        except:
            # If direct path execution failed, try with pytesseract
            try:
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
                v = pytesseract.get_tesseract_version()
                tesseract_version = str(v)
                tesseract_found = True
            except:
                tesseract_found = False
    
    if tesseract_found:
        print(f"✅ Tesseract OCR detected (version {tesseract_version})")
        print(f"   Path: {tesseract_path}")
        return tesseract_path
    else:
        print("❌ Tesseract OCR not found")
        
        # Provide installation instructions based on OS
        if system == "Windows":
            print("   Download and install from: https://github.com/UB-Mannheim/tesseract/wiki")
        elif system == "Darwin":  # macOS
            print("   Install with Homebrew: brew install tesseract")
        elif system == "Linux":
            print("   Install with apt: sudo apt-get install tesseract-ocr")
            print("   Or yum: sudo yum install tesseract")
        
        return False

def check_directories():
    """Ensure required directories exist"""
    print_step("Setting up directories")
    
    base_dir = Path(__file__).parent
    required_dirs = [
        base_dir / "static",
        base_dir / "static/uploads",
        base_dir / "static/test_docs",
        base_dir / "app",
    ]
    
    for directory in required_dirs:
        if not directory.exists():
            print(f"Creating directory: {directory}")
            directory.mkdir(parents=True, exist_ok=True)
    
    print("✅ All required directories exist")
    return True

def check_sample_files():
    """Ensure sample files exist"""
    print_step("Checking sample files")
    
    base_dir = Path(__file__).parent
    sample_txt = base_dir / "static/test_docs/sample_prescription.txt"
    
    if not sample_txt.exists():
        print(f"Creating sample prescription text file")
        with open(sample_txt, "w") as f:
            f.write("""NORTHSIDE MEDICAL CENTER
123 Health Avenue, Metropolis, XY 10001
Tel: (555) 123-4567 | Fax: (555) 987-6543

PRESCRIPTION

Date: April 17, 2023
Patient Name: John Smith
DOB: 06/12/1985
Patient ID: MED78901234

DIAGNOSIS:
- Hypertension (Essential), Uncontrolled (ICD-10: I10)
- Type 2 Diabetes Mellitus (ICD-10: E11.9)
- Hyperlipidemia (ICD-10: E78.5)

MEDICATIONS:
1. Lisinopril 20mg
   Take 1 tablet by mouth once daily
   Dispense: 30 tablets
   Refill: 3 times

2. Metformin 500mg
   Take 1 tablet by mouth twice daily with meals
   Dispense: 60 tablets
   Refill: 3 times

3. Atorvastatin 40mg
   Take 1 tablet by mouth at bedtime
   Dispense: 30 tablets
   Refill: 3 times

LABS:
- HbA1c: 7.8% (Target: <7.0%)
- Blood Pressure: 142/90 mmHg (Target: <130/80 mmHg)
- LDL: 118 mg/dL (Target: <100 mg/dL)

FOLLOW-UP:
Please return to clinic in 3 months for medication review and lab work.
Schedule appointment for blood pressure check in 4 weeks.

NOTES:
Patient advised on diet and exercise. Recommended 30 minutes of moderate exercise at least 5 days per week. Advised to follow diabetic diet and reduce sodium intake.

Dr. Sarah Johnson, MD
License #: MD123456
NPI: 1234567890

Electronically signed: 04/17/2023""")
    
    print("✅ Sample text file exists")
    return True

def verify_api_key():
    """Check if Gemini API key is available"""
    print_step("Checking Gemini API key")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if api_key:
        print("✅ Gemini API key found in environment variables")
        return True
    else:
        print("⚠️  No Gemini API key found in environment variables")
        print("   Please consider setting the GEMINI_API_KEY environment variable")
        print("   Without it, the system will use a fallback rule-based summarization")
        
        # Check for hardcoded key in ai_service.py
        base_dir = Path(__file__).parent
        ai_service_path = base_dir / "app/ai_service.py"
        
        if ai_service_path.exists():
            with open(ai_service_path, "r") as f:
                content = f.read()
                if "API-KEY-GEMINI" in content:
                    print("⚠️  Using default API key from ai_service.py")
                    print("   For production use, it's recommended to use your own API key")
                    return True
        
        return False

def run_test_ocr(tesseract_path=None):
    """Run a test OCR if possible"""
    print_step("Testing OCR functionality")
    
    if not tesseract_path:
        print("⚠️  Skipping OCR test because Tesseract is not available")
        return False
    
    try:
        import pytesseract
        from PIL import Image
        
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        # Create a simple test image with text
        img = Image.new('RGB', (200, 50), color=(255, 255, 255))
        from PIL import ImageDraw, ImageFont
        d = ImageDraw.Draw(img)
        d.text((10, 10), "MediVault OCR Test", fill=(0, 0, 0))
        
        # Save to temp file
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        img.save(temp_file.name)
        
        # Run OCR
        text = pytesseract.image_to_string(Image.open(temp_file.name))
        
        # Clean up
        os.unlink(temp_file.name)
        
        if "MediVault" in text or "OCR" in text or "Test" in text:
            print(f"✅ OCR test successful! Extracted: {text.strip()}")
            return True
        else:
            print(f"⚠️  OCR test extracted text but did not find expected words.")
            print(f"   Extracted: {text.strip()}")
            return False
    except Exception as e:
        print(f"❌ OCR test failed: {e}")
        return False

def start_server():
    """Offer to start the server"""
    print_step("Starting the server")
    
    response = input("Would you like to start the Flask server now? (y/n): ").strip().lower()
    
    if response == 'y':
        base_dir = Path(__file__).parent
        app_path = base_dir / "app.py"
        
        if app_path.exists():
            print("Starting Flask server...")
            try:
                # Open browser after a delay
                def open_browser():
                    import time
                    time.sleep(2)
                    webbrowser.open('http://localhost:5000/test-ocr')
                
                import threading
                threading.Thread(target=open_browser).start()
                
                # Start server
                subprocess.run([sys.executable, str(app_path)], check=True)
                return True
            except KeyboardInterrupt:
                print("\nServer stopped")
                return True
            except Exception as e:
                print(f"❌ Error starting server: {e}")
                return False
        else:
            print(f"❌ Cannot find app.py at {app_path}")
            return False
    else:
        print("Server not started. You can start it manually with:")
        print("python app.py")
        return True

def main():
    """Main function to run all checks"""
    print_header("MediVault OCR Setup")
    
    # Run all checks
    python_ok = check_python_version()
    check_directories()
    check_sample_files()
    req_ok = install_requirements()
    tesseract_path = detect_tesseract()
    api_ok = verify_api_key()
    
    # Only run OCR test if Tesseract is available
    if tesseract_path:
        ocr_ok = run_test_ocr(tesseract_path)
    else:
        ocr_ok = False
    
    # Summarize setup results
    print_header("Setup Summary")
    
    if python_ok and req_ok and tesseract_path and api_ok and ocr_ok:
        print("✅ All checks passed! Your OCR system is ready to use.")
    elif python_ok and req_ok and tesseract_path and ocr_ok:
        print("✅ Basic OCR functionality is working.")
        print("⚠️  AI summarization may use fallback method due to missing API key.")
    elif python_ok and req_ok and tesseract_path:
        print("⚠️  OCR system is partially set up. OCR test failed.")
        print("   Please check the troubleshooting guide: README-OCR-TROUBLESHOOTING.md")
    else:
        print("❌ Setup incomplete. Please address the issues above.")
        print("   See README-OCR-TROUBLESHOOTING.md for detailed help.")
    
    # Offer to start the server
    start_server()

if __name__ == "__main__":

    main() 
