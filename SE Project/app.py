import os
import sqlite3
from flask import Flask, g, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# ── App setup ─────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev_secret")  # override in prod

bcrypt = Bcrypt(app)

# ── Database setup ───────────────────────────────────────────────────────────
DATABASE = os.path.join(app.root_path, 'users.db')
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
    # users table
    db.execute("""
      CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
      )
    """)
    # pull requests table
    db.execute("""
      CREATE TABLE IF NOT EXISTS pr (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        pr_id TEXT,
        repo_url TEXT,
        filename TEXT,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES user(id)
      )
    """)
    db.commit()

with app.app_context():
    init_db()

# ── Authentication Routes ────────────────────────────────────────────────────

@app.route('/')
def login_page():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    db = get_db()
    user = db.execute("SELECT * FROM user WHERE email = ?", (email,)).fetchone()
    if user and bcrypt.check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        session['email'] = user['email']
        return redirect(url_for('dashboard'))
    flash("Invalid email or password", "error")
    return redirect(url_for('login_page'))

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email    = request.form['email']
        pwd      = request.form['password']
        confirm  = request.form['confirm_password']

        if pwd != confirm:
            flash("Passwords do not match", "error")
            return redirect(url_for('signup'))

        db = get_db()
        try:
            pw_hash = bcrypt.generate_password_hash(pwd).decode('utf-8')
            db.execute(
                "INSERT INTO user (username, email, password) VALUES (?, ?, ?)",
                (username, email, pw_hash)
            )
            db.commit()
        except sqlite3.IntegrityError:
            flash("Username or email already taken", "error")
            return redirect(url_for('signup'))

        flash("Account created! Please log in.", "success")
        return redirect(url_for('login_page'))

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

# ── Main App Pages ────────────────────────────────────────────────────────────

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

    user_id     = session['user_id']
    pr_id       = request.form.get('prId')
    repo_url    = request.form.get('repoUrl')
    description = request.form.get('description')
    file        = request.files.get('file')

    filename = None
    if file and file.filename:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    db = get_db()
    db.execute("""
      INSERT INTO pr (user_id, pr_id, repo_url, filename, description)
      VALUES (?, ?, ?, ?, ?)
    """, (user_id, pr_id, repo_url, filename, description))
    db.commit()

    flash("Pull request submitted successfully!", "success")
    return render_template('dashboard.html')

# ── Static & Fallback ─────────────────────────────────────────────────────────

@app.route('/<page>.html')
def serve_page(page):
    return render_template(f'{page}.html')

@app.route('/<path:filename>')
def static_files(filename):
    from flask import send_from_directory
    return send_from_directory('.', filename)

# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True, port=5000)
