import React, { useState } from 'react';
import '../style/Auth.css';

const ForgotPassword = () => {
  const [step, setStep] = useState(1);

  return (
    <div className="auth-container">
      <div className="auth-box">
        <div className="logo">{"</>"}</div>
        <h2>Forgot Password</h2>
        
        {step === 1 ? (
          <>
            <p className="subtitle">Enter email address to receive CIP</p>
            <div className="input-group">
              <label>Email address</label>
              <input
                type="email"
                placeholder="Enter your email"
                className="input-field"
              />
            </div>
            <button className="submit-btn" onClick={() => setStep(2)}>Get CIP</button>
          </>
        ) : (
          <>
            <p className="subtitle">Enter CIP Verification Code</p>
            <div className="input-group">
              <label>Verification Code</label>
              <input
                type="text"
                placeholder="Enter verification code"
                className="input-field"
              />
            </div>
            <button className="submit-btn">Sign Up</button>
          </>
        )}

        <div className="divider">
          <span>Or continue with</span>
        </div>

        <div className="social-login">
          <button className="social-btn">@linkb</button>
          <button className="social-btn">@lutub</button>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;