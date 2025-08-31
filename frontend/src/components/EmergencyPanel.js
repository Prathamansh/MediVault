import React, { useState } from 'react';
import axios from 'axios';

const EmergencyPanel = ({ onClose }) => {
  const [loading, setLoading] = useState(false);
  const [messageSent, setMessageSent] = useState(false);

  // Mock patient data - in a real app, this would be fetched from a public endpoint
  const patientInfo = {
    bloodGroup: 'O+',
    criticalConditions: ['Diabetes Type 2', 'Hypertension'],
    allergies: ['Penicillin', 'Shellfish'],
    emergencyContact: '+1 (555) 987-6543'
  };

  const handleEmergencyCall = async () => {
    setLoading(true);
    try {
      // Get current location
      const position = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject, {
          enableHighAccuracy: true,
          timeout: 5000,
          maximumAge: 0
        });
      });

      const location = {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
        accuracy: position.coords.accuracy
      };

      // In a real app, this would call your backend API
      // Mock API call for demo purposes
      // await axios.post('/api/emergency/notify', {
      //   location,
      //   contactNumber: patientInfo.emergencyContact
      // });

      // For demo, just simulate a successful API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setMessageSent(true);
    } catch (error) {
      console.error('Error sending emergency notification:', error);
      alert('Failed to send emergency notification. Please try calling emergency services directly.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="emergency-panel">
      <div className="emergency-panel-header">
        <h1 className="text-2xl font-bold text-emergency">Emergency Information</h1>
        <button 
          onClick={onClose}
          className="text-gray-500 hover:text-gray-700"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Critical Medical Information</h2>
          
          <div className="space-y-4">
            <div>
              <h3 className="font-medium text-gray-700">Blood Group</h3>
              <p className="text-2xl font-bold text-emergency">{patientInfo.bloodGroup}</p>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-700">Critical Conditions</h3>
              <ul className="list-disc pl-5 mt-2">
                {patientInfo.criticalConditions.map((condition, index) => (
                  <li key={index} className="text-gray-800">{condition}</li>
                ))}
              </ul>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-700">Allergies</h3>
              <ul className="list-disc pl-5 mt-2">
                {patientInfo.allergies.map((allergy, index) => (
                  <li key={index} className="text-gray-800">{allergy}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
        
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Emergency Contact</h2>
          
          <p className="text-gray-700 mb-6">
            Notify emergency services and send your current location with a single tap:
          </p>
          
          <button
            className="w-full btn btn-emergency flex items-center justify-center text-lg py-4"
            onClick={handleEmergencyCall}
            disabled={loading || messageSent}
          >
            {loading ? (
              <>
                <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Sending...
              </>
            ) : messageSent ? (
              <>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Help is on the way
              </>
            ) : (
              <>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
                </svg>
                Call Emergency Services
              </>
            )}
          </button>
          
          <div className="mt-6 text-center text-sm text-gray-600">
            {messageSent && 'Emergency services have been notified of your location.'}
          </div>
        </div>
      </div>
    </div>
  );
};

export default EmergencyPanel; 