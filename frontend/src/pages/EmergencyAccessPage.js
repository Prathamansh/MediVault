import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import EmergencyPanel from '../components/EmergencyPanel';

const EmergencyAccessPage = () => {
  const [showEmergencyPanel, setShowEmergencyPanel] = useState(false);

  return (
    <div className="page-container bg-emergency">
      {showEmergencyPanel ? (
        <EmergencyPanel onClose={() => setShowEmergencyPanel(false)} />
      ) : (
        <div className="flex flex-col items-center justify-center min-h-screen px-6 py-12 text-white">
          <div className="w-full max-w-md text-center">
            <div className="w-20 h-20 mx-auto mb-8 bg-white rounded-full flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-emergency" viewBox="0 0 20 20" fill="currentColor">
                <path d="M2.93 17.07A10 10 0 1 1 17.07 2.93 10 10 0 0 1 2.93 17.07zm12.73-1.41A8 8 0 1 0 4.34 4.34a8 8 0 0 0 11.32 11.32zM9 5h2v6H9V5zm0 8h2v2H9v-2z"/>
              </svg>
            </div>
            
            <h1 className="text-3xl font-bold mb-4">Emergency Access</h1>
            <p className="text-xl mb-8">
              Access critical medical information for emergency situations
            </p>
            
            <button
              onClick={() => setShowEmergencyPanel(true)}
              className="w-full bg-white text-emergency font-bold py-4 px-6 rounded-lg text-lg mb-6 hover:bg-gray-100 transition-colors"
            >
              View Emergency Information
            </button>
            
            <p className="text-sm mb-6">
              This page provides access to critical medical information for emergency responders.
              No login required.
            </p>
            
            <div className="flex justify-center space-x-4">
              <Link to="/" className="text-white hover:underline">
                Return to Home
              </Link>
              <Link to="/login" className="text-white hover:underline">
                Login
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default EmergencyAccessPage; 