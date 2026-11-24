from flask import Flask, render_template, send_from_directory, request, g, make_response, redirect, url_for
import json
import os

from routes.pdf import pdf_bp, PDF_TOOLS
from routes.image import image_bp, IMAGE_TOOLS
from routes.code import code_bp, CODE_TOOLS
from routes.video import video_bp, VIDEO_TOOLS
from routes.admin import admin_bp
from routes.blogs import blogs_bp
from routes.learn import learn_bp

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "default-secret-key-for-admin-otp")

# Global configs & Best Practices
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 # 50 MB max file size limit to protect the server

# --- AUTHORITATIVE ENGLISH ENGINE (MULTI-LANG CONSOLIDATED) ---
try:
    with open('translations.json', 'r', encoding='utf-8') as f:
        TRANSLATIONS = json.load(f)
except Exception as e:
    TRANSLATIONS = {}

SUPPORTED_LANGUAGES = {'en': 'English'}

@app.before_request
def handle_language_and_redirects():
    if request.path == '/health':
        return None
    # If any query parameter lang= is requested, redirect 301 to the clean canonical path
    if request.args.get('lang'):
        return redirect(request.path, code=301)
    g.lang = 'en'

@app.context_processor
def inject_translations():
    def t(key):
        if key in TRANSLATIONS and 'en' in TRANSLATIONS[key]:
            return TRANSLATIONS[key]['en']
        return key
    return dict(t=t, current_lang='en', supported_langs=SUPPORTED_LANGUAGES, year=2026)
# -------------------------------------------------------------

# Register Surviving Core Blueprints
app.register_blueprint(pdf_bp)
app.register_blueprint(image_bp)
app.register_blueprint(code_bp)
app.register_blueprint(video_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(blogs_bp)
app.register_blueprint(learn_bp)

# --- 301 PERMANENT REDIRECTS FOR PRUNED THIN PAGES ---
@app.route('/finance')
@app.route('/finance/')
@app.route('/finance/<path:subpath>')
def redirect_finance(subpath=None):
    return redirect('/blog/how-sip-returns-are-calculated-formula-real-examples', code=301)

@app.route('/text')
@app.route('/text/')
@app.route('/text/<path:subpath>')
def redirect_text(subpath=None):
    return redirect('/dev/', code=301)

@app.route('/network')
@app.route('/network/')
@app.route('/network/<path:subpath>')
def redirect_network(subpath=None):
    return redirect('/dev/', code=301)

@app.route('/math')
@app.route('/math/')
@app.route('/math/<path:subpath>')
def redirect_math(subpath=None):
    return redirect('/', code=301)

@app.route('/health')
def health_check():
    from flask import jsonify
    return jsonify({"status": "ok"}), 200

@app.route('/health/')
@app.route('/health/<path:subpath>')
def redirect_health(subpath=None):
    return redirect('/', code=301)

@app.route('/es')
@app.route('/es/<path:subpath>')
@app.route('/pt')
@app.route('/pt/<path:subpath>')
@app.route('/hi')
@app.route('/hi/<path:subpath>')
def redirect_multilang(subpath=None):
    if subpath:
        return redirect(f'/{subpath}', code=301)
    return redirect('/', code=301)

@app.route('/privacy-policy')
def redirect_privacy_policy():
    return redirect('/privacy', code=301)

@app.route('/blog/how-to-remove-pdf-owner-passwords-safely-for-editing-printing')
def redirect_removed_pdf_pw_blog():
    return redirect('/blog/', code=301)

@app.route('/pdf')
def redirect_pdf_shorthand():
    return redirect('/pdf/', code=301)

@app.route('/mobiles')
@app.route('/mobiles/')
def redirect_mobiles():
    return redirect('/', code=301)

# Shorthand & legacy redirects
@app.route('/code')
@app.route('/code/<path:subpath>')
def redirect_code_shorthand(subpath=None):
    if subpath and subpath in CODE_TOOLS:
        return redirect(url_for('code.code_tool_page', tool_id=subpath), code=301)
    return redirect(url_for('code.code_hub'), code=301)

# ---------------- Home ----------------
@app.route('/')
def home():
    from routes.blogs import get_db_connection
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, title, slug, created_at, image_path FROM blogs WHERE is_hidden = 0 ORDER BY created_at DESC LIMIT 3")
    latest_blogs = c.fetchall()
    conn.close()

    return render_template('index.html',
                           image_tools=IMAGE_TOOLS,
                           pdf_tools=PDF_TOOLS,
                           code_tools=CODE_TOOLS,
                           video_tools=VIDEO_TOOLS,
                           latest_blogs=latest_blogs)

# ---------------- Legal & Policy Pages ----------------
@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/sitemap.xml')
def sitemap():
    from routes.blogs import get_db_connection
    
    # Fetch active blogs for sitemap
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT slug, created_at FROM blogs WHERE is_hidden = 0 ORDER BY created_at DESC")
    blogs = c.fetchall()
    conn.close()

    template = render_template('sitemap.xml',
                               pdf_tools=PDF_TOOLS,
                               image_tools=IMAGE_TOOLS,
                               code_tools=CODE_TOOLS,
                               video_tools=VIDEO_TOOLS,
                               blogs=blogs)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html')

# ---------------- SEO & Webmaster Endpoints ----------------
@app.route('/ads.txt')
def ads_txt():
    ads_content = os.environ.get('ADS_TXT_CONTENT')
    if not ads_content:
        ads_path = os.path.join(app.static_folder, 'ads.txt')
        if os.path.exists(ads_path):
            try:
                with open(ads_path, 'r', encoding='utf-8') as f:
                    ads_content = f.read()
            except Exception:
                ads_content = "google.com, pub-7852131472234228, DIRECT, f08c47fec0942fa0\n"
        else:
            ads_content = "google.com, pub-7852131472234228, DIRECT, f08c47fec0942fa0\n"
    from flask import Response
    return Response(ads_content, status=200, mimetype='text/plain')

@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route('/sw.js')
def sw():
    from flask import make_response
    response = make_response(send_from_directory(app.static_folder, 'sw.js'))
    response.headers['Cache-Control'] = 'no-cache'
    return response


import sqlite3
from collections import defaultdict

@app.context_processor
def inject_features():
    try:
        conn = sqlite3.connect('blogs.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT key, value FROM settings WHERE key LIKE 'feature_%'")
        rows = c.fetchall()
        conn.close()
        
        features = defaultdict(lambda: True)
        for r in rows:
            features[r['key']] = (r['value'] == '1')
        return dict(features=features)
    except:
        return dict(features=defaultdict(lambda: True))


if __name__ == '__main__':
    # Ensure upload folder exists just in case it's used elsewhere
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
