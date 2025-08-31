# MediVault - Medical Records Portal

MediVault is a comprehensive application for securely storing and accessing medical information, with advanced features for emergency situations and medical document analysis.

## Key Features

### 1. Core Functionality
- **User Authentication**: Registration and login functionality
- **Medical Information Storage**: Store blood type, allergies, and other important health information
- **Appointment Management**: Track upcoming doctor appointments
- **Medical Records**: View and manage your medical files

### 2. Emergency Features
- **Emergency Access**: Quick access to critical information in emergency situations
- **Twilio Integration**: Automated emergency calls and SMS with location sharing
- **Location Sharing**: Automatically includes your current location in emergency notifications

### 3. Medical Document Analysis
- **OCR Processing**: Extract text from medical documents (prescriptions, lab reports, etc.)
- **AI Summarization**: Generate concise summaries of medical documents using Google Gemini AI
- **Document Management**: Upload and process various medical files (PDF, JPG, PNG)

## Running the Application

### Frontend
Simply open the `index.html` file in your browser to access the launcher page.

### Backend
The backend provides API services for emergency notifications and document processing:

```
cd backend
pip install -r requirements.txt
python app.py
```

## Setup Instructions

### Twilio Emergency Feature
See [README-TWILIO.md](README-TWILIO.md) for detailed instructions on setting up the emergency calling and SMS feature.

### OCR and AI Document Processing
See [backend/README-OCR.md](backend/README-OCR.md) for instructions on setting up the document processing features.

## Technical Details

- **Frontend**: HTML5, CSS3, JavaScript with TailwindCSS
- **Backend**: Python Flask API server
- **Storage**: Client-side storage using localStorage (data is stored in the browser)
- **APIs**: Twilio for communication, Google Gemini for AI processing
- **OCR**: Tesseract for text extraction from images and PDFs

## Pages

- **Login**: User authentication
- **Register**: Create a new account
- **Dashboard**: Main user interface with medical information
- **Emergency**: Quick access to critical medical information

## Notes

- This is a demonstration application
- For a production application, a more secure authentication and storage solution would be necessary
- The Twilio and Google API keys included are for demonstration purposes and should be replaced with your own 