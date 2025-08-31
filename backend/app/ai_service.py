import google.generativeai as genai
import os
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('ai_service')

def initialize_genai(api_key):
    """Initialize the Gemini API with the provided API key"""
    try:
        genai.configure(api_key=api_key)
        logger.info("Gemini API initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize Gemini API: {str(e)}")
        return False

def summarize_medical_text(text, api_key=None, use_fake_data_on_error=True, max_retries=2):
    """
    Summarize medical text using Google Gemini API
    
    Args:
        text: The medical text to summarize
        api_key: Google Gemini API key (defaults to environment variable or hardcoded fallback)
        use_fake_data_on_error: Whether to use fake data if the API fails
        max_retries: Maximum number of retry attempts for API calls
        
    Returns:
        dict: Dictionary with summary and metadata
    """
    # Try to get API key from environment first
    if not api_key:
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            logger.warning("GEMINI_API_KEY environment variable not set, using fallback key")
            api_key = "AIzaSyB-b0jwOrGIzWUbRkWxw_o4gAWFE5clkX4"  # Fallback key that may not work
    
    result = {
        "summary": "",
        "success": False,
        "error": None
    }
    
    if not text or len(text.strip()) < 10:
        logger.warning("Not enough text to summarize")
        result["error"] = "Not enough text to summarize"
        return result
    
    # Try the API with retries
    for attempt in range(max_retries):
        try:
            # Initialize the Gemini API
            if not initialize_genai(api_key):
                raise Exception("Failed to initialize Gemini API")
            
            logger.info(f"Attempt {attempt+1}/{max_retries} to summarize text")
            
            # Create a model instance
            model = genai.GenerativeModel('gemini-pro')
            
            # Prepare prompt for better medical report summarization
            prompt = f"""
            Please provide a concise summary of the following medical report/document. 
            Extract and organize key information including:
            
            1. Patient information if available
            2. Diagnosis or medical conditions
            3. Test results and their significance
            4. Recommended treatments or medications
            5. Follow-up instructions
            
            Focus on the most important medical information and present it in a clear, organized format.
            If you can't identify specific information for a category, you can omit that section.
            
            MEDICAL DOCUMENT TEXT:
            {text}
            """
            
            # Generate summary
            response = model.generate_content(prompt)
            
            # Extract summary from response
            if hasattr(response, 'text'):
                result["summary"] = response.text
            else:
                # For older API versions
                result["summary"] = response.candidates[0].content.parts[0].text
            
            # Check if we got a meaningful summary
            if len(result["summary"].strip()) < 10:
                logger.warning("API returned very short summary")
                if attempt < max_retries - 1:
                    logger.info("Retrying with different prompt")
                    continue
            
            result["success"] = True
            return result
            
        except Exception as e:
            logger.error(f"Error in summarization (attempt {attempt+1}): {str(e)}")
            # Sleep before retry (exponential backoff)
            if attempt < max_retries - 1:
                sleep_time = 2 ** attempt  # 1, 2, 4, 8, etc. seconds
                logger.info(f"Waiting {sleep_time}s before retry...")
                time.sleep(sleep_time)
    
    # If we're here, all API attempts failed
    result["error"] = "Failed to generate summary using AI service after multiple attempts"
    
    # If we should use fake data on error and there's enough text to work with
    if use_fake_data_on_error and len(text.strip()) >= 10:
        logger.info("Using rule-based summary due to API failure")
        
        # Create a rule-based fake summary
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        sample_summary = generate_fallback_summary(text, lines)
        
        result["summary"] = sample_summary
        result["success"] = True
        result["error"] = "Note: This is a rule-based summary due to AI service unavailability."
        
    return result

