import os
import json

BASE_DIR = '/Users/darsana/Online-Tools/OnlineTools'
ROUTES_DIR = os.path.join(BASE_DIR, 'routes')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# 1. Create Dynamic Tool Template
dynamic_tool_html = """{% extends "base.html" %}
{% block title %}{{ tool.name }} - Free Qube{% endblock %}
{% block content %}
<div class="tool-interface" style="max-width: 700px;">
    <div class="text-center mb-4">
        <h2 class="fw-bold">{{ tool.name }}</h2>
        <p class="text-muted">{{ tool.desc }}</p>
    </div>
    <form id="dynamicForm">
        {% if tool.type in ['image', 'pdf'] %}
        <div class="drag-drop-area mb-4" id="dropArea" onclick="document.getElementById('fileInput').click()">
            <i class="fas {{ tool.icon }} text-primary"></i>
            <h4>Select File</h4>
            <p class="text-muted mb-0">or drop file here</p>
            <input class="d-none" type="file" id="fileInput" name="file" accept="{% if tool.type == 'image' %}image/*{% else %}application/pdf{% endif %}" required>
        </div>
        <div id="fileInfoContainer" class="text-center mb-4 p-3 bg-light rounded shadow-sm border" style="display:none;">
            <h5 id="fileName" class="mb-1 text-truncate"></h5>
            <small class="text-muted" id="fileSize"></small>
        </div>
        {% endif %}

        {% if tool.inputs %}
        <div class="row g-3 justify-content-center mb-4" id="optionsContainer">
            {% for input in tool.inputs %}
            <div class="col-md-6">
                <label class="form-label fw-bold">{{ input.label }}</label>
                {% if input.type == 'textarea' %}
                <textarea class="form-control" name="{{ input.name }}" rows="4" required></textarea>
                {% else %}
                <input type="{{ input.type }}" class="form-control" name="{{ input.name }}" {% if input.min %}min="{{ input.min }}"{% endif %} {% if input.max %}max="{{ input.max }}"{% endif %} required>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        {% endif %}

        <div class="text-center">
            <button type="submit" class="btn btn-primary btn-lg rounded-pill px-5 fw-bold shadow-sm" id="submitBtn">
                <i class="fas fa-magic me-2"></i>Process
            </button>
        </div>
        <div class="text-center mt-3" id="spinnerContainer" style="display: none;">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-2 text-muted">Processing, please wait...</p>
        </div>
    </form>
</div>
{% endblock %}
{% block scripts %}
<script>
const form = document.getElementById('dynamicForm');
const fileInput = document.getElementById('fileInput');
const dropArea = document.getElementById('dropArea');
const submitBtn = document.getElementById('submitBtn');
const spinnerContainer = document.getElementById('spinnerContainer');

if (dropArea && fileInput) {
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const fileInfoContainer = document.getElementById('fileInfoContainer');

    dropArea.addEventListener('dragover', (e) => { e.preventDefault(); dropArea.classList.add('dragover'); });
    dropArea.addEventListener('dragleave', () => { dropArea.classList.remove('dragover'); });
    dropArea.addEventListener('drop', (e) => {
        e.preventDefault();
        dropArea.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            handleFileLoad();
        }
    });

    fileInput.addEventListener('change', handleFileLoad);

    function handleFileLoad() {
        if (fileInput.files && fileInput.files[0]) {
            const file = fileInput.files[0];
            fileName.textContent = file.name;
            fileSize.textContent = (file.size / 1024 / 1024).toFixed(2) + ' MB';
            fileInfoContainer.style.display = 'block';
        }
    }
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    spinnerContainer.style.display = 'block';
    submitBtn.disabled = true;
    
    const formData = new FormData(form);
    try {
        const response = await fetch("{{ tool.endpoint }}", {
            method: 'POST',
            body: formData
        });
        if (response.ok) {
            const blob = await response.blob();
            let downloadFilename = 'processed_file';
            const disposition = response.headers.get('Content-Disposition');
            if (disposition && disposition.indexOf('attachment') !== -1) {
                const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(disposition);
                if (matches != null && matches[1]) downloadFilename = matches[1].replace(/['"]/g, '');
            } else {
                {% if tool.type == 'image' %}
                downloadFilename = 'processed.png';
                {% elif tool.type == 'pdf' or tool.type == 'career' %}
                downloadFilename = 'document.pdf';
                {% endif %}
            }
            
            // Check if response is JSON (error)
            if (blob.type === 'application/json') {
                const text = await blob.text();
                const json = JSON.parse(text);
                alert('Error: ' + json.error);
                return;
            }

            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = downloadFilename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } else {
            const data = await response.json();
            alert('Error: ' + (data.error || 'Processing failed'));
        }
    } catch (error) {
        alert('An error occurred.');
    } finally {
        spinnerContainer.style.display = 'none';
        submitBtn.disabled = false;
    }
});
</script>
{% endblock %}
"""
with open(os.path.join(TEMPLATES_DIR, 'dynamic_tool.html'), 'w') as f:
    f.write(dynamic_tool_html)


# 2. Update routes/image.py
image_routes = """
from flask import Blueprint, render_template, request, jsonify, send_file
import io
from PIL import Image, ImageFilter, ImageEnhance
from werkzeug.utils import secure_filename

image_bp = Blueprint('image', __name__)

IMAGE_TOOLS = {
    'grayscale': {'id': 'grayscale', 'type': 'image', 'name': 'Grayscale Image', 'desc': 'Convert your image to black and white.', 'icon': 'fa-adjust', 'endpoint': '/image/process/grayscale', 'inputs': []},
    'blur': {'id': 'blur', 'type': 'image', 'name': 'Blur Image', 'desc': 'Apply a gaussian blur to your image.', 'icon': 'fa-tint', 'endpoint': '/image/process/blur', 'inputs': [{'name': 'radius', 'type': 'number', 'label': 'Blur Radius', 'min': 1, 'max': 50}]},
    'flip_h': {'id': 'flip_h', 'type': 'image', 'name': 'Flip Horizontal', 'desc': 'Mirror your image horizontally.', 'icon': 'fa-arrows-alt-h', 'endpoint': '/image/process/flip_h', 'inputs': []},
    'flip_v': {'id': 'flip_v', 'type': 'image', 'name': 'Flip Vertical', 'desc': 'Mirror your image vertically.', 'icon': 'fa-arrows-alt-v', 'endpoint': '/image/process/flip_v', 'inputs': []},
    'rotate_tool': {'id': 'rotate_tool', 'type': 'image', 'name': 'Rotate Image', 'desc': 'Rotate your image by any degree.', 'icon': 'fa-sync', 'endpoint': '/image/process/rotate_tool', 'inputs': [{'name': 'angle', 'type': 'number', 'label': 'Angle (Degrees)', 'min': -360, 'max': 360}]},
    'brightness': {'id': 'brightness', 'type': 'image', 'name': 'Adjust Brightness', 'desc': 'Change the brightness of your image.', 'icon': 'fa-sun', 'endpoint': '/image/process/brightness', 'inputs': [{'name': 'factor', 'type': 'number', 'label': 'Brightness Factor (1.0 = normal, 2.0 = double)', 'min': 0, 'max': 5}]},
    'contrast': {'id': 'contrast', 'type': 'image', 'name': 'Adjust Contrast', 'desc': 'Change the contrast of your image.', 'icon': 'fa-adjust', 'endpoint': '/image/process/contrast', 'inputs': [{'name': 'factor', 'type': 'number', 'label': 'Contrast Factor (1.0 = normal)', 'min': 0, 'max': 5}]}
}

# --- Legacy Custom Routes ---
@image_bp.route('/resizer')
def resizer(): return render_template('resizer.html')
@image_bp.route('/background_remover')
def background_remover(): return render_template('background_remover.html')
@image_bp.route('/converter')
def image_converter_page(): return render_template('image_converter.html')

# (Legacy endpoints implementation kept from original code for safety, abbreviated here for generation but we will patch them in)
"""
# I'll append the dynamic routes to the existing image.py instead of replacing to preserve complex legacy logic.
with open(os.path.join(ROUTES_DIR, 'image.py'), 'r') as f:
    existing_image = f.read()

dynamic_image_append = """
IMAGE_TOOLS = {
    'grayscale': {'id': 'grayscale', 'type': 'image', 'name': 'Grayscale Image', 'desc': 'Convert your image to black and white.', 'icon': 'fa-adjust', 'endpoint': '/image/process/grayscale', 'inputs': []},
    'blur': {'id': 'blur', 'type': 'image', 'name': 'Blur Image', 'desc': 'Apply a gaussian blur to your image.', 'icon': 'fa-tint', 'endpoint': '/image/process/blur', 'inputs': [{'name': 'radius', 'type': 'number', 'label': 'Blur Radius', 'min': 1, 'max': 50}]},
    'flip_h': {'id': 'flip_h', 'type': 'image', 'name': 'Flip Horizontal', 'desc': 'Mirror your image horizontally.', 'icon': 'fa-arrows-alt-h', 'endpoint': '/image/process/flip_h', 'inputs': []},
    'flip_v': {'id': 'flip_v', 'type': 'image', 'name': 'Flip Vertical', 'desc': 'Mirror your image vertically.', 'icon': 'fa-arrows-alt-v', 'endpoint': '/image/process/flip_v', 'inputs': []},
    'rotate_tool': {'id': 'rotate_tool', 'type': 'image', 'name': 'Rotate Image', 'desc': 'Rotate your image by any degree.', 'icon': 'fa-sync', 'endpoint': '/image/process/rotate_tool', 'inputs': [{'name': 'angle', 'type': 'number', 'label': 'Angle (Degrees)', 'min': -360, 'max': 360}]},
    'brightness': {'id': 'brightness', 'type': 'image', 'name': 'Adjust Brightness', 'desc': 'Change the brightness of your image.', 'icon': 'fa-sun', 'endpoint': '/image/process/brightness', 'inputs': [{'name': 'factor', 'type': 'number', 'label': 'Brightness Factor (1.0 = normal)', 'min': 0, 'max': 5}]},
    'contrast': {'id': 'contrast', 'type': 'image', 'name': 'Adjust Contrast', 'desc': 'Change the contrast of your image.', 'icon': 'fa-adjust', 'endpoint': '/image/process/contrast', 'inputs': [{'name': 'factor', 'type': 'number', 'label': 'Contrast Factor (1.0 = normal)', 'min': 0, 'max': 5}]}
}

@image_bp.route('/tool/<tool_id>')
def dynamic_image_tool(tool_id):
    tool = IMAGE_TOOLS.get(tool_id)
    if not tool: return "Tool not found", 404
    return render_template('dynamic_tool.html', tool=tool)

@image_bp.route('/process/<tool_id>', methods=['POST'])
def process_dynamic_image(tool_id):
    from PIL import ImageFilter, ImageEnhance
    if 'file' not in request.files: return jsonify({'error': 'No image uploaded'}), 400
    file = request.files['file']
    if file.filename == '': return jsonify({'error': 'No selected file'}), 400

    try:
        img = Image.open(file.stream)
        
        if tool_id == 'grayscale':
            img = img.convert('L')
        elif tool_id == 'blur':
            radius = float(request.form.get('radius', 2))
            img = img.filter(ImageFilter.GaussianBlur(radius))
        elif tool_id == 'flip_h':
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        elif tool_id == 'flip_v':
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
        elif tool_id == 'rotate_tool':
            angle = float(request.form.get('angle', 90))
            img = img.rotate(-angle, expand=True) # Negative so positive = clockwise
        elif tool_id == 'brightness':
            factor = float(request.form.get('factor', 1.0))
            img = ImageEnhance.Brightness(img).enhance(factor)
        elif tool_id == 'contrast':
            factor = float(request.form.get('factor', 1.0))
            img = ImageEnhance.Contrast(img).enhance(factor)
            
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        
        return send_file(buf, mimetype='image/png', as_attachment=True, download_name=f"processed_{tool_id}.png")
    except Exception as e:
        return jsonify({'error': str(e)}), 500
"""
with open(os.path.join(ROUTES_DIR, 'image.py'), 'a') as f:
    f.write(dynamic_image_append)


# 3. Update routes/pdf.py
dynamic_pdf_append = """
PDF_TOOLS = {
    'protect': {'id': 'protect', 'type': 'pdf', 'name': 'Protect PDF', 'desc': 'Encrypt your PDF with a password.', 'icon': 'fa-lock', 'endpoint': '/pdf-route/process/protect', 'inputs': [{'name': 'password', 'type': 'password', 'label': 'Password'}]},
    'unlock': {'id': 'unlock', 'type': 'pdf', 'name': 'Unlock PDF', 'desc': 'Remove password from a PDF.', 'icon': 'fa-unlock', 'endpoint': '/pdf-route/process/unlock', 'inputs': [{'name': 'password', 'type': 'password', 'label': 'Current Password'}]},
    'rotate_pdf': {'id': 'rotate_pdf', 'type': 'pdf', 'name': 'Rotate PDF', 'desc': 'Rotate all pages by 90, 180, or 270 degrees.', 'icon': 'fa-sync', 'endpoint': '/pdf-route/process/rotate_pdf', 'inputs': [{'name': 'angle', 'type': 'number', 'label': 'Angle (90, 180, 270)', 'min': 90, 'max': 270}]},
    'extract_text': {'id': 'extract_text', 'type': 'pdf', 'name': 'Extract Text', 'desc': 'Extract all text from a PDF file into a .txt file.', 'icon': 'fa-file-word', 'endpoint': '/pdf-route/process/extract_text', 'inputs': []},
    'remove_page': {'id': 'remove_page', 'type': 'pdf', 'name': 'Remove Page', 'desc': 'Delete a specific page from your PDF.', 'icon': 'fa-trash-alt', 'endpoint': '/pdf-route/process/remove_page', 'inputs': [{'name': 'page_num', 'type': 'number', 'label': 'Page Number to Remove', 'min': 1}]},
    'add_blank': {'id': 'add_blank', 'type': 'pdf', 'name': 'Add Blank Page', 'desc': 'Add a blank page to the end of the document.', 'icon': 'fa-plus-square', 'endpoint': '/pdf-route/process/add_blank', 'inputs': []},
    'metadata': {'id': 'metadata', 'type': 'pdf', 'name': 'Read Metadata', 'desc': 'Extract metadata (author, title) as text.', 'icon': 'fa-info-circle', 'endpoint': '/pdf-route/process/metadata', 'inputs': []}
}

@pdf_bp.route('/tool/<tool_id>')
def dynamic_pdf_tool(tool_id):
    tool = PDF_TOOLS.get(tool_id)
    if not tool: return "Tool not found", 404
    return render_template('dynamic_tool.html', tool=tool)

@pdf_bp.route('/process/<tool_id>', methods=['POST'])
def process_dynamic_pdf(tool_id):
    if 'file' not in request.files: return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if file.filename == '': return jsonify({'error': 'No selected file'}), 400

    try:
        reader = PdfReader(file.stream)
        writer = PdfWriter()
        
        if tool_id == 'extract_text':
            text = ""
            for page in reader.pages: text += page.extract_text() + "\\n"
            buf = io.BytesIO(text.encode('utf-8'))
            return send_file(buf, as_attachment=True, download_name="extracted_text.txt", mimetype='text/plain')
            
        elif tool_id == 'metadata':
            meta = reader.metadata
            text = str(meta) if meta else "No metadata found."
            buf = io.BytesIO(text.encode('utf-8'))
            return send_file(buf, as_attachment=True, download_name="metadata.txt", mimetype='text/plain')
            
        elif tool_id == 'protect':
            password = request.form.get('password', '')
            for page in reader.pages: writer.add_page(page)
            writer.encrypt(password)
            
        elif tool_id == 'unlock':
            password = request.form.get('password', '')
            if reader.is_encrypted:
                reader.decrypt(password)
            for page in reader.pages: writer.add_page(page)
            
        elif tool_id == 'rotate_pdf':
            angle = int(request.form.get('angle', 90))
            for page in reader.pages:
                page.rotate(angle)
                writer.add_page(page)
                
        elif tool_id == 'remove_page':
            page_num = int(request.form.get('page_num', 1)) - 1
            for i, page in enumerate(reader.pages):
                if i != page_num: writer.add_page(page)
                
        elif tool_id == 'add_blank':
            for page in reader.pages: writer.add_page(page)
            writer.add_blank_page()
            
        buf = io.BytesIO()
        writer.write(buf)
        buf.seek(0)
        
        return send_file(buf, as_attachment=True, download_name=f"processed_{tool_id}.pdf", mimetype='application/pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
"""
with open(os.path.join(ROUTES_DIR, 'pdf.py'), 'a') as f:
    f.write(dynamic_pdf_append)

