import os
import sqlite3
import random
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()   # ← this reads .env into os.environ


from flask import (
    Flask, g, render_template, request,
    redirect, url_for, flash, session
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
        filename    TEXT,
        description TEXT,
        created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES user(id)
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




# ── Protected Pages ───────────────────────────────────────────────────────────

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('dashboard.html')

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

    filename = None
    if file and file.filename:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    db = get_db()
    # insert PR
    db.execute("""
      INSERT INTO pr (user_id, pr_id, repo_url, filename, description)
      VALUES (?, ?, ?, ?, ?)
    """, (uid, prid, url, filename, desc))

    # award 10 points
    db.execute("""
      UPDATE user
         SET points = points + 10
       WHERE id = ?
    """, (uid,))

    db.commit()

    flash("Pull request submitted successfully! +10 points", "success")
    return redirect(url_for('dashboard'))


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
