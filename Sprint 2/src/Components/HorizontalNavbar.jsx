import React from 'react';
import '../style/HorizontalNavbar.css';
import { Link, useLocation } from 'react-router-dom';

const HorizontalNavbar = () => {
  const location = useLocation();
  
  return (
    <nav className="horizontal-navbar">
      <div className="navbar-brand">
        <span className="logo">{"</>"}</span>
        <span className="app-name">CodeQuest</span>
      </div>

      <div className="nav-links">
        <Link to="/dashboard" className={`nav-link ${location.pathname === '/dashboard' ? 'active' : ''}`}>
          <span className="nav-icon"></span>
          <span>Dashboard</span>
        </Link>
        <Link to="/feedback" className={`nav-link ${location.pathname === '/feedback' ? 'active' : ''}`}>
          <span className="nav-icon"></span>
          <span>Feedback</span>
        </Link>
        <Link to="/review-code" className={`nav-link ${location.pathname === '/review-code' ? 'active' : ''}`}>
          <span className="nav-icon"></span>
          <span>Review Code</span>
        </Link>
        <Link to="/leaderboard" className={`nav-link ${location.pathname === '/leaderboard' ? 'active' : ''}`}>
          <span className="nav-icon"></span>
          <span>Leaderboard</span>
        </Link>
        <Link to="/my-files" className={`nav-link ${location.pathname === '/my-files' ? 'active' : ''}`}>
          <span className="nav-icon"></span>
          <span>My Files</span>
        </Link>
      </div>

      <div className="user-section">
        <div className="user-info">
          <span className="user-name">Alex C.</span>
        </div>
        <button className="logout-btn">Logout</button>
      </div>
    </nav>
  );
};

export default HorizontalNavbar;