# 4. Update routes/resume.py (Career Tools)
dynamic_career_append = """
CAREER_TOOLS = {
    'cover_letter': {'id': 'cover_letter', 'type': 'career', 'name': 'Cover Letter Builder', 'desc': 'Generate a professional cover letter.', 'icon': 'fa-envelope-open-text', 'endpoint': '/resume/process/cover_letter', 'inputs': [{'name': 'hiring_manager', 'type': 'text', 'label': 'Hiring Manager Name'}, {'name': 'company', 'type': 'text', 'label': 'Company Name'}, {'name': 'role', 'type': 'text', 'label': 'Target Role'}, {'name': 'skills', 'type': 'textarea', 'label': 'Key Skills & Why you are a fit'}]},
    'resignation': {'id': 'resignation', 'type': 'career', 'name': 'Resignation Letter', 'desc': 'Generate a standard two-week notice.', 'icon': 'fa-door-open', 'endpoint': '/resume/process/resignation', 'inputs': [{'name': 'manager', 'type': 'text', 'label': 'Manager Name'}, {'name': 'date', 'type': 'date', 'label': 'Last Day of Work'}]},
    'thank_you': {'id': 'thank_you', 'type': 'career', 'name': 'Interview Thank You', 'desc': 'Follow up professionally after an interview.', 'icon': 'fa-handshake', 'endpoint': '/resume/process/thank_you', 'inputs': [{'name': 'interviewer', 'type': 'text', 'label': 'Interviewer Name'}, {'name': 'role', 'type': 'text', 'label': 'Interviewed Role'}]},
    'cold_email': {'id': 'cold_email', 'type': 'career', 'name': 'Cold Outreach Email', 'desc': 'Template for networking with recruiters.', 'icon': 'fa-paper-plane', 'endpoint': '/resume/process/cold_email', 'inputs': [{'name': 'recruiter', 'type': 'text', 'label': 'Recruiter Name'}, {'name': 'company', 'type': 'text', 'label': 'Company'}, {'name': 'background', 'type': 'textarea', 'label': 'Brief Background'}]},
    'recommendation': {'id': 'recommendation', 'type': 'career', 'name': 'Letter of Recommendation', 'desc': 'Template for recommending a colleague.', 'icon': 'fa-star', 'endpoint': '/resume/process/recommendation', 'inputs': [{'name': 'person', 'type': 'text', 'label': 'Person You Are Recommending'}, {'name': 'relationship', 'type': 'text', 'label': 'Your Relationship (e.g. Manager)'}, {'name': 'strengths', 'type': 'textarea', 'label': 'Key Strengths'}]},
    'offer_negotiation': {'id': 'offer_negotiation', 'type': 'career', 'name': 'Salary Negotiation', 'desc': 'Professional email to negotiate an offer.', 'icon': 'fa-comments-dollar', 'endpoint': '/resume/process/offer_negotiation', 'inputs': [{'name': 'company', 'type': 'text', 'label': 'Company Name'}, {'name': 'current_offer', 'type': 'text', 'label': 'Current Offer'}, {'name': 'target_offer', 'type': 'text', 'label': 'Target Offer'}]},
    'promotion_request': {'id': 'promotion_request', 'type': 'career', 'name': 'Promotion Request', 'desc': 'Formal request for a promotion/raise.', 'icon': 'fa-arrow-up', 'endpoint': '/resume/process/promotion_request', 'inputs': [{'name': 'manager', 'type': 'text', 'label': 'Manager Name'}, {'name': 'achievements', 'type': 'textarea', 'label': 'Recent Key Achievements'}]},
    'reference_list': {'id': 'reference_list', 'type': 'career', 'name': 'Reference List Builder', 'desc': 'Generate a professional reference sheet.', 'icon': 'fa-users', 'endpoint': '/resume/process/reference_list', 'inputs': [{'name': 'references', 'type': 'textarea', 'label': 'List References (Name, Title, Email)'}]},
    'networking': {'id': 'networking', 'type': 'career', 'name': 'Networking Request', 'desc': 'Ask for a coffee chat or informational interview.', 'icon': 'fa-coffee', 'endpoint': '/resume/process/networking', 'inputs': [{'name': 'contact', 'type': 'text', 'label': 'Contact Name'}, {'name': 'topic', 'type': 'text', 'label': 'Topic to Discuss'}]}
}

@resume_bp.route('/tool/<tool_id>')
def dynamic_career_tool(tool_id):
    tool = CAREER_TOOLS.get(tool_id)
    if not tool: return "Tool not found", 404
    return render_template('dynamic_tool.html', tool=tool)

@resume_bp.route('/process/<tool_id>', methods=['POST'])
def process_dynamic_career(tool_id):
    from weasyprint import HTML
    import io
    from flask import send_file
    
    form_data = request.form.to_dict()
    
    # Generic template rendering
    html_content = f"<html><body style='font-family: Arial, sans-serif; padding: 40px; line-height: 1.6;'>"
    html_content += f"<h1 style='color: #333; border-bottom: 2px solid #ccc; padding-bottom: 10px;'>{tool_id.replace('_', ' ').title()}</h1>"
    
    for key, value in form_data.items():
        html_content += f"<h3 style='margin-bottom: 5px; color: #555;'>{key.replace('_', ' ').title()}:</h3>"
        html_content += f"<p style='margin-top: 0; white-space: pre-wrap;'>{value}</p>"
        
    html_content += "</body></html>"
    
    pdf_bytes = HTML(string=html_content).write_pdf()
    buf = io.BytesIO(pdf_bytes)
    
    return send_file(buf, as_attachment=True, download_name=f"{tool_id}.pdf", mimetype='application/pdf')
"""
with open(os.path.join(ROUTES_DIR, 'resume.py'), 'a') as f:
    f.write(dynamic_career_append)

print("Engine generation complete.")
