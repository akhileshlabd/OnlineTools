from flask import Blueprint, render_template

pdf_bp = Blueprint('pdf', __name__, url_prefix='/pdf')

@pdf_bp.route('/pdf-merger', methods=['GET'])
def pdf_merger():
    return render_template('pdf_merger.html')

@pdf_bp.route('/pdf-splitter', methods=['GET'])
def pdf_splitter():
    return render_template('pdf_split.html')

@pdf_bp.route("/word-to-pdf", methods=["GET"])
def word_to_pdf():
    return render_template("word_to_pdf.html")

@pdf_bp.route("/excel-to-pdf", methods=["GET"])
def excel_to_pdf():
    return render_template("excel_to_pdf.html")

@pdf_bp.route('/image-to-pdf', methods=['GET'])
def image_to_pdf():  
    return render_template('image_to_pdf.html')


import io
import PyPDF2
from flask import request, send_file, make_response

@pdf_bp.route('/lock-pdf', methods=['GET'])
def lock_pdf():
    return render_template('lock_pdf.html')

@pdf_bp.route('/unlock-pdf', methods=['GET'])
def unlock_pdf():
    return render_template('unlock_pdf.html')

@pdf_bp.route('/api/lock-pdf', methods=['POST'])
def api_lock_pdf():
    if 'pdf' not in request.files:
        return "No PDF file provided", 400
    password = request.form.get('password')
    if not password:
        return "No password provided", 400
        
    file = request.files['pdf']
    try:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
            
        writer.encrypt(password)
        
        output = io.BytesIO()
        writer.write(output)
        output.seek(0)
        
        return send_file(output, as_attachment=True, download_name=f"locked_{file.filename}", mimetype="application/pdf")
    except Exception as e:
        return str(e), 500

@pdf_bp.route('/api/unlock-pdf', methods=['POST'])
def api_unlock_pdf():
    if 'pdf' not in request.files:
        return "No PDF file provided", 400
    password = request.form.get('password')
    if not password:
        return "No password provided", 400
        
    file = request.files['pdf']
    try:
        reader = PyPDF2.PdfReader(file)
        if reader.is_encrypted:
            success = reader.decrypt(password)
            if not success:
                return "Incorrect password", 401
                
        writer = PyPDF2.PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
            
        output = io.BytesIO()
        writer.write(output)
        output.seek(0)
        
        return send_file(output, as_attachment=True, download_name=f"unlocked_{file.filename}", mimetype="application/pdf")
    except Exception as e:
        return str(e), 500

PDF_TOOLS = {
    'rotate_pdf': {'id': 'rotate_pdf', 'type': 'pdf', 'name': 'Rotate PDF', 'desc': 'Rotate all pages by 90, 180, or 270 degrees.', 'icon': 'fa-sync', 'inputs': [{'name': 'angle', 'type': 'number', 'label': 'Angle (90, 180, 270)', 'min': 90, 'max': 270}]},
    'remove_page': {'id': 'remove_page', 'type': 'pdf', 'name': 'Remove Page', 'desc': 'Delete a specific page from your PDF.', 'icon': 'fa-trash-alt', 'inputs': [{'name': 'page_num', 'type': 'number', 'label': 'Page Number to Remove', 'min': 1}]},
    'add_blank': {'id': 'add_blank', 'type': 'pdf', 'name': 'Add Blank Page', 'desc': 'Add a blank page to the end of the document.', 'icon': 'fa-plus-square', 'inputs': []},
    'watermark': {'id': 'watermark', 'type': 'pdf', 'name': 'Add Watermark', 'desc': 'Add text or image watermark.', 'icon': 'fa-water', 'inputs': [{'name': 'watermark_text', 'type': 'text', 'label': 'Watermark Text'}]}
}

@pdf_bp.route('/pdf-tool/<tool_id>')
def dynamic_pdf_tool(tool_id):
    tool = PDF_TOOLS.get(tool_id)
    if not tool: return "Tool not found", 404
    return render_template('dynamic_tool.html', tool=tool)

@pdf_bp.route('/')
def pdf_hub():
    return render_template('hub_pdf.html', pdf_tools=PDF_TOOLS)
