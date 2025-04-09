import React from 'react';
import '../style/Auth.css';
import { useNavigate, Link } from 'react-router-dom';

const Registration = () => {
  const navigate = useNavigate();
  
  const handleSignUp = () => {
    // Add your registration logic here
    // If registration is successful:
    navigate('/dashboard');
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <div className="logo">{"</>"}</div>
        <h2>Welcome to CodeQuest</h2>
        <p className="subtitle">Sign up to continue to your dashboard</p>

        <div className="input-group">
          <label>Username</label>
          <input
            type="text"
            placeholder="Enter your username"
            className="input-field"
          />
        </div>

        <div className="input-group">
          <label>Email Address</label>
          <input
            type="email"
            placeholder="Enter your email"
            className="input-field"
          />
        </div>

        <div className="input-group">
          <label>Password</label>
          <input
            type="password"
            placeholder="Enter your password"
            className="input-field"
          />
        </div>

        <div className="input-group">
          <label>Confirm Password</label>
          <input
            type="password"
            placeholder="Enter your password"
            className="input-field"
          />
        </div>

        <button className="submit-btn" onClick={handleSignUp}>Sign up</button>

        <div className="divider">
          <span>Or continue with</span>
        </div>

        <div className="social-login">
          <button className="social-btn">@linkb</button>
          <button className="social-btn">@lutub</button>
        </div>

        <p className="auth-link">
          Have an account? <Link to="/">Sign in</Link>
        </p>
      </div>
    </div>
  );
};

export default Registration;