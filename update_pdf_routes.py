import re

with open('routes/pdf.py', 'r') as f:
    content = f.read()

new_routes = """
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
"""

if "/lock-pdf" not in content:
    content = content.replace("PDF_TOOLS = {", new_routes + "\nPDF_TOOLS = {")

with open('routes/pdf.py', 'w') as f:
    f.write(content)
