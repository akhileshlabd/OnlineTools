import sqlite3
import os
import re
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, current_app

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

ADMIN_USER = "dhwaniakhilesh@gmail.com"
ADMIN_PASS = "itsformyfamily"


FEATURE_GROUPS = {
    "PDF Tools": "feature_nav_pdf",
    "Image Tools": "feature_nav_image",
    "Free Games": "feature_nav_games",
    "Finance Tools": "feature_nav_finance",
    "Health Tools": "feature_nav_health",
    "Text Tools": "feature_nav_text",
    "Network Tools": "feature_nav_network",
    "Code & Dev Tools": "feature_nav_dev",
}
    },
    {
        "key": "feature_nav_image",
        "label": "Image Tools",
        "icon": "fa-image",
        "children": [
            {"key": "feature_image_resizer", "label": "Image Resizer"},
            {"key": "feature_image_converter", "label": "Image Converter"},
            {"key": "feature_image_qr", "label": "QR Generator"},
            {"key": "feature_image_passport_maker", "label": "Passport Maker"},
            {"key": "feature_image_bg_remover", "label": "Background Remover"},
            {"key": "feature_image_grayscale", "label": "Grayscale Image"},
            {"key": "feature_image_blur", "label": "Blur Image"},
            {"key": "feature_image_flip_h", "label": "Flip Horizontal"},
            {"key": "feature_image_flip_v", "label": "Flip Vertical"},
            {"key": "feature_image_rotate_tool", "label": "Rotate Image"},
            {"key": "feature_image_brightness", "label": "Adjust Brightness"},
            {"key": "feature_image_contrast", "label": "Adjust Contrast"},
        ]
    },
    {
        "key": "feature_nav_games",
        "label": "Free Games",
        "icon": "fa-gamepad",
        "children": [
            {"key": "feature_game_sudoku-game", "label": "Sudoku"},
            {"key": "feature_game_tetris-game", "label": "Tetris"},
            {"key": "feature_game_brick-breaker", "label": "Brick Breaker"},
            {"key": "feature_game_snake-game", "label": "Snake"},
            {"key": "feature_game_neon-qube", "label": "Neon Qube"},
        ]
    },
    {
        "key": "feature_nav_finance",
        "label": "Finance Tools",
        "icon": "fa-calculator",
        "children": [
            {"key": "feature_fin_emi", "label": "EMI Calculator"},
            {"key": "feature_fin_sip", "label": "SIP Calculator"},
            {"key": "feature_fin_fd", "label": "FD Calculator"},
        ]
    },
    {
        "key": "feature_nav_health",
        "label": "Health Tools",
        "icon": "fa-heartbeat",
        "children": [
            {"key": "feature_health_bmi", "label": "BMI Calculator"},
            {"key": "feature_health_macro", "label": "Macro Calculator"},
        ]
    },
    {
        "key": "feature_nav_text",
        "label": "Text Tools",
        "icon": "fa-font",
        "children": [
            {"key": "feature_text_counter", "label": "Word Counter"},
            {"key": "feature_text_case", "label": "Case Converter"},
            {"key": "feature_text_tts", "label": "Text to Speech"},
        ]
    },
    {
        "key": "feature_nav_network",
        "label": "Network Tools",
        "icon": "fa-network-wired",
        "children": [
            {"key": "feature_net_ip", "label": "My IP Address"},
            {"key": "feature_net_ping", "label": "Ping Tester"},
        ]
    },
    {
        "key": "feature_nav_dev",
        "label": "Code & Dev Tools",
        "icon": "fa-code",
        "children": [
            {"key": "feature_dev_json", "label": "JSON Formatter"},
            {"key": "feature_dev_b64", "label": "Base64 Encode/Decode"},
        ]
    },
    {
        "key": "feature_nav_video",
        "label": "Video Tools",
        "icon": "fa-video",
        "children": [
            {"key": "feature_vid_mp3", "label": "Video to MP3"}
        ]
    },
    {
        "key": "feature_nav_kids",
        "label": "Kids Zone",
        "icon": "fa-child",
        "children": [
            {"key": "feature_kids_tracing", "label": "Letter Tracing"}
        ]
    },
    {
        "key": "feature_nav_compare",
        "label": "Compare Phones",
        "icon": "fa-mobile-alt",
        "children": []
    }
]

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
    
    # Settings (Global Comments)
    c.execute("SELECT value FROM settings WHERE key = 'global_comments_enabled'")
    row = c.fetchone()
    global_comments_enabled = (row['value'] == '1') if row else True
    
    # Feature Toggles
    c.execute("SELECT key, value FROM settings WHERE key LIKE 'feature_%'")
    f_rows = c.fetchall()
    feature_dict = {r['key']: (r['value'] == '1') for r in f_rows}
    
    features_grouped = {}
    for label, key in FEATURE_GROUPS.items():
        features_grouped[label] = {
            "key": key,
            "is_enabled": feature_dict.get(key, True)
        }
    
    # Blog Filters
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    sort = request.args.get('sort', 'DESC')
    if sort not in ['ASC', 'DESC']: sort = 'DESC'
    
    query = "SELECT * FROM blogs"
    params = []
    conditions = []
    
    if date_from:
        conditions.append("date(created_at) >= ?")
        params.append(date_from)
    if date_to:
        conditions.append("date(created_at) <= ?")
        params.append(date_to)
        
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    query += f" ORDER BY created_at {sort}"
    
    c.execute(query, params)
    blogs_raw = c.fetchall()
    
    blogs = []
    for b in blogs_raw:
        blog_dict = dict(b)
        c.execute("SELECT * FROM comments WHERE blog_id = ? ORDER BY created_at ASC", (b['id'],))
        blog_dict['comments'] = c.fetchall()
        blogs.append(blog_dict)
        
    conn.close()
    
    active_tab = request.args.get('tab', 'blogs')
    
    return render_template('admin_dashboard.html', 
                           blogs=blogs, 
                           global_comments_enabled=global_comments_enabled, 
                           features_grouped=features_grouped,
                           sort=sort, 
                           date_from=date_from or '', 
                           date_to=date_to or '',
                           active_tab=active_tab)

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
        c.execute("INSERT INTO blogs (title, slug, content, image_path, comments_enabled, is_hidden) VALUES (?, ?, ?, ?, 1, 0)", (title, slug, content, image_path))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Blog added successfully!"})
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "A blog with this title/slug already exists."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@admin_bp.route('/api/edit-blog/<int:blog_id>', methods=['POST'])
def edit_blog(blog_id):
    if not session.get('admin_logged_in'): return jsonify({"success": False, "message": "Unauthorized"}), 401
    title = request.form.get('title')
    content = request.form.get('content')
    remove_image = request.form.get('remove_image') == 'true'
    image = request.files.get('image')
    
    conn = get_db_connection()
    c = conn.cursor()
    
    if remove_image:
        c.execute("UPDATE blogs SET title = ?, content = ?, image_path = NULL WHERE id = ?", (title, content, blog_id))
    elif image and image.filename != '':
        filename = secure_filename(image.filename)
        upload_dir = os.path.join('static', 'uploads', 'blogs')
        os.makedirs(upload_dir, exist_ok=True)
        full_path = os.path.join(upload_dir, filename)
        image.save(full_path)
        image_path = f"/static/uploads/blogs/{filename}"
        c.execute("UPDATE blogs SET title = ?, content = ?, image_path = ? WHERE id = ?", (title, content, image_path, blog_id))
    else:
        c.execute("UPDATE blogs SET title = ?, content = ? WHERE id = ?", (title, content, blog_id))
        
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Blog updated successfully!"})

