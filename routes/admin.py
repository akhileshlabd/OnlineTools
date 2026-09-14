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
    
    # Get global comment setting
    c.execute("SELECT value FROM settings WHERE key = 'global_comments_enabled'")
    row = c.fetchone()
    global_comments_enabled = (row['value'] == '1') if row else True
    
    c.execute("SELECT * FROM blogs ORDER BY created_at DESC")
    blogs_raw = c.fetchall()
    
    blogs = []
    # Attach comments to each blog for admin viewing
    for b in blogs_raw:
        blog_dict = dict(b)
        c.execute("SELECT * FROM comments WHERE blog_id = ? ORDER BY created_at ASC", (b['id'],))
        blog_dict['comments'] = c.fetchall()
        blogs.append(blog_dict)
        
    conn.close()
    
    return render_template('admin_dashboard.html', blogs=blogs, global_comments_enabled=global_comments_enabled)

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
        upload_dir = os.path.join('static', 'uploads', 'blogs')
        os.makedirs(upload_dir, exist_ok=True)
        
        full_path = os.path.join(upload_dir, filename)
        image.save(full_path)
        image_path = f"/static/uploads/blogs/{filename}"
    
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO blogs (title, slug, content, image_path, comments_enabled) VALUES (?, ?, ?, ?, 1)", 
                  (title, slug, content, image_path))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Blog added successfully!"})
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "A blog with this title/slug already exists."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@admin_bp.route('/api/toggle-global-comments', methods=['POST'])
def toggle_global_comments():
    if not session.get('admin_logged_in'):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key = 'global_comments_enabled'")
    row = c.fetchone()
    current_val = row['value'] if row else '1'
    new_val = '0' if current_val == '1' else '1'
    
    c.execute("UPDATE settings SET value = ? WHERE key = 'global_comments_enabled'", (new_val,))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "new_status": new_val})

@admin_bp.route('/api/toggle-blog-comments/<int:blog_id>', methods=['POST'])
def toggle_blog_comments(blog_id):
    if not session.get('admin_logged_in'):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
        
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT comments_enabled FROM blogs WHERE id = ?", (blog_id,))
    row = c.fetchone()
    if not row:
        return jsonify({"success": False, "message": "Blog not found"}), 404
        
    new_val = 0 if row['comments_enabled'] else 1
    c.execute("UPDATE blogs SET comments_enabled = ? WHERE id = ?", (new_val, blog_id))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "new_status": new_val})

@admin_bp.route('/api/delete-comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    if not session.get('admin_logged_in'):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
        
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})
