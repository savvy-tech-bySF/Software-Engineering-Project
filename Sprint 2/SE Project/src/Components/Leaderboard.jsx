import React from 'react';
import '../style/Leaderboard.css';

function Leaderboard() {
  const topReviewers = [
    { id: 1, name: "Mike Johnson", points: 2890, rank: 2 },
    { id: 2, name: "Sarah Chen", points: 3450, rank: 1 },
    { id: 3, name: "Emma Wilson", points: 2340, rank: 3 }
  ];

  const otherReviewers = [
    { id: 4, name: "John Doe", points: 3240, rank: 4 },
    { id: 5, name: "Syed Hamza", points: 3040, rank: 5 },
    { id: 6, name: "Aiza Imran", points: 2210, rank: 6 },
    { id: 7, name: "Kulsoom Asim", points: 2133, rank: 7 }
  ];

  return (
    <div className="leaderboard-container">
      <h1>Top Reviewers</h1>

      <div className="top-three-container">
        {topReviewers.map(reviewer => (
          <div 
            key={reviewer.id} 
            className={`top-reviewer-card ${reviewer.rank === 1 ? 'top-rank' : ''}`}
          >
            <div className="reviewer-avatar">
              <span>{reviewer.name.charAt(0)}</span>
            </div>
            <div className="reviewer-info">
              <p className="reviewer-name">{reviewer.name}</p>
              <p className="reviewer-points">{reviewer.points.toLocaleString()} points</p>
            </div>
          </div>
        ))}
      </div>

      <div className="other-reviewers-list">
        {otherReviewers.map(reviewer => (
          <div key={reviewer.id} className="reviewer-row">
            <div className="rank-indicator">
              <span>#{reviewer.rank}</span>
            </div>
            <div className="reviewer-avatar small">
              <span>{reviewer.name.charAt(0)}</span>
            </div>
            <div className="reviewer-name">{reviewer.name}</div>
            <div className="reviewer-points">
              {reviewer.points.toLocaleString()}
              <span className="star-icon">★</span>
            </div>
          </div>
        ))}
      </div>

      <div className="pagination">
        <button className="page-btn active">1</button>
        <button className="page-btn">2</button>
        <button className="page-btn">3</button>
        <span className="page-ellipsis">...</span>
        <button className="page-btn">12</button>
        <button className="page-btn">13</button>
        <button className="page-btn">14</button>
      </div>

      <footer className="leaderboard-footer">
        <p>© 2025 CodeQuest. All rights reserved.</p>
        <div className="social-icons">
          <span className="icon">●</span>
          <span className="icon">●</span>
          <span className="icon">●</span>
        </div>
      </footer>
    </div>
  );
}

export default Leaderboard;