def generate_fallback_summary(text, lines):
    """Generate a rule-based summary when the API is unavailable"""
    logger.info("Generating rule-based fallback summary")
    
    # Very basic rule-based summary generator
    summary_parts = []
    
    # Try to extract patient info if available
    patient_info = []
    for line in lines[:15]:  # Look in first few lines
        if any(term in line.lower() for term in ['patient', 'name', 'dob', 'birth', 'age', 'id', 'mr#']):
            patient_info.append(line)
    
    if patient_info:
        summary_parts.append("## Patient Information\n" + "\n".join(patient_info))
    
    # Look for diagnosis or medical conditions
    diagnosis = []
    diagnosis_section = False
    for i, line in enumerate(lines):
        lower_line = line.lower()
        
        # Check for section headers
        if any(term == lower_line.strip() for term in ['diagnosis:', 'diagnoses:', 'assessment:']):
            diagnosis_section = True
            continue
            
        # If we're in the diagnosis section, add lines until we hit another section
        if diagnosis_section:
            # Check if we've hit another section header
            if lower_line.endswith(':') and len(lower_line.strip()) < 30:
                diagnosis_section = False
                continue
                
            # Add the line if it looks like a diagnosis
            if line.strip() and not line.startswith('---'):
                diagnosis.append(line)
                
        # Look for lines that might contain diagnoses
        elif any(term in lower_line for term in ['diagnosis', 'diagnosed with', 'condition', 'assessment']):
            diagnosis.append(line)
    
    if diagnosis:
        summary_parts.append("## Diagnosis\n" + "\n".join(diagnosis))
    else:
        # Look for potential symptoms or conditions
        symptoms = []
        for line in lines:
            if any(term in line.lower() for term in ['pain', 'ache', 'discomfort', 'symptom', 'complaint']):
                symptoms.append(line)
        if symptoms:
            summary_parts.append("## Symptoms\n" + "\n".join(symptoms[:5]))
    
    # Look for medications or treatments
    medications = []
    medication_section = False
    for line in lines:
        lower_line = line.lower()
        
        # Check for medication section headers
        if any(term == lower_line.strip() for term in ['medications:', 'medication:', 'prescription:', 'prescriptions:']):
            medication_section = True
            continue
            
        # If we're in the medication section, add lines
        if medication_section:
            if lower_line.endswith(':') and len(lower_line.strip()) < 30:
                medication_section = False
                continue
                
            if line.strip() and not line.startswith('---'):
                medications.append(line)
                
        # Check for lines that might contain medication info
        elif any(term in lower_line for term in ['mg', 'mcg', 'prescription', 'rx', 'take', 'dose', 'tablet', 'capsule']):
            medications.append(line)
    
    if medications:
        summary_parts.append("## Medications\n" + "\n".join(medications))
    
    # Look for lab results
    lab_results = []
    lab_section = False
    for line in lines:
        lower_line = line.lower()
        
        # Check for lab section headers
        if any(term == lower_line.strip() for term in ['laboratory:', 'labs:', 'lab results:', 'test results:']):
            lab_section = True
            continue
            
        # If we're in the lab section, add lines
        if lab_section:
            if lower_line.endswith(':') and len(lower_line.strip()) < 30:
                lab_section = False
                continue
                
            if line.strip() and not line.startswith('---'):
                lab_results.append(line)
                
        # Check for lines that might contain lab info
        elif any(term in lower_line for term in ['test result', 'blood pressure', 'mmol', 'mg/dl', 'normal range']):
            lab_results.append(line)
    
    if lab_results:
        summary_parts.append("## Lab Results\n" + "\n".join(lab_results))
    
    # Look for follow-up information
    followup = []
    followup_section = False
    for line in lines:
        lower_line = line.lower()
        
        # Check for follow-up section headers
        if any(term == lower_line.strip() for term in ['follow-up:', 'follow up:', 'plan:']):
            followup_section = True
            continue
            
        # If we're in the follow-up section, add lines
        if followup_section:
            if lower_line.endswith(':') and len(lower_line.strip()) < 30:
                followup_section = False
                continue
                
            if line.strip() and not line.startswith('---'):
                followup.append(line)
                
        # Check for lines that might contain follow-up info
        elif any(term in lower_line for term in ['follow', 'appointment', 'visit', 'return', 'weeks', 'months']):
            followup.append(line)
    
    if followup:
        summary_parts.append("## Follow-up\n" + "\n".join(followup))
    
    # If we couldn't extract structured information, just grab a few meaningful lines
    if not summary_parts:
        important_lines = []
        for line in lines:
            if len(line) > 20 and not line.startswith('---') and not all(c.isdigit() or c.isspace() for c in line):
                important_lines.append(line)
                if len(important_lines) >= 5:
                    break
        
        if important_lines:
            summary_parts.append("## Extracted Information\n" + "\n".join(important_lines))
    
    # Add a disclaimer
    summary_parts.append("*Note: This is a rule-based summary generated when AI services were unavailable.*")
    
    return "\n\n".join(summary_parts) 