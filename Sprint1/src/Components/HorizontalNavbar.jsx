import React from 'react';
import '../style/HorizontalNavbar.css';

const HorizontalNavbar = () => {
  return (
    <nav className="horizontal-navbar">
      <div className="navbar-brand">
        <span className="logo">{"</>"}</span>
        <span className="app-name">CodeQuest</span>
      </div>

      <div className="nav-links">
        <a href="#" className="nav-link active">
          <span className="nav-icon"></span>
          <span>Dashboard</span>
        </a>
        <a href="#" className="nav-link">
          <span className="nav-icon"></span>
          <span>Feedback</span>
        </a>
        <a href="#" className="nav-link">
          <span className="nav-icon"></span>
          <span>Review Code</span>
        </a>
        <a href="#" className="nav-link">
          <span className="nav-icon"></span>
          <span>Leaderboard</span>
        </a>
        <a href="#" className="nav-link">
          <span className="nav-icon"></span>
          <span>My Files</span>
        </a>
      </div>

      <div className="nav-user">
        <div className="user-profile">
          <span className="user-icon"></span>
          <span className="username">Alex C.</span>
        </div>
        <button className="logout-btn">
          <span className="logout-icon"></span>
        </button>
      </div>
    </nav>
  );
};

export default HorizontalNavbar;