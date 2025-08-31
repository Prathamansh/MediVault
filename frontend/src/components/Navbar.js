import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = ({ isLoggedIn, onLogout }) => {
  return (
    <nav className="navbar">
      <div className="flex items-center">
        <Link to="/" className="text-xl font-bold text-primary">
          MediVault
        </Link>
      </div>
      <div className="flex items-center gap-4">
        {isLoggedIn ? (
          <>
            <Link to="/dashboard" className="text-gray-700 hover:text-primary">
              Dashboard
            </Link>
            <Link to="/profile" className="text-gray-700 hover:text-primary">
              Profile
            </Link>
            <button 
              onClick={onLogout}
              className="btn btn-primary"
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="text-gray-700 hover:text-primary">
              Login
            </Link>
            <Link to="/register" className="btn btn-primary">
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar; 