import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';

const LandingPage = () => {
  return (
    <div className="page-container">
      <Navbar isLoggedIn={false} />
      
      <div className="hero-section">
        <div className="container mx-auto max-w-6xl">
          <div className="flex flex-col items-center text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-6">Healthcare Emergency Management Made Simple</h1>
            <p className="text-xl md:text-2xl mb-10 max-w-3xl">
              Access critical medical information instantly in emergencies and stay connected with healthcare providers.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Link to="/register" className="btn bg-white text-primary hover:bg-gray-100 px-8 py-3 text-lg">
                Get Started
              </Link>
              <Link to="/emergency" className="btn btn-emergency px-8 py-3 text-lg">
                Emergency Access
              </Link>
            </div>
          </div>
        </div>
      </div>
      
      <div className="py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <h2 className="text-3xl font-bold text-center mb-12">How MediVault Helps</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="feature-card">
              <div className="w-16 h-16 mb-6 bg-primary-light rounded-lg flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3">Medical Information</h3>
              <p className="text-gray-600">
                Store and access your critical medical information securely, including allergies, medications, and conditions.
              </p>
            </div>
            
            <div className="feature-card">
              <div className="w-16 h-16 mb-6 bg-primary-light rounded-lg flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3">One-Tap Emergency</h3>
              <p className="text-gray-600">
                Notify emergency services instantly with your location and critical medical information.
              </p>
            </div>
            
            <div className="feature-card">
              <div className="w-16 h-16 mb-6 bg-primary-light rounded-lg flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3">Secure & Private</h3>
              <p className="text-gray-600">
                Your medical data is encrypted and secure, only accessible to authorized healthcare providers.
              </p>
            </div>
          </div>
        </div>
      </div>
      
      <div className="bg-gray-100 py-16 px-6">
        <div className="container mx-auto max-w-6xl text-center">
          <h2 className="text-3xl font-bold mb-8">Ready to get started?</h2>
          <div className="flex justify-center">
            <Link to="/register" className="btn btn-primary px-8 py-3 text-lg">
              Create Free Account
            </Link>
          </div>
        </div>
      </div>
      
      <footer className="bg-gray-800 text-white py-10 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-6 md:mb-0">
              <h2 className="text-xl font-bold">MediVault</h2>
              <p className="text-gray-400">Healthcare Emergency Management</p>
            </div>
            <div className="flex flex-col md:flex-row gap-6 md:gap-10">
              <a href="#" className="text-gray-300 hover:text-white">About</a>
              <a href="#" className="text-gray-300 hover:text-white">Privacy</a>
              <a href="#" className="text-gray-300 hover:text-white">Terms</a>
              <a href="#" className="text-gray-300 hover:text-white">Contact</a>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-gray-700 text-center text-gray-400">
            <p>© {new Date().getFullYear()} MediVault. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage; 