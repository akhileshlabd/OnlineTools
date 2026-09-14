import sqlite3
import os
import re
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, current_app

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

ADMIN_USER = "dhwaniakhilesh@gmail.com"
ADMIN_PASS = "itsformyfamily"

def get_db_connection():
    conn = sqlite3.connect('blogs.db')
    conn.row_factory = sqlite3.Row
    return conn

def make_slug(title):
    s = title.lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

@admin_bp.route('/', methods=['GET'])
def index():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('admin.login'))

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin.dashboard'))
        
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            error = "Invalid username or password"
            
    return render_template('admin_login.html', error=error)

@admin_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard', methods=['GET'])
def dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
        
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM blogs ORDER BY created_at DESC")
    blogs = c.fetchall()
    conn.close()
    
    return render_template('admin_dashboard.html', blogs=blogs)

@admin_bp.route('/api/add-blog', methods=['POST'])
def add_blog():
    if not session.get('admin_logged_in'):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
        
    title = request.form.get('title')
    content = request.form.get('content')
    image = request.files.get('image')
    
    if not title or not content:
        return jsonify({"success": False, "message": "Title and Content are required."})
        
    slug = make_slug(title)
    image_path = None
    
    if image and image.filename != '':
        filename = secure_filename(image.filename)
        # Ensure directory exists
        upload_dir = os.path.join('static', 'uploads', 'blogs')
        os.makedirs(upload_dir, exist_ok=True)
        
        full_path = os.path.join(upload_dir, filename)
        image.save(full_path)
        image_path = f"/static/uploads/blogs/{filename}"
    
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO blogs (title, slug, content, image_path) VALUES (?, ?, ?, ?)", 
                  (title, slug, content, image_path))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Blog added successfully!"})
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "A blog with this title/slug already exists."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