@admin_bp.route('/api/delete-blog/<int:blog_id>', methods=['POST'])
def delete_blog(blog_id):
    if not session.get('admin_logged_in'): return jsonify({"success": False, "message": "Unauthorized"}), 401
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM comments WHERE blog_id = ?", (blog_id,))
    c.execute("DELETE FROM blogs WHERE id = ?", (blog_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@admin_bp.route('/api/toggle-visibility/<int:blog_id>', methods=['POST'])
def toggle_visibility(blog_id):
    if not session.get('admin_logged_in'): return jsonify({"success": False, "message": "Unauthorized"}), 401
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT is_hidden FROM blogs WHERE id = ?", (blog_id,))
    row = c.fetchone()
    new_val = 0 if row['is_hidden'] else 1
    c.execute("UPDATE blogs SET is_hidden = ? WHERE id = ?", (new_val, blog_id))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@admin_bp.route('/api/toggle-global-comments', methods=['POST'])
def toggle_global_comments():
    if not session.get('admin_logged_in'): return jsonify({"success": False, "message": "Unauthorized"}), 401
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key = 'global_comments_enabled'")
    row = c.fetchone()
    current_val = row['value'] if row else '1'
    new_val = '0' if current_val == '1' else '1'
    c.execute("INSERT INTO settings (key, value) VALUES ('global_comments_enabled', ?) ON CONFLICT(key) DO UPDATE SET value = ?", (new_val, new_val))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@admin_bp.route('/api/toggle-blog-comments/<int:blog_id>', methods=['POST'])
def toggle_blog_comments(blog_id):
    if not session.get('admin_logged_in'): return jsonify({"success": False, "message": "Unauthorized"}), 401
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT comments_enabled FROM blogs WHERE id = ?", (blog_id,))
    row = c.fetchone()
    new_val = 0 if row['comments_enabled'] else 1
    c.execute("UPDATE blogs SET comments_enabled = ? WHERE id = ?", (new_val, blog_id))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@admin_bp.route('/api/delete-comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    if not session.get('admin_logged_in'): return jsonify({"success": False, "message": "Unauthorized"}), 401
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@admin_bp.route('/api/toggle-feature', methods=['POST'])
def toggle_feature():
    if not session.get('admin_logged_in'): return jsonify({"success": False, "message": "Unauthorized"}), 401
    feature_key = request.form.get('key')
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key = ?", (feature_key,))
    row = c.fetchone()
    current_val = row['value'] if row else '1'
    new_val = '0' if current_val == '1' else '1'
    
    c.execute("INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = ?", (feature_key, new_val, new_val))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "new_val": new_val})
