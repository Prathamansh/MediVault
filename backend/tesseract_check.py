import sys
import subprocess
import platform
import os

def check_tesseract_installed():
    """Check if Tesseract is installed and available in the PATH"""
    print("Checking Tesseract OCR installation...")
    
    try:
        if platform.system() == 'Windows':
            # On Windows, we'll check for the typical installation paths
            possible_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                r'C:\Tesseract-OCR\tesseract.exe',
                os.environ.get('TESSERACT_PATH')
            ]
            
            path_found = None
            for path in possible_paths:
                if path and os.path.exists(path):
                    path_found = path
                    break
            
            if path_found:
                print(f"✅ Tesseract found at: {path_found}")
                
                # Try to get version
                try:
                    result = subprocess.run([path_found, "--version"], capture_output=True, text=True)
                    print(f"Version information: {result.stdout.splitlines()[0]}")
                except:
                    print("Could not get version information, but executable exists.")
                    
                return True
            else:
                print("❌ Tesseract not found in standard locations.")
                return False
        else:
            # On Unix-like systems, we can try to run the tesseract command
            try:
                result = subprocess.run(["tesseract", "--version"], capture_output=True, text=True)
                print(f"✅ Tesseract is installed. Version: {result.stdout.splitlines()[0]}")
                return True
            except FileNotFoundError:
                print("❌ Tesseract command not found.")
                return False
    except Exception as e:
        print(f"❌ Error checking Tesseract: {e}")
        return False

def provide_installation_instructions():
    """Provide OS-specific instructions for installing Tesseract"""
    print("\n=== Tesseract OCR Installation Instructions ===\n")
    
    if platform.system() == 'Windows':
        print("Windows Installation:")
        print("1. Download the installer from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Run the installer and complete the installation process")
        print("3. Add Tesseract to your PATH or set the TESSERACT_PATH environment variable")
        print("   - Right-click on 'This PC' -> Properties -> Advanced system settings -> Environment Variables")
        print("   - Add a new variable TESSERACT_PATH with the path to tesseract.exe")
        print("   - Example: C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
        print("\nAlternatively, edit ocr_service.py to set the correct path on line 26.")
    
    elif platform.system() == 'Darwin':  # macOS
        print("macOS Installation:")
        print("1. Install Homebrew if you don't have it: https://brew.sh/")
        print("2. Run: brew install tesseract")
        print("3. Verify installation with: tesseract --version")
    
    else:  # Linux
        print("Linux Installation:")
        print("Ubuntu/Debian: sudo apt-get install tesseract-ocr")
        print("Fedora: sudo dnf install tesseract")
        print("Arch Linux: sudo pacman -S tesseract")
        print("\nVerify installation with: tesseract --version")
    
    print("\n=== Python Dependencies ===")
    print("Install required Python packages:")
    print("pip install pytesseract Pillow PyMuPDF google-generativeai")

def check_python_dependencies():
    """Check if the required Python packages are installed"""
    print("\nChecking Python dependencies...")
    
    dependencies = ['pytesseract', 'PIL', 'fitz', 'google.generativeai']
    missing = []
    
    for dep in dependencies:
        try:
            if dep == 'PIL':
                __import__('PIL.Image')
            elif dep == 'fitz':
                __import__('fitz')
            else:
                __import__(dep)
            print(f"✅ {dep} is installed")
        except ImportError:
            missing.append(dep)
            print(f"❌ {dep} is missing")
    
    if missing:
        print("\nInstall missing dependencies with:")
        if 'PIL' in missing:
            missing.remove('PIL')
            missing.append('Pillow')
        if 'fitz' in missing:
            missing.remove('fitz')
            missing.append('PyMuPDF')
        install_cmd = "pip install " + " ".join(missing)
        print(install_cmd)

if __name__ == "__main__":
    print("=== Tesseract OCR Setup Checker ===\n")
    
    tesseract_installed = check_tesseract_installed()
    check_python_dependencies()
    
    if not tesseract_installed:
        provide_installation_instructions()
    
    print("\n=== Check Complete ===")
    if tesseract_installed:
        print("Tesseract OCR appears to be installed correctly!")
        print("If you're still having issues with OCR, check that:")
        print("1. The Tesseract language data files are correctly installed")
        print("2. You have proper permissions to execute Tesseract")
        print("3. If using a custom path, ensure it's correctly set in the code or environment")
    else:
        print("Tesseract OCR needs to be installed for the OCR feature to work.")
        print("Follow the installation instructions above to get started.") 