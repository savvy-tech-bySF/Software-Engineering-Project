import React from 'react';
import '../style/Feedback.css';

const FeedbackPage = () => {
  return (
    <div className="feedback-container">
      <h1>Submit Pull Request</h1>
      
      <div className="pr-id-section">
        <h2>Pull Request ID</h2>
        <div className="pr-id">123</div>
      </div>

      <div className="repo-info">
        <p>Repository URL</p>
        <a href="https://github.com/usemame/repository" className="repo-link">
          https://github.com/usemame/repository
        </a>
      </div>

      <div className="divider"></div>

      <div className="description-section">
        <h3>Description</h3>
        <p className="description-text">Briefly describe your project...</p>
      </div>

      <div className="file-upload">
        <div className="drag-drop-message">Drag and Drop files here</div>
      </div>

      <button className="submit-button">Submit for Review</button>
    </div>
  );
};

export default FeedbackPage;