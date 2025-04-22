import os
import sqlite3
import random
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage
from dotenv import load_dotenv
from git import Repo
load_dotenv()   # ← this reads .env into os.environ


from flask import (
    Flask, g, render_template, request,
    redirect, url_for, flash, session, jsonify, send_from_directory
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# ── App setup ─────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev_secret")  # override in prod
bcrypt = Bcrypt(app)

# ── Paths & DB setup ──────────────────────────────────────────────────────────
DATABASE      = os.path.join(app.root_path, 'users.db')
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db:
        db.close()



def init_db():
    db = get_db()

    # --- users table with a points column ---
    db.execute("""
      CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email    TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        points   INTEGER NOT NULL DEFAULT 0
      );
    """)

    # --- pull‑requests table stays the same ---
    db.execute("""
        CREATE TABLE IF NOT EXISTS pr (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id     INTEGER NOT NULL,
        pr_id       TEXT,
        repo_url    TEXT,
        repo_name   TEXT,
        filename    TEXT,
        description TEXT,
        created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES user(id)
        );
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS review (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pr_id INTEGER NOT NULL,
        reviewer_id INTEGER NOT NULL,
        rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
        comments TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(pr_id) REFERENCES pr(id),
        FOREIGN KEY(reviewer_id) REFERENCES user(id)
        );
    """)
    db.commit()

with app.app_context():
    init_db()

# ── Email OTP helper ──────────────────────────────────────────────────────────

import os, smtplib
from email.message import EmailMessage

def send_otp_email(to_email, otp):
    host = os.getenv('SMTP_HOST', 'live.smtp.mailtrap.io')
    port = int(os.getenv('SMTP_PORT', 587))
    user = os.getenv('SMTP_USER', 'apismtp@mailtrap.io')
    pwd  = os.getenv('SMTP_PASS', 'adc6')

    msg = EmailMessage()
    msg['Subject'] = "Your CodeQuest OTP"
    msg['From']    = user
    msg['To']      = to_email
    msg.set_content(f"Your CodeQuest OTP is {otp}. It expires in 10 minutes.")

    # Connect to Mailtrap
    with smtplib.SMTP(host, port, timeout=10) as server:
        server.ehlo()
        server.starttls()      # MUST do STARTTLS on port 587
        server.ehlo()
        server.login(user, pwd)
        server.send_message(msg)
        print(f"[SMTP OK] Sent OTP to {to_email}")


# ── Authentication Routes ────────────────────────────────────────────────────

@app.route('/')
def login_page():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    pwd   = request.form['password']
    db    = get_db()
    user  = db.execute("SELECT * FROM user WHERE email = ?", (email,)).fetchone()

    if not user:
        flash("No account with that email. Please sign up first.", "error")
        return redirect(url_for('login_page'))

    if bcrypt.check_password_hash(user['password'], pwd):
        session['user_id'] = user['id']
        session['email']   = user['email']
        return redirect(url_for('dashboard'))

    flash("Invalid password", "error")
    return redirect(url_for('login_page'))

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        u = request.form['username']
        e = request.form['email']
        p = request.form['password']
        c = request.form['confirm_password']
        if p != c:
            flash("Passwords do not match", "error")
            return redirect(url_for('signup'))
        db = get_db()
        try:
            h = bcrypt.generate_password_hash(p).decode()
            db.execute(
                "INSERT INTO user (username,email,password) VALUES (?, ?, ?)",
                (u, e, h)
            )
            db.commit()
        except sqlite3.IntegrityError:
            flash("Username or email already taken", "error")
            return redirect(url_for('signup'))
        flash("Account created! Please log in.", "success")
        return redirect(url_for('login_page'))
    return render_template('signup.html')

@app.route('/forgot-password', methods=['GET','POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        db    = get_db()
        user  = db.execute("SELECT id FROM user WHERE email = ?", (email,)).fetchone()
        if not user:
            flash("No account with that email. Please sign up first.", "error")
            return redirect(url_for('signup'))

        otp = f"{random.randint(1000,9999)}"
        session['otp']        = otp
        session['otp_email']  = email
        session['otp_expiry'] = (datetime.utcnow() + timedelta(minutes=10)).timestamp()
        send_otp_email(email, otp)
        flash("OTP sent to your email", "success")
        return redirect(url_for('verify_otp'))

    return render_template('forgot-password.html')

@app.route('/verify-otp', methods=['GET','POST'])
def verify_otp():
    if request.method == 'POST':
        code   = ''.join(request.form.get(f'otp{i}', '') for i in (1,2,3,4))
        expiry = session.get('otp_expiry', 0)
        if datetime.utcnow().timestamp() > expiry:
            flash("OTP expired, try again.", "error")
            return redirect(url_for('forgot_password'))

        if code == session.get('otp'):
            email = session.pop('otp_email')
            session.pop('otp'); session.pop('otp_expiry')
            user = get_db().execute(
                "SELECT id,email FROM user WHERE email = ?", (email,)
            ).fetchone()
            session['user_id'] = user['id']
            session['email']   = user['email']
            flash("Logged in via OTP!", "success")
            return redirect(url_for('dashboard'))
        flash("Invalid OTP", "error")
        return redirect(url_for('verify_otp'))

    return render_template('verify-otp.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

# Define a list of common coding file extensions
CODE_FILE_EXTENSIONS = [
    '.py', '.js', '.html', '.css', '.java', '.php', '.rb', '.cpp', '.h', '.c', 
    '.ts', '.tsx', '.json', '.xml', '.sql', '.go', '.swift', '.sh', '.bash'
]

import os
from flask import send_from_directory, jsonify

# Define a list of common coding file extensions
CODE_FILE_EXTENSIONS = [
    '.cpp', '.c', '.h', '.js', '.html', '.css', '.java', '.py', '.php', '.rb', 
    '.ts', '.json', '.xml', '.go', '.sh', '.bash', '.md', '.makefile', '.hpp'
]

@app.route('/load-file')
def load_file():
    file_path = request.args.get('path')
    repo_name = request.args.get('repo')

    # Log received file path for debugging
    print(f"Received file path: {file_path} for repo: {repo_name}")

    # Normalize the file path (replace backslashes with forward slashes)
    normalized_path = file_path.replace('\\', '/')

    # Build the full path to the file
    full_path = os.path.join('cloned_repos', repo_name, normalized_path)

    try:
        # Log the final resolved path for debugging
        print(f"Resolved file path: {full_path}")

        # Check if the file exists
        if not os.path.exists(full_path):
            print(f"File does not exist: {full_path}")
            return jsonify({'error': 'File not found'}), 404

        # Get the file extension
        _, file_extension = os.path.splitext(full_path.lower())

        # Check if it's a coding file (based on extension)
        if file_extension in CODE_FILE_EXTENSIONS:
            # Attempt to read the file as text
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({'content': content})
        else:
            # If it's not a coding file, return it as a download
            return send_from_directory(os.path.dirname(full_path), os.path.basename(full_path), as_attachment=True)

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500




@app.route('/leaderboard')
@app.route('/leaderboard.html')
def leaderboard():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    db = get_db()
    users = db.execute(
        "SELECT username, points FROM user ORDER BY points DESC"
    ).fetchall()

    return render_template('leaderboard.html', users=users)

# ── Review Code Listing ───────────────────────────────────────────────────────
@app.route("/review-code")
def review_code():
    # require login
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    db       = get_db()
    sort     = request.args.get('sort', 'latest')
    order    = 'DESC' if sort == 'latest' else 'ASC'
    page     = request.args.get('page', 1, type=int)
    per_page = 5
    offset   = (page - 1) * per_page

    # total count for pagination
    total    = db.execute("SELECT COUNT(*) FROM pr").fetchone()[0]
    pages    = (total + per_page - 1) // per_page

    # fetch a page of PRs with author username
    prs = db.execute(f"""
        SELECT p.*, u.username
          FROM pr p
          JOIN user u ON p.user_id = u.id
      ORDER BY p.created_at {order}
         LIMIT ? OFFSET ?
    """, (per_page, offset)).fetchall()

    return render_template(
        "review-code.html",
        prs           = prs,
        pages         = range(1, pages+1),
        current_page  = page,
        sort          = sort
    )

# ── Review Detail & Submit ───────────────────────────────────────────────────
@app.route("/review-pr/<int:pr_id>", methods=["GET", "POST"])
def review_pr(pr_id):
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    db = get_db()
    pr = db.execute("""
        SELECT p.*, u.username
          FROM pr p
          JOIN user u ON p.user_id = u.id
         WHERE p.id = ?
    """, (pr_id,)).fetchone()

    if not pr:
        flash("Pull request not found.", "error")
        return redirect(url_for('review_code'))

    # Handle form submission
    if request.method == "POST":
        rating = int(request.form["score"])  # score is the field in the form
        comments = request.form["review"].strip()
        reviewer = session["user_id"]

        db.execute("""
          INSERT INTO review (pr_id, reviewer_id, rating, comments)
          VALUES (?, ?, ?, ?)
        """, (pr_id, reviewer, rating, comments))
        
        db.execute("""
          UPDATE user
             SET points = points + 5
           WHERE id = ?
        """, (reviewer,))
        db.commit()

        flash("Review submitted! +5 points", "success")
        return redirect(url_for("review_code"))

    # File browser from cloned repo
    repo_path = os.path.join("cloned_repos", pr["repo_name"])
    file_list = []

    for root, dirs, files in os.walk(repo_path):
        for f in files:
            rel_path = os.path.relpath(os.path.join(root, f), repo_path)
            file_list.append(rel_path)

    return render_template("review_pr.html", pr=pr, files=file_list)


# ── Protected Pages ───────────────────────────────────────────────────────────

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    db = get_db()
    uid = session['user_id']

    user = db.execute("SELECT username, email, points FROM user WHERE id = ?", (uid,)).fetchone()
    my_prs = db.execute("""SELECT id, pr_id, repo_name, created_at FROM pr WHERE user_id = ? ORDER BY created_at DESC""", (uid,)).fetchall()
    given_reviews = db.execute("""SELECT r.id, r.rating, r.comments, r.created_at, p.repo_name FROM review r JOIN pr p ON r.pr_id = p.id WHERE r.reviewer_id = ? ORDER BY r.created_at DESC""", (uid,)).fetchall()
    received_reviews = db.execute("""SELECT r.rating, r.comments, r.created_at, u.username AS reviewer, p.pr_id FROM review r JOIN pr p ON r.pr_id = p.id JOIN user u ON r.reviewer_id = u.id WHERE p.user_id = ? ORDER BY r.created_at DESC""", (uid,)).fetchall()

    leaderboard = db.execute("""SELECT username, points FROM user ORDER BY points DESC LIMIT 10""").fetchall()

    return render_template("dashboard.html",
        user=user,
        my_prs=my_prs,
        given_reviews=given_reviews,
        received_reviews=received_reviews,
        leaderboard=leaderboard
    )


@app.route('/submit-pr', methods=['POST'])
def submit_pr():
    if 'user_id' not in session:
        flash("Please log in first", "error")
        return redirect(url_for('login_page'))

    uid   = session['user_id']
    prid  = request.form.get('prId')
    url   = request.form.get('repoUrl')
    desc  = request.form.get('description')
    file  = request.files.get('file')

    
    # Extract repo name from URL
    repo_name = url.rstrip('/').split('/')[-1]
    local_path = os.path.join("cloned_repos", repo_name)

    # Clone repo if not already cloned
    if not os.path.exists(local_path):
        try:
            Repo.clone_from(url, local_path)
        except Exception as e:
            flash(f"Failed to clone repository: {e}", "error")
            return redirect(url_for('dashboard'))

    filename = None
    if file and file.filename:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    db = get_db()
    db.execute("""
      INSERT INTO pr (user_id, pr_id, repo_url, repo_name, filename, description)
      VALUES (?, ?, ?, ?, ?, ?)
    """, (uid, prid, url, repo_name, filename, desc))

    db.execute("""
      UPDATE user
         SET points = points + 10
       WHERE id = ?
    """, (uid,))
    db.commit()

    flash("Pull request submitted successfully! +10 points", "success")
    return redirect(url_for('dashboard'))

@app.route('/submit-review', methods=['POST'])
def submit_review():
    if 'user_id' not in session:
        flash("Please log in first", "error")
        return redirect(url_for('login_page'))

    uid = session['user_id']
    pr_id = request.form.get('pr_id')  # Retrieve pr_id from the hidden field
    review = request.form.get('review')
    score = int(request.form.get('score'))  # The score provided by the reviewer
    try:
        pr_id = int(request.form.get('pr_id'))
    except (ValueError, TypeError):
        flash("Invalid PR ID", "error")
        return redirect(url_for('review_code'))
    print(f"Received pr_id: {pr_id}")

    # Avoid awarding points to the coder who submitted the PR based on the score
    coder_id = request.form.get('coder_id')  # Assuming coder's ID is passed to the form

    # Calculate points for the reviewer based on the quality of the review
    review_points = calculate_review_points(review)

    # Store the review and points for the reviewer
    db = get_db()

    db.execute("""
      INSERT INTO review (pr_id, reviewer_id, rating, comments)
      VALUES (?, ?, ?, ?)
    """, (pr_id, uid, score, review))  # Use pr_id from the form

    # Award points to the reviewer (not the coder)
    db.execute("""
      UPDATE user
         SET points = points + ?
       WHERE id = ?
    """, (review_points, uid))  # Give points to the reviewer
    db.commit()

    # Do not award points to the coder based on the score given by the reviewer
    db.execute("""
      UPDATE user
         SET points = points + 10  
       WHERE id = ?
    """, (coder_id,))
    db.commit()

    flash(f"Review submitted successfully! You earned {review_points} points.", "success")
    return redirect(url_for('dashboard'))



def calculate_review_points(review_text):
    """
    Calculate points based on the review text.
    A more advanced example could be rewarding points for positive sentiment.
    """
    word_count = len(review_text.split())
    
    # Basic logic: Assign points based on review length
    if word_count >= 200:
        return 5  # High-quality review
    elif word_count >= 100:
        return 3  # Medium-quality review
    else:
        return 1  # Short review, minimal points

    # Optionally, you can also incorporate sentiment analysis with TextBlob for more complex scoring
    # sentiment_score = TextBlob(review_text).sentiment.polarity
    # if sentiment_score > 0.5:
    #     return 5  # Positive, helpful review
    # elif sentiment_score > 0:
    #     return 3  # Neutral, constructive review
    # else:
    #     return 1  # Negative review

# ── Static & Fallback ─────────────────────────────────────────────────────────

@app.route('/<page>.html')
def serve_page(page):
    return render_template(f'{page}.html')

@app.route('/<path:filename>')
def static_files(filename):
    from flask import send_from_directory
    return send_from_directory('.', filename)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
