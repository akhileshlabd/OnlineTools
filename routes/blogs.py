import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, abort

blogs_bp = Blueprint('blogs', __name__, url_prefix='/blog')

def get_db_connection():
    conn = sqlite3.connect('blogs.db')
    conn.row_factory = sqlite3.Row
    return conn

@blogs_bp.route('/', methods=['GET'])
def index():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM blogs ORDER BY created_at DESC")
    blogs = c.fetchall()
    conn.close()
    return render_template('blog_hub.html', blogs=blogs)

@blogs_bp.route('/<slug>', methods=['GET', 'POST'])
def view_blog(slug):
    conn = get_db_connection()
    c = conn.cursor()
    
    # Check global settings
    c.execute("SELECT value FROM settings WHERE key = 'global_comments_enabled'")
    row = c.fetchone()
    global_comments = (row['value'] == '1') if row else True
    
    c.execute("SELECT * FROM blogs WHERE slug = ?", (slug,))
    blog = c.fetchone()
    
    if not blog:
        conn.close()
        abort(404)
        
    comments_allowed = global_comments and bool(blog['comments_enabled'])
    
    if request.method == 'POST' and comments_allowed:
        content = request.form.get('content')
        blog_id = request.form.get('blog_id')
        if content and blog_id:
            c.execute("INSERT INTO comments (blog_id, content) VALUES (?, ?)", (blog_id, content))
            conn.commit()
        return redirect(url_for('blogs.view_blog', slug=slug))

    comments = []
    if comments_allowed:
        c.execute("SELECT * FROM comments WHERE blog_id = ? ORDER BY created_at DESC", (blog['id'],))
        comments = c.fetchall()
    
    conn.close()
    
    return render_template('blog_post.html', blog=blog, comments=comments, comments_allowed=comments_allowed)
