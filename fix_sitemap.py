import re

with open('app.py', 'r') as f:
    content = f.read()

# Define the new function
new_func = """@app.route('/sitemap.xml')
def sitemap():
    import sqlite3
    from routes.blogs import get_db_connection
    from flask import make_response
    
    # Fetch blogs for sitemap
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT slug, created_at FROM blogs WHERE is_hidden = 0")
    blogs = c.fetchall()
    conn.close()

    template = render_template('sitemap.xml',
                               pdf_tools=PDF_TOOLS,
                               image_tools=IMAGE_TOOLS,
                               finance_tools=FINANCE_TOOLS,
                               code_tools=CODE_TOOLS,
                               text_tools=TEXT_TOOLS,
                               health_tools=HEALTH_TOOLS,
                               math_tools=MATH_TOOLS,
                               network_tools=NETWORK_TOOLS,
                               games_tools=GAMES_TOOLS,
                               video_tools=VIDEO_TOOLS,
                               blogs=blogs)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response"""

# Replace existing sitemap function
# Find where it starts and ends
start = content.find("@app.route('/sitemap.xml')")
if start != -1:
    end = content.find("return response", start) + 15
    new_content = content[:start] + new_func + content[end:]
    with open('app.py', 'w') as f:
        f.write(new_content)
