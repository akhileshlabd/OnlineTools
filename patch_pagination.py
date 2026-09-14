with open('routes/blogs.py', 'r') as f:
    content = f.read()

# Replace index() route
old_index = """@blogs_bp.route('/', methods=['GET'])
def index():
    conn = get_db_connection()
    c = conn.cursor()
    # Only show blogs that are not hidden
    c.execute("SELECT * FROM blogs WHERE is_hidden = 0 ORDER BY created_at DESC")
    blogs = c.fetchall()
    conn.close()
    return render_template('blog_hub.html', blogs=blogs)"""

new_index = """@blogs_bp.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 6
    offset = (page - 1) * per_page
    
    conn = get_db_connection()
    c = conn.cursor()
    
    # Get total count
    c.execute("SELECT COUNT(*) as count FROM blogs WHERE is_hidden = 0")
    total_blogs = c.fetchone()['count']
    total_pages = (total_blogs + per_page - 1) // per_page
    
    # Get paginated blogs
    c.execute("SELECT * FROM blogs WHERE is_hidden = 0 ORDER BY created_at DESC LIMIT ? OFFSET ?", (per_page, offset))
    blogs = c.fetchall()
    conn.close()
    
    return render_template('blog_hub.html', blogs=blogs, page=page, total_pages=total_pages)"""

content = content.replace(old_index, new_index)

with open('routes/blogs.py', 'w') as f:
    f.write(content)


with open('templates/blog_hub.html', 'r') as f:
    html_content = f.read()

pagination_html = """
    {% if total_pages and total_pages > 1 %}
    <nav aria-label="Blog pagination" class="mt-5">
        <ul class="pagination justify-content-center">
            <li class="page-item {% if page == 1 %}disabled{% endif %}">
                <a class="page-link" href="{{ url_for('blogs.index', page=page-1) }}" tabindex="-1" style="border-radius: 8px 0 0 8px; font-weight: 600;">Previous</a>
            </li>
            
            {% for p in range(1, total_pages + 1) %}
            <li class="page-item {% if p == page %}active{% endif %}">
                <a class="page-link" href="{{ url_for('blogs.index', page=p) }}" style="font-weight: 600;">{{ p }}</a>
            </li>
            {% endfor %}
            
            <li class="page-item {% if page == total_pages %}disabled{% endif %}">
                <a class="page-link" href="{{ url_for('blogs.index', page=page+1) }}" style="border-radius: 0 8px 8px 0; font-weight: 600;">Next</a>
            </li>
        </ul>
    </nav>
    {% endif %}
</div>
"""

html_content = html_content.replace('</div>\n{% endblock %}', pagination_html + '\n{% endblock %}')

with open('templates/blog_hub.html', 'w') as f:
    f.write(html_content)
