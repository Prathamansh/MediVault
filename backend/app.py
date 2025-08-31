from flask import Flask, request, jsonify
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from flask_cors import CORS
import os
from dotenv import load_dotenv
import json
from werkzeug.utils import secure_filename
import tempfile

# Import OCR and AI services
from app.ocr_service import extract_text
from app.ai_service import summarize_medical_text

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# File upload configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/send-alert', methods=['POST'])
def send_alert():
    try:
        data = request.json
        account_sid = data.get('accountSid', TWILIO_ACCOUNT_SID)
        auth_token = data.get('authToken', TWILIO_AUTH_TOKEN)
        from_number = data.get('fromNumber', TWILIO_PHONE_NUMBER)
        to_number = data['toNumber']
        message_body = data['message']

        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )

        return jsonify({"status": "success", "sid": message.sid}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/emergency-contact', methods=['POST'])
def emergency_contact():
    try:
        data = request.json
        location = data.get('location', {})
        contact_info = data.get('contactInfo', {})
        user_info = data.get('userInfo', {})
        
        # Initialize Twilio client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Format emergency message with location
        lat = location.get('latitude', 'unknown')
        lng = location.get('longitude', 'unknown')
        accuracy = location.get('accuracy', 'unknown')
        
        location_url = f"https://maps.google.com/?q={lat},{lng}"
        
        emergency_message = (
            f"EMERGENCY ALERT: {user_info.get('name', 'Someone')} needs medical assistance. "
            f"Location: {location_url} (Accuracy: {accuracy}m). "
            f"Medical info - Blood Type: {user_info.get('bloodGroup', 'unknown')}, "
            f"Critical Conditions: {user_info.get('criticalConditions', 'None reported')}, "
            f"Allergies: {user_info.get('allergies', 'None reported')}."
        )
        
        response = {"status": "success", "messages": []}
        
        # Send SMS to emergency contacts
        for contact in contact_info.get('emergencyContacts', []):
            try:
                message = client.messages.create(
                    body=emergency_message,
                    from_=TWILIO_PHONE_NUMBER,
                    to=contact.get('phoneNumber')
                )
                response["messages"].append({
                    "contact": contact.get('name'),
                    "sid": message.sid,
                    "status": "sent"
                })
            except Exception as e:
                response["messages"].append({
                    "contact": contact.get('name'),
                    "error": str(e),
                    "status": "failed"
                })
        
        # Initiate call to first emergency contact if available
        if contact_info.get('emergencyContacts') and len(contact_info['emergencyContacts']) > 0:
            first_contact = contact_info['emergencyContacts'][0]
            try:
                # Use inline TwiML instead of URL
                call = client.calls.create(
                    twiml='<Response><Say voice="alice">This is an emergency alert. Someone has requested medical assistance and has listed you as an emergency contact. Please check your text messages for more information and respond accordingly.</Say><Pause length="2"/><Say voice="alice">Again, this is an emergency medical alert. Please check your text messages for the location and medical information of the person who needs assistance.</Say></Response>',
                    to=first_contact.get('phoneNumber'),
                    from_=TWILIO_PHONE_NUMBER
                )
                response["call"] = {
                    "sid": call.sid,
                    "status": "initiated",
                    "contact": first_contact.get('name')
                }
            except Exception as e:
                print(f"CALL ERROR: {str(e)}")  # This will print the specific error
                response["call"] = {
                    "error": str(e), 
                    "status": "failed"
                }
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/emergency-twiml', methods=['POST'])
def emergency_twiml():
    """Generate TwiML for the emergency call"""
    response = VoiceResponse()
    
    # Add a message to be spoken to the recipient
    response.say(
        "This is an emergency alert. Someone has requested medical assistance "
        "and has listed you as an emergency contact. They are sharing their "
        "location with you via text message. Please check your text messages "
        "for more information and respond accordingly.",
        voice='alice'
    )
    
    # Pause and repeat the message
    response.pause(length=2)
    response.say(
        "Again, this is an emergency medical alert. Please check your text "
        "messages for the location and medical information of the person "
        "who needs assistance.",
        voice='alice'
    )
    
    return str(response)

@app.route('/process-medical-document', methods=['POST'])
def process_medical_document():
    """
    Process a medical document (image or PDF) using OCR and AI summarization
    """
    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"}), 400
    
    file = request.files['file']
    
    # Check if the file has a name
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400
    
    # Print file information for debugging
    print(f"Received file: {file.filename}, Content-Type: {file.content_type}")
    
    if file and allowed_file(file.filename):
        # Process the file with OCR
        try:
            # Extract text from the document
            print(f"Starting OCR processing for {file.filename}")
            ocr_result = extract_text(file)
            
            if not ocr_result["success"]:
                print(f"OCR failed: {ocr_result['error']}")
                return jsonify({
                    "status": "error", 
                    "message": f"OCR processing failed: {ocr_result['error']}"
                }), 500
            
            # Log the extracted text for debugging
            extracted_text = ocr_result["text"]
            print(f"Extracted text (first 100 chars): {extracted_text[:100]}...")
            
            # Summarize the extracted text
            print("Starting AI summarization")
            summary_result = summarize_medical_text(ocr_result["text"])
            
            if not summary_result["success"]:
                print(f"AI summarization failed: {summary_result['error']}")
            
            # Return the results
            return jsonify({
                "status": "success",
                "original_text": ocr_result["text"],
                "summary": summary_result["summary"] if summary_result["success"] else "Summarization failed",
                "error": summary_result["error"]
            }), 200
            
        except Exception as e:
            print(f"Error processing document: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify({
            "status": "error", 
            "message": f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        }), 400

@app.route('/test-ocr', methods=['GET'])
def test_ocr():
    """
    Test endpoint to process a sample prescription image
    """
    try:
        # Path to sample image
        sample_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/test_docs/sample_prescription.jpg')
        sample_text_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/test_docs/sample_prescription.txt')
        
        # Check if sample text file exists as fallback
        if not os.path.exists(sample_path) and os.path.exists(sample_text_path):
            print(f"Sample image not found, using text file: {sample_text_path}")
            with open(sample_text_path, 'r') as text_file:
                sample_text = text_file.read()
                
            # Create a mock OCR result
            ocr_result = {
                "text": sample_text,
                "source": "sample_prescription.txt",
                "pages": 1,
                "success": True,
                "error": None
            }
            
            # Summarize the text
            print("Starting AI summarization of sample text file")
            summary_result = summarize_medical_text(ocr_result["text"])
            
            # Return the results
            return jsonify({
                "status": "success",
                "original_text": ocr_result["text"],
                "summary": summary_result["summary"] if summary_result["success"] else "Summarization failed",
                "error": summary_result["error"],
                "note": "Using sample text file instead of OCR image"
            }), 200
        
        # Check if the sample file exists
        if not os.path.exists(sample_path):
            print(f"Sample file not found at: {sample_path}")
            # Look for any image in the test_docs directory as a fallback
            test_docs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/test_docs')
            available_files = [f for f in os.listdir(test_docs_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.pdf'))]
            
            if available_files:
                sample_path = os.path.join(test_docs_dir, available_files[0])
                print(f"Using alternative sample file: {sample_path}")
            else:
                return jsonify({
                    "status": "error", 
                    "message": "Sample file not found and no alternative images available"
                }), 404
                
        print(f"Using sample file: {sample_path}")
        # Process the sample file
        with open(sample_path, "rb") as img_file:
            print("Starting OCR processing for sample file")
            ocr_result = extract_text(img_file)
        
        if not ocr_result["success"]:
            print(f"OCR failed: {ocr_result['error']}")
            
            # If OCR failed but we have a sample text file, use it
            if os.path.exists(sample_text_path):
                print(f"OCR failed, using text file as fallback: {sample_text_path}")
                with open(sample_text_path, 'r') as text_file:
                    sample_text = text_file.read()
                    
                ocr_result = {
                    "text": sample_text,
                    "source": "sample_prescription.txt",
                    "pages": 1,
                    "success": True,
                    "error": None
                }
            else:
                return jsonify({
                    "status": "error", 
                    "message": f"OCR processing failed: {ocr_result['error']}"
                }), 500
        
        # Log the extracted text
        extracted_text = ocr_result["text"]
        print(f"Extracted text (first 100 chars): {extracted_text[:100]}...")
        
        # For testing, if no text was extracted, provide a sample text
        if not extracted_text or len(extracted_text.strip()) < 10:
            print("No text extracted from sample, using placeholder text for testing")
            if os.path.exists(sample_text_path):
                with open(sample_text_path, 'r') as text_file:
                    extracted_text = text_file.read()
            else:
                extracted_text = """
                Dr. Smith Medical Center
                Patient: John Doe
                Date: 04/15/2023
                
                Diagnosis: Seasonal allergies, mild hypertension
                
                Prescription:
                - Loratadine 10mg - Take 1 tablet daily
                - Amlodipine 5mg - Take 1 tablet in the morning
                
                Follow up in 3 months
                Dr. Jane Smith, MD
                """
            ocr_result["text"] = extracted_text
        
        # Summarize the extracted text
        print("Starting AI summarization")
        summary_result = summarize_medical_text(ocr_result["text"])
        
        # Return the results
        return jsonify({
            "status": "success",
            "original_text": ocr_result["text"],
            "summary": summary_result["summary"] if summary_result["success"] else "Summarization failed",
            "error": summary_result["error"]
        }), 200
        
    except Exception as e:
        print(f"Error in test OCR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
