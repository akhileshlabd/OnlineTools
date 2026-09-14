import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, abort

blogs_bp = Blueprint('blogs', __name__, url_prefix='/blog')

def get_db_connection():
    conn = sqlite3.connect('blogs.db')
    conn.row_factory = sqlite3.Row
    return conn

@blogs_bp.route('/<slug>', methods=['GET', 'POST'])
def view_blog(slug):
    conn = get_db_connection()
    c = conn.cursor()
    
    if request.method == 'POST':
        content = request.form.get('content')
        blog_id = request.form.get('blog_id')
        if content and blog_id:
            c.execute("INSERT INTO comments (blog_id, content) VALUES (?, ?)", (blog_id, content))
            conn.commit()
        return redirect(url_for('blogs.view_blog', slug=slug))

    c.execute("SELECT * FROM blogs WHERE slug = ?", (slug,))
    blog = c.fetchone()
    
    if not blog:
        conn.close()
        abort(404)
        
    c.execute("SELECT * FROM comments WHERE blog_id = ? ORDER BY created_at DESC", (blog['id'],))
    comments = c.fetchall()
    
    conn.close()
    
    return render_template('blog_post.html', blog=blog, comments=comments)
