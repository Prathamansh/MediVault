import React, { useState, useEffect } from 'react';
import axios from 'axios';

const EmergencyPage = () => {
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState({ show: false, message: '', type: '' });
  const [reportData, setReportData] = useState(null);
  const [userData, setUserData] = useState(null);
  const [location, setLocation] = useState({
    latitude: 37.7749,
    longitude: -122.4194,
    accuracy: 100
  });

  useEffect(() => {
    // Load user data from localStorage
    const storedUserData = JSON.parse(localStorage.getItem('medivault_user_data') || '{}');
    setUserData(storedUserData);
    
    // Try to get location if available
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude, 
            accuracy: position.coords.accuracy
          });
        },
        (error) => {
          console.error('Error getting location:', error);
        }
      );
    }
  }, []);

  const handleEmergency = async () => {
    setLoading(true);
    try {
      // Gather user information and emergency contacts
      const emergencyInfo = userData?.emergencyInfo || {};
      
      // Prepare user info for emergency message
      const userInfo = {
        name: `${userData?.firstName || ''} ${userData?.lastName || ''}`.trim() || 'Unknown User',
        bloodGroup: emergencyInfo.bloodGroup || 'Unknown',
        criticalConditions: emergencyInfo.criticalIllnesses || 'None reported',
        allergies: emergencyInfo.allergies || 'None reported'
      };
      
      // Make API call to emergency contact endpoint
      const response = await axios.post('http://localhost:5000/emergency-contact', {
        location,
        contactInfo: {
          emergencyContacts: emergencyInfo.emergencyContacts || []
        },
        userInfo
      });

      // Set report data for display
      setReportData({
        location,
        timestamp: new Date().toISOString(),
        status: response.data.status,
        messagesSent: response.data.messages?.length || 0,
        callInitiated: !!response.data.call
      });
      
      setNotification({
        show: true,
        message: 'Emergency services and contacts have been notified!',
        type: 'success'
      });

    } catch (error) {
      console.error('Error notifying emergency services:', error);
      setNotification({
        show: true,
        message: 'Failed to notify emergency services. Please try again or call emergency services directly.',
        type: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleAIVoiceAnalysis = async () => {
    setLoading(true);
    try {
      // Mock API call to AI/ML voice analysis service
      const response = await axios.get('/ai/emergency-voice', {
        params: { userId: 'user123' }
      });

      setReportData({
        ...reportData,
        aiAnalysis: response.data
      });

      setNotification({
        show: true,
        message: 'Voice analysis complete!',
        type: 'success'
      });

    } catch (error) {
      console.error('Error with AI voice analysis:', error);
      setNotification({
        show: true,
        message: 'Failed to analyze voice data. Please try again.',
        type: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="py-6">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Emergency Assistance</h1>

      {notification.show && (
        <div className={`p-4 mb-6 rounded-lg ${notification.type === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
          {notification.message}
        </div>
      )}

      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Trigger Emergency Response</h2>
        <p className="mb-6 text-gray-600">In case of medical emergency, press the button below to notify emergency services with your location and send alerts to your emergency contacts.</p>
        
        <div className="flex flex-col md:flex-row gap-4">
          <button
            className="btn btn-emergency flex items-center justify-center"
            onClick={handleEmergency}
            disabled={loading}
          >
            {loading ? (
              <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            )}
            Notify Emergency Services
          </button>
          
          <button
            className="btn btn-primary flex items-center justify-center"
            onClick={handleAIVoiceAnalysis}
            disabled={loading}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
            </svg>
            Voice Analysis
          </button>
        </div>
      </div>

      {reportData && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Emergency Report</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-medium text-gray-700 mb-2">Location Data</h3>
              <p><span className="font-medium">Latitude:</span> {reportData.location?.latitude}</p>
              <p><span className="font-medium">Longitude:</span> {reportData.location?.longitude}</p>
              <p><span className="font-medium">Time Reported:</span> {new Date(reportData.timestamp).toLocaleString()}</p>
              
              {reportData.messagesSent > 0 && (
                <p className="mt-2"><span className="font-medium">SMS Alerts:</span> {reportData.messagesSent} contact(s) notified</p>
              )}
              
              {reportData.callInitiated && (
                <p className="mt-2"><span className="font-medium">Emergency Call:</span> Initiated</p>
              )}
            </div>
            
            {reportData.aiAnalysis && (
              <div>
                <h3 className="font-medium text-gray-700 mb-2">AI Voice Analysis</h3>
                <p><span className="font-medium">Stress Level:</span> {reportData.aiAnalysis.stressLevel || 'Medium'}</p>
                <p><span className="font-medium">Emergency Type:</span> {reportData.aiAnalysis.emergencyType || 'Medical'}</p>
                <p><span className="font-medium">Recommendation:</span> {reportData.aiAnalysis.recommendation || 'Immediate medical assistance recommended'}</p>
              </div>
            )}
          </div>
        </div>
      )}
      
      <div className="mt-6">
        <h2 className="text-xl font-semibold mb-4">Your Emergency Contacts</h2>
        <div className="card">
          {userData?.emergencyInfo?.emergencyContacts && userData.emergencyInfo.emergencyContacts.length > 0 ? (
            <div className="divide-y divide-gray-200">
              {userData.emergencyInfo.emergencyContacts.map((contact, index) => (
                <div key={index} className="py-3 first:pt-0 last:pb-0">
                  <h3 className="font-medium">{contact.name}</h3>
                  <p className="text-gray-600">{contact.relationship || 'Contact'}</p>
                  <p className="font-medium">{contact.phoneNumber}</p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-600">No emergency contacts configured. Please update your profile to add emergency contacts.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default EmergencyPage; 