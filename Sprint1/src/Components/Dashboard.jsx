import React from 'react';

import '../style/Dashboard.css';


const Dashboard = () => {
  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Dashboard</h1>
      </header>

      <main className="dashboard-content">
        <section className="welcome-section">
          <h2>Welcome back, Alex!</h2>
          <p>Your code review stats this month.</p>
          
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Code Reviews</h3>
              <div className="stat-value">42</div>
            </div>
            <div className="stat-card">
              <h3>Points Earned</h3>
              <div className="stat-value">156</div>
            </div>
            <div className="stat-card">
              <h3>Badges Earned</h3>
              <div className="stat-value">3</div>
            </div>
            <div className="stat-card">
              <h3>Rank</h3>
              <div className="stat-value">#3</div>
            </div>
          </div>
        </section>

        <div className="dashboard-columns">
          <section className="pending-reviews">
            <h3>Your Pending Reviews</h3>
            <ul className="review-list">
              <li>
                <div className="review-icon"></div>
                <div>
                  <h4>Authentication Service Update</h4>
                  <p>by Mike Chen • 3h ago</p>
                </div>
              </li>
              <li>
                <div className="review-icon"></div>
                <div>
                  <h4>API Endpoint Optimization</h4>
                  <p>by Karen Lee • 1d ago</p>
                </div>
              </li>
            </ul>
          </section>

          <section className="recent-activity">
            <h3>Recent Activity</h3>
            <ul className="activity-list">
              <li>
                <div className="activity-icon"></div>
                <div>
                  <h4>Completed Review: Database Schema Changes</h4>
                  <p>You earned 5 points • 1h ago</p>
                </div>
              </li>
              <li>
                <div className="activity-icon"></div>
                <div>
                  <h4>Earned Badge: Code Guru</h4>
                  <p>Completed 50 reviews • 3h ago</p>
                </div>
              </li>
              <li>
                <div className="activity-icon"></div>
                <div>
                  <h4>New Comment on Your Review</h4>
                  <p>From Droid Wrang • 8h ago</p>
                </div>
              </li>
            </ul>
          </section>
        </div>

        <section className="sent-reviews">
          <h3>Recently Sent for Review</h3>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Repository</th>
                  <th>PR ID</th>
                  <th>Status</th>
                  <th>Points</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>frontend/main</td>
                  <td>#1234</td>
                  <td>Pending</td>
                  <td>50</td>
                  <td><button className="view-btn">View Details</button></td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <div className="dashboard-columns">
          <section className="badges-section">
            <h3>Your Badges</h3>
            <div className="badges-grid">
              <div className="badge-card">
                <div className="badge-icon"></div>
                <h4>Top Reviewer</h4>
              </div>
              <div className="badge-card">
                <div className="badge-icon"></div>
                <h4>Quick Response</h4>
              </div>
              <div className="badge-card">
                <div className="badge-icon"></div>
                <h4>Consistent</h4>
              </div>
            </div>
          </section>

          <section className="top-reviewers">
            <h3>Top Reviewers</h3>
            <ul className="reviewers-list">
              <li>
                <div className="reviewer-icon"></div>
                <div>
                  <h4>John Doe</h4>
                  <p>324 pts</p>
                </div>
              </li>
              <li>
                <div className="reviewer-icon"></div>
                <div>
                  <h4>Emma Wilson</h4>
                  <p>298 pts</p>
                </div>
              </li>
              <li>
                <div className="reviewer-icon"></div>
                <div>
                  <h4>Alex Chen</h4>
                  <p>156 pts</p>
                </div>
              </li>
            </ul>
          </section>
        </div>
      </main>

      <footer className="dashboard-footer">
        <p>© 2025 Dashboard. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Dashboard;