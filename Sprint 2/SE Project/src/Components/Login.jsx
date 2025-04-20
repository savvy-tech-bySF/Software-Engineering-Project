import React from 'react';
import '../style/Auth.css';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const navigate = useNavigate();

  const handleLogin = () => {
    // Add your login logic here
    // If login is successful:
    navigate('/dashboard');
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <div className="logo">{"</>"}</div>
        <h2>Welcome to CodeQuest</h2>
        <p className="subtitle">Sign in to continue to your dashboard</p>

        <div className="input-group">
          <label>Email Address</label>
          <input
            type="email"
            placeholder="Enter your email"
            className="input-field"
          />
          <span className="error-message">Invalid address</span>
        </div>

        <div className="input-group">
          <label>Password</label>
          <input
            type="password"
            placeholder="Enter your password"
            className="input-field"
          />
        </div>

        <div className="remember-forgot">
          <label className="remember">
            <input type="checkbox" />
            Remember me
          </label>
          <a href="/forgot" className="forgot-password">Forgot password?</a>
        </div>

        <button className="submit-btn" onClick={handleLogin}>Sign in</button>

        <div className="divider">
          <span>Or continue with</span>
        </div>

        <div className="social-login">
          <button className="social-btn">@github</button>
          <button className="social-btn">@gmail</button>
        </div>

        <p className="auth-link">
          Don't have an account? <a href="/signup">Sign up</a>
        </p>
      </div>
    </div>
  );
};

export default Login;