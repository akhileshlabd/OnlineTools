from flask import Flask, render_template, send_from_directory
import os

from routes.pdf import pdf_bp, PDF_TOOLS
from routes.image import image_bp, IMAGE_TOOLS
from routes.finance import finance_bp, FINANCE_TOOLS
from routes.code import code_bp, CODE_TOOLS

app = Flask(__name__)

# Global configs & Best Practices
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 # 50 MB max file size limit to protect the server

# Register Blueprints
app.register_blueprint(pdf_bp)
app.register_blueprint(image_bp)
app.register_blueprint(finance_bp)
app.register_blueprint(code_bp)

# ---------------- Home ----------------
@app.route('/')
def home():
    return render_template('index.html', image_tools=IMAGE_TOOLS, pdf_tools=PDF_TOOLS, finance_tools=FINANCE_TOOLS, code_tools=CODE_TOOLS)

# ---------------- Legal / Policies (AdSense Compliance) ----------------
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

@app.route('/sitemap.xml')
def sitemap_xml():
    return send_from_directory(app.static_folder, 'sitemap.xml')

if __name__ == '__main__':
    # Ensure upload folder exists just in case it's used elsewhere
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
