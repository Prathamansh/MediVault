import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

const RegisterPage = ({ onLogin }) => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
    bloodType: '',
    allergies: '',
    conditions: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [step, setStep] = useState(1); // Step 1: Account, Step 2: Medical Info
  
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const validateStep1 = () => {
    if (!formData.firstName || !formData.lastName || !formData.email || !formData.password) {
      setError('All fields are required');
      return false;
    }
    
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return false;
    }
    
    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters');
      return false;
    }
    
    return true;
  };

  const handleNextStep = () => {
    setError('');
    
    if (validateStep1()) {
      setStep(2);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // In a real app, this would be an API call to your register endpoint
      // Mock registration for demo
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Create the user account
      onLogin({
        id: '456',
        name: `${formData.firstName} ${formData.lastName}`,
        email: formData.email,
        // Store medical info
        medicalInfo: {
          bloodType: formData.bloodType,
          allergies: formData.allergies ? formData.allergies.split(',').map(a => a.trim()) : [],
          conditions: formData.conditions ? formData.conditions.split(',').map(c => c.trim()) : []
        }
      });
      
      // Redirect to dashboard
      navigate('/dashboard');
    } catch (err) {
      setError('An error occurred during registration. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <Navbar isLoggedIn={false} />
      
      <div className="flex-1 flex items-center justify-center px-6 py-12">
        <div className="w-full max-w-md">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800">Create Your Account</h1>
            <p className="text-gray-600 mt-2">
              {step === 1 
                ? 'Sign up for MediVault to manage your healthcare information'
                : 'Add your medical information for emergency situations'
              }
            </p>
          </div>
          
          {error && (
            <div className="bg-red-100 text-red-800 p-4 rounded-lg mb-6">
              {error}
            </div>
          )}
          
          <div className="mb-6">
            <div className="w-full bg-gray-200 h-2 rounded-full overflow-hidden">
              <div 
                className="bg-primary h-full transition-all duration-300"
                style={{ width: step === 1 ? '50%' : '100%' }}
              ></div>
            </div>
            <div className="flex justify-between mt-2 text-sm text-gray-600">
              <span className={step === 1 ? 'font-medium text-primary' : ''}>Account</span>
              <span className={step === 2 ? 'font-medium text-primary' : ''}>Medical Information</span>
            </div>
          </div>
          
          <form onSubmit={step === 1 ? handleNextStep : handleSubmit} className="card">
            {step === 1 ? (
              /* Step 1: Account Information */
              <>
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div>
                    <label htmlFor="firstName" className="form-label">First Name</label>
                    <input
                      id="firstName"
                      name="firstName"
                      type="text"
                      required
                      className="form-input"
                      value={formData.firstName}
                      onChange={handleChange}
                    />
                  </div>
                  <div>
                    <label htmlFor="lastName" className="form-label">Last Name</label>
                    <input
                      id="lastName"
                      name="lastName"
                      type="text"
                      required
                      className="form-input"
                      value={formData.lastName}
                      onChange={handleChange}
                    />
                  </div>
                </div>
                
                <div className="mb-6">
                  <label htmlFor="email" className="form-label">Email Address</label>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    required
                    className="form-input"
                    placeholder="you@example.com"
                    value={formData.email}
                    onChange={handleChange}
                  />
                </div>
                
                <div className="mb-6">
                  <label htmlFor="password" className="form-label">Password</label>
                  <input
                    id="password"
                    name="password"
                    type="password"
                    required
                    className="form-input"
                    placeholder="••••••••"
                    value={formData.password}
                    onChange={handleChange}
                  />
                </div>
                
                <div className="mb-6">
                  <label htmlFor="confirmPassword" className="form-label">Confirm Password</label>
                  <input
                    id="confirmPassword"
                    name="confirmPassword"
                    type="password"
                    required
                    className="form-input"
                    placeholder="••••••••"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                  />
                </div>
              </>
            ) : (
              /* Step 2: Medical Information */
              <>
                <div className="mb-6">
                  <label htmlFor="bloodType" className="form-label">Blood Type</label>
                  <select
                    id="bloodType"
                    name="bloodType"
                    className="form-input"
                    value={formData.bloodType}
                    onChange={handleChange}
                  >
                    <option value="">Select Blood Type</option>
                    <option value="A+">A+</option>
                    <option value="A-">A-</option>
                    <option value="B+">B+</option>
                    <option value="B-">B-</option>
                    <option value="AB+">AB+</option>
                    <option value="AB-">AB-</option>
                    <option value="O+">O+</option>
                    <option value="O-">O-</option>
                  </select>
                </div>
                
                <div className="mb-6">
                  <label htmlFor="allergies" className="form-label">Allergies (comma separated)</label>
                  <input
                    id="allergies"
                    name="allergies"
                    type="text"
                    className="form-input"
                    placeholder="Penicillin, Peanuts, Shellfish"
                    value={formData.allergies}
                    onChange={handleChange}
                  />
                </div>
                
                <div className="mb-6">
                  <label htmlFor="conditions" className="form-label">Medical Conditions (comma separated)</label>
                  <textarea
                    id="conditions"
                    name="conditions"
                    rows="3"
                    className="form-input"
                    placeholder="Diabetes, Hypertension, Asthma"
                    value={formData.conditions}
                    onChange={handleChange}
                  ></textarea>
                </div>
              </>
            )}
            
            <div className="flex justify-between items-center mb-6">
              {step === 2 && (
                <button
                  type="button"
                  className="btn bg-gray-200 text-gray-800 hover:bg-gray-300"
                  onClick={() => setStep(1)}
                >
                  Back
                </button>
              )}
              
              <button
                type={step === 1 ? 'button' : 'submit'}
                className={`btn btn-primary ${step === 1 ? 'ml-auto' : ''}`}
                onClick={step === 1 ? handleNextStep : undefined}
                disabled={loading}
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Creating Account...
                  </div>
                ) : step === 1 ? 'Continue' : 'Create Account'}
              </button>
            </div>
            
            <div className="text-center text-gray-600">
              Already have an account?{' '}
              <Link to="/login" className="text-primary hover:underline">
                Sign in
              </Link>
            </div>
          </form>
          
          <div className="mt-6 text-center">
            <Link to="/emergency" className="text-emergency hover:underline text-sm font-medium">
              Emergency Access
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage; 