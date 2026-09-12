from flask import Flask, render_template, send_from_directory, request, g, make_response
import json

import os

from routes.pdf import pdf_bp, PDF_TOOLS
from routes.image import image_bp, IMAGE_TOOLS
from routes.finance import finance_bp, FINANCE_TOOLS
from routes.code import code_bp, CODE_TOOLS
from routes.text import text_bp, TEXT_TOOLS
from routes.health import health_bp, HEALTH_TOOLS
from routes.math import math_bp, MATH_TOOLS
from routes.network import network_bp, NETWORK_TOOLS
from routes.games import games_bp, GAMES_TOOLS
from routes.kids import kids_bp, KIDS_TOOLS


app = Flask(__name__)

# Global configs & Best Practices
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 # 50 MB max file size limit to protect the server

# --- MULTI-LANGUAGE SEO ENGINE ---
try:
    with open('translations.json', 'r', encoding='utf-8') as f:
        TRANSLATIONS = json.load(f)
except Exception as e:
    TRANSLATIONS = {}

SUPPORTED_LANGUAGES = {'en': 'English', 'es': 'Español', 'pt': 'Português', 'hi': 'हिन्दी'}

@app.before_request
def set_language():
    lang = request.args.get('lang')
    if lang in SUPPORTED_LANGUAGES:
        g.lang = lang
    else:
        g.lang = request.cookies.get('lang', 'en')
        if g.lang not in SUPPORTED_LANGUAGES:
            g.lang = 'en'

@app.context_processor
def inject_translations():
    def t(key):
        if key in TRANSLATIONS and g.lang in TRANSLATIONS[key]:
            return TRANSLATIONS[key][g.lang]
        if key in TRANSLATIONS and 'en' in TRANSLATIONS[key]:
            return TRANSLATIONS[key]['en']
        return key
    return dict(t=t, current_lang=g.lang, supported_langs=SUPPORTED_LANGUAGES)
# ---------------------------------

# Register Blueprints
app.register_blueprint(pdf_bp)
app.register_blueprint(image_bp)
app.register_blueprint(finance_bp)
app.register_blueprint(code_bp)
app.register_blueprint(text_bp)
app.register_blueprint(health_bp)
app.register_blueprint(math_bp)
app.register_blueprint(network_bp)
app.register_blueprint(games_bp)
app.register_blueprint(kids_bp)


# ---------------- Home ----------------
@app.route('/')
def home():
    return render_template('index.html', image_tools=IMAGE_TOOLS, pdf_tools=PDF_TOOLS, finance_tools=FINANCE_TOOLS, code_tools=CODE_TOOLS, text_tools=TEXT_TOOLS, health_tools=HEALTH_TOOLS, math_tools=MATH_TOOLS, network_tools=NETWORK_TOOLS, games_tools=GAMES_TOOLS, kids_tools=KIDS_TOOLS)

# ---------------- Legal / Policies (AdSense Compliance) ----------------
@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/sitemap.xml')
def sitemap():
    from flask import make_response
    template = render_template('sitemap.xml', 
                               pdf_tools=PDF_TOOLS, 
                               image_tools=IMAGE_TOOLS, 
                               finance_tools=FINANCE_TOOLS, 
                               code_tools=CODE_TOOLS, 
                               text_tools=TEXT_TOOLS, 
                               health_tools=HEALTH_TOOLS, 
                               math_tools=MATH_TOOLS,
                               network_tools=NETWORK_TOOLS,
                               games_tools=GAMES_TOOLS)
    response = make_response(template)
    response.headers["Content-Type"] = "application/xml"
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

# ---------------- AdSense & SEO ----------------
@app.route('/ads.txt')
def ads_txt():
    return send_from_directory(app.static_folder, 'ads.txt')

@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route('/sw.js')
def sw():
    from flask import make_response
    response = make_response(send_from_directory(app.static_folder, 'sw.js'))
    response.headers['Cache-Control'] = 'no-cache'
    return response

if __name__ == '__main__':
    # Ensure upload folder exists just in case it's used elsewhere
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
