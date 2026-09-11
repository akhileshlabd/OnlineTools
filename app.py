from flask import Flask, render_template, send_from_directory
import os

from routes.pdf import pdf_bp
from routes.image import image_bp
from routes.resume import resume_bp

app = Flask(__name__)

# Global configs & Best Practices
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 # 50 MB max file size limit to protect the server

# Register Blueprints
app.register_blueprint(pdf_bp)
app.register_blueprint(image_bp)
app.register_blueprint(resume_bp)

# ---------------- Home ----------------
@app.route('/')
def home():
    return render_template('index.html')

# ---------------- AdSense ----------------
@app.route('/ads.txt')
def static_from_root():
    return send_from_directory(app.static_folder, 'ads.txt')

if __name__ == '__main__':
    # Ensure upload folder exists just in case it's used elsewhere
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
