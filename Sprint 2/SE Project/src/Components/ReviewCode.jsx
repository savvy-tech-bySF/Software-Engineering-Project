import React, { useState } from 'react';
import '../style/ReviewCode.css';

const ReviewCode = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [score, setScore] = useState(5);
  const [comment, setComment] = useState('');

  const reviews = [
    {
      title: "Authentication Service Update",
      author: "Michael Chen",
      time: "2 hours ago",
      lines: 5,
      comments: 3,
      completed: false,
      code: `function authentication(token) {
  // Updated Dutch implementation
  return verify(token).then(user => {
    return validateSession(user);
  });
}`
    },
    {
      title: "API Rate Limiting Implementation",
      author: "Sarah Wilson",
      time: "3 hours ago",
      lines: 5,
      comments: 2,
      completed: true,
      code: `class ReticLister {
  constructor(limit) {
    this.limit = limit;
    this.tokens = new Map();
  }
}`
    }
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log({ score, comment });
    // Submit logic would go here
    alert('Review submitted successfully!');
    setComment('');
    setScore(5);
  };

  const handleCommentClick = (index) => {
    // Handle comment click - could show a modal or navigate to comments section
    console.log(`Viewing comments for review ${index}`);
    // For now, just set the active tab
    setActiveTab(index);
  };

  return (
    <div className="review-code-container">
      <h1>Review Code</h1>

      <div className="sort-options">
        <label>Sort by:</label>
        <select>
          <option>Latest First</option>
          <option>Oldest First</option>
          <option>Most Comments</option>
          <option>Least Comments</option>
        </select>
      </div>

      <div className="review-layout">
        <div className="review-tabs-vertical">
          {reviews.map((review, index) => (
            <div 
              key={index}
              className={`review-tab ${activeTab === index ? 'active' : ''}`}
              onClick={() => setActiveTab(index)}
            >
              <h2>{review.title}</h2>
              <p className="meta">by {review.author} - {review.time}</p>
              <div className="gitlab-info">
                <p>{review.lines} lines</p>
                <p>
                  <span 
                    className={`comment-count ${review.comments > 0 ? 'has-comments' : ''}`}
                    onClick={(e) => {
                      e.stopPropagation();
                      handleCommentClick(index);
                    }}
                  >
                    {review.comments} comments
                  </span>
                </p>
              </div>
            </div>
          ))}
        </div>

        <div className="code-review-content">
          <div className="code-display">
            <pre><code>{reviews[activeTab].code}</code></pre>
          </div>

          <div className="feedback-section">
            <h3>Submit Feedback</h3>
            <form onSubmit={handleSubmit}>
              <div className="score-selector">
                <label>Score:</label>
                <div className="score-buttons">
                  {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(num => (
                    <button
                      key={num}
                      type="button"
                      className={`score-btn ${score === num ? 'selected' : ''}`}
                      onClick={() => setScore(num)}
                    >
                      {num}
                    </button>
                  ))}
                </div>
              </div>

              <div className="comment-box">
                <label>Comments:</label>
                <textarea
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  placeholder="Provide detailed feedback..."
                  rows="5"
                />
              </div>

              <button type="submit" className="submit-btn">
                Submit Review
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReviewCode;