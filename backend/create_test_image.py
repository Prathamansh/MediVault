from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

# Create a test image with medical text that can be used for OCR testing
def create_test_medical_image():
    # Create output directory if it doesn't exist
    output_dir = Path(__file__).parent / 'static' / 'test_docs'
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = output_dir / 'test_medical_report.png'
    
    # Create a white background image
    width, height = 800, 1000
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    
    # Get a drawing context
    draw = ImageDraw.Draw(image)
    
    # Try to use a default font available on most systems
    try:
        # Try to load Arial or a similar font
        font_path = None
        
        # Windows common fonts
        windows_fonts = [
            "C:\\Windows\\Fonts\\arial.ttf",
            "C:\\Windows\\Fonts\\times.ttf",
            "C:\\Windows\\Fonts\\calibri.ttf"
        ]
        
        # Check if any of these fonts exist
        for f in windows_fonts:
            if os.path.exists(f):
                font_path = f
                break
        
        # If no font found, use default
        if font_path:
            title_font = ImageFont.truetype(font_path, 24)
            header_font = ImageFont.truetype(font_path, 16)
            body_font = ImageFont.truetype(font_path, 14)
        else:
            # Use default PIL font if TrueType not available
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
            
    except Exception as e:
        print(f"Error loading font: {e}")
        # Use default PIL font if TrueType not available
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
    
    # Add medical report content
    draw.text((50, 50), "MEDICAL REPORT", font=title_font, fill=(0, 0, 0))
    draw.text((50, 80), "PATIENT INFORMATION", font=header_font, fill=(0, 0, 0))
    draw.text((50, 110), "Name: John Smith", font=body_font, fill=(0, 0, 0))
    draw.text((50, 130), "DOB: 01/15/1980", font=body_font, fill=(0, 0, 0))
    draw.text((50, 150), "Medical Record #: 12345678", font=body_font, fill=(0, 0, 0))
    draw.text((50, 170), "Date of Visit: 06/12/2023", font=body_font, fill=(0, 0, 0))
    
    draw.text((50, 210), "VITAL SIGNS", font=header_font, fill=(0, 0, 0))
    draw.text((50, 240), "Blood Pressure: 120/80 mmHg", font=body_font, fill=(0, 0, 0))
    draw.text((50, 260), "Heart Rate: 72 bpm", font=body_font, fill=(0, 0, 0))
    draw.text((50, 280), "Respiratory Rate: 16 breaths/min", font=body_font, fill=(0, 0, 0))
    draw.text((50, 300), "Temperature: 98.6°F (37°C)", font=body_font, fill=(0, 0, 0))
    draw.text((50, 320), "Oxygen Saturation: 98%", font=body_font, fill=(0, 0, 0))
    
    draw.text((50, 360), "DIAGNOSIS", font=header_font, fill=(0, 0, 0))
    draw.text((50, 390), "Primary: Hypertension (I10)", font=body_font, fill=(0, 0, 0))
    draw.text((50, 410), "Secondary: Type 2 Diabetes Mellitus (E11.9)", font=body_font, fill=(0, 0, 0))
    
    draw.text((50, 450), "MEDICATIONS", font=header_font, fill=(0, 0, 0))
    draw.text((50, 480), "1. Lisinopril 10mg - Take 1 tablet daily", font=body_font, fill=(0, 0, 0))
    draw.text((50, 500), "2. Metformin 500mg - Take 1 tablet twice daily with meals", font=body_font, fill=(0, 0, 0))
    draw.text((50, 520), "3. Atorvastatin 20mg - Take 1 tablet at bedtime", font=body_font, fill=(0, 0, 0))
    
    draw.text((50, 560), "LABORATORY RESULTS", font=header_font, fill=(0, 0, 0))
    draw.text((50, 590), "Glucose: 126 mg/dL (High)", font=body_font, fill=(0, 0, 0))
    draw.text((50, 610), "HbA1c: 7.2% (High)", font=body_font, fill=(0, 0, 0))
    draw.text((50, 630), "Total Cholesterol: 210 mg/dL (High)", font=body_font, fill=(0, 0, 0))
    draw.text((50, 650), "LDL: 130 mg/dL (High)", font=body_font, fill=(0, 0, 0))
    draw.text((50, 670), "HDL: 45 mg/dL (Normal)", font=body_font, fill=(0, 0, 0))
    draw.text((50, 690), "Triglycerides: 150 mg/dL (Borderline High)", font=body_font, fill=(0, 0, 0))
    
    draw.text((50, 730), "RECOMMENDATIONS", font=header_font, fill=(0, 0, 0))
    draw.text((50, 760), "1. Follow low-sodium, diabetic diet", font=body_font, fill=(0, 0, 0))
    draw.text((50, 780), "2. Exercise 30 minutes daily, 5 days per week", font=body_font, fill=(0, 0, 0))
    draw.text((50, 800), "3. Monitor blood glucose levels twice daily", font=body_font, fill=(0, 0, 0))
    draw.text((50, 820), "4. Schedule follow-up appointment in 3 months", font=body_font, fill=(0, 0, 0))
    
    draw.text((50, 860), "SIGNATURE", font=header_font, fill=(0, 0, 0))
    draw.text((50, 890), "Dr. Jane Williams, MD", font=body_font, fill=(0, 0, 0))
    draw.text((50, 910), "License #: MD12345", font=body_font, fill=(0, 0, 0))
    draw.text((50, 930), "Date: 06/12/2023", font=body_font, fill=(0, 0, 0))
    
    # Draw a border
    draw.rectangle([(20, 20), (width-20, height-20)], outline=(0, 0, 0), width=2)
    
    # Save the image
    image.save(output_path, format='PNG')
    print(f"Test medical image created at: {output_path}")
    return output_path

if __name__ == "__main__":
    print("Creating test medical image for OCR testing...")
    image_path = create_test_medical_image()
    print(f"Test image created successfully at: {image_path}")
    print("You can now use this image to test the OCR functionality.")
    print("Run the following to test it:")
    print("python ocr_debug.py") 