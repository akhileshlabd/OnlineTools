from flask import Blueprint, render_template, request, jsonify, send_file, current_app
import io
import os
import subprocess
import tempfile
import zipfile
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PIL import Image
from werkzeug.utils import secure_filename
# Additional libraries for new PDF tools
import pandas as pd
from pdf2docx import Converter
from tabula import read_pdf
from pdf2image import convert_from_bytes
import pytesseract
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

pdf_bp = Blueprint('pdf', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@pdf_bp.route('/pdf-merger')
def pdf_merger_page():
    return render_template('pdf_merger.html')

@pdf_bp.route('/pdf-merger/merge', methods=['POST'])
def pdf_merge():
    try:
        files = request.files.getlist('pdfs[]')
        order = request.form.getlist('order[]')

        if not files or len(files) < 2:
            return jsonify({'error': 'Please upload at least two PDF files'}), 400

        sorted_files = sorted(zip(order, files), key=lambda x: int(x[0]))

        merger = PdfMerger()
        for _, file in sorted_files:
            merger.append(file.stream)

        output = io.BytesIO()
        merger.write(output)
        merger.close()
        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name='merged.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pdf_bp.route('/pdf-splitter')
def pdf_splitter_page():
    return render_template('pdf_split.html')

@pdf_bp.route('/pdf-splitter/split', methods=['POST'])
def pdf_split():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF uploaded'}), 400
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        start_page = int(request.form.get('start_page', 1))
        end_page = request.form.get('end_page')

        reader = PdfReader(file.stream)
        total_pages = len(reader.pages)

        end_page = int(end_page) if end_page else total_pages

        if start_page < 1 or end_page > total_pages or start_page > end_page:
            return jsonify({'error': f"Invalid page range. Document has {total_pages} pages."}), 400

        writer = PdfWriter()
        # PyPDF2 uses 0-based indexing
        for i in range(start_page - 1, end_page):
            writer.add_page(reader.pages[i])

        output = io.BytesIO()
        writer.write(output)
        output.seek(0)
        
        filename = secure_filename(file.filename)
        name = filename.rsplit('.', 1)[0] if '.' in filename else 'document'

        return send_file(
            output,
            as_attachment=True,
            download_name=f"{name}_pages_{start_page}_to_{end_page}.pdf",
            mimetype='application/pdf'
        )
    except ValueError:
        return jsonify({'error': "Invalid page numbers provided."}), 400
    except Exception as e:
        return jsonify({'error': f"Failed to split PDF: {str(e)}"}), 500


@pdf_bp.route('/image-to-pdf', methods=['GET', 'POST'])
def image_to_pdf():  
    if request.method == 'POST':
        images = request.files.getlist('images')
        image_list = []

        for image_file in images:
            if image_file and allowed_file(image_file.filename):
                try:
                    img = Image.open(image_file).convert('RGB')
                    image_list.append(img)
                except Exception:
                    continue # Skip invalid images to prevent crashing

        if image_list:
            pdf_io = io.BytesIO()
            image_list[0].save(pdf_io, format='PDF', save_all=True, append_images=image_list[1:])
            pdf_io.seek(0)
            return send_file(pdf_io, mimetype='application/pdf', as_attachment=True, download_name='converted_images.pdf')
        else:
            return "No valid images uploaded.", 400

    return render_template('image_to_pdf.html')

PDF_TOOLS = {
    'protect': {'id': 'protect', 'type': 'pdf', 'name': 'Protect PDF', 'desc': 'Encrypt your PDF with a password.', 'icon': 'fa-lock', 'endpoint': '/pdf-process/protect', 'inputs': [{'name': 'password', 'type': 'password', 'label': 'Password'}]},
    'unlock': {'id': 'unlock', 'type': 'pdf', 'name': 'Unlock PDF', 'desc': 'Remove password from a PDF.', 'icon': 'fa-unlock', 'endpoint': '/pdf-process/unlock', 'inputs': [{'name': 'password', 'type': 'password', 'label': 'Current Password'}]},
    'rotate_pdf': {'id': 'rotate_pdf', 'type': 'pdf', 'name': 'Rotate PDF', 'desc': 'Rotate all pages by 90, 180, or 270 degrees.', 'icon': 'fa-sync', 'endpoint': '/pdf-process/rotate_pdf', 'inputs': [{'name': 'angle', 'type': 'number', 'label': 'Angle (90, 180, 270)', 'min': 90, 'max': 270}]},
    'extract_text': {'id': 'extract_text', 'type': 'pdf', 'name': 'Extract Text', 'desc': 'Extract all text from a PDF file into a .txt file.', 'icon': 'fa-file-word', 'endpoint': '/pdf-process/extract_text', 'inputs': []},
    'remove_page': {'id': 'remove_page', 'type': 'pdf', 'name': 'Remove Page', 'desc': 'Delete a specific page from your PDF.', 'icon': 'fa-trash-alt', 'endpoint': '/pdf-process/remove_page', 'inputs': [{'name': 'page_num', 'type': 'number', 'label': 'Page Number to Remove', 'min': 1}]},
    'add_blank': {'id': 'add_blank', 'type': 'pdf', 'name': 'Add Blank Page', 'desc': 'Add a blank page to the end of the document.', 'icon': 'fa-plus-square', 'endpoint': '/pdf-process/add_blank', 'inputs': []},
    'metadata': {'id': 'metadata', 'type': 'pdf', 'name': 'Read Metadata', 'desc': 'Extract metadata (author, title) as text.', 'icon': 'fa-info-circle', 'endpoint': '/pdf-process/metadata', 'inputs': []},
    # New PDF tools added to match iLovePDF features
    'compress': {'id': 'compress', 'type': 'pdf', 'name': 'Compress PDF', 'desc': 'Reduce PDF file size.', 'icon': 'fa-compress', 'endpoint': '/pdf-process/compress', 'inputs': []},
    'convert_word': {'id': 'convert_word', 'type': 'pdf', 'name': 'PDF to Word', 'desc': 'Convert PDF to DOCX.', 'icon': 'fa-file-word', 'endpoint': '/pdf-process/convert_word', 'inputs': []},
    'convert_excel': {'id': 'convert_excel', 'type': 'pdf', 'name': 'PDF to Excel', 'desc': 'Convert PDF to XLSX.', 'icon': 'fa-file-excel', 'endpoint': '/pdf-process/convert_excel', 'inputs': []},
    'watermark': {'id': 'watermark', 'type': 'pdf', 'name': 'Add Watermark', 'desc': 'Add text or image watermark.', 'icon': 'fa-water', 'endpoint': '/pdf-process/watermark', 'inputs': [{'name': 'watermark_text', 'type': 'text', 'label': 'Watermark Text'}]},
    'ocr': {'id': 'ocr', 'type': 'pdf', 'name': 'PDF OCR', 'desc': 'Extract text via OCR.', 'icon': 'fa-magnifying-glass', 'endpoint': '/pdf-process/ocr', 'inputs': []},
    'extract_images': {'id': 'extract_images', 'type': 'pdf', 'name': 'Extract Images', 'desc': 'Extract all images from PDF.', 'icon': 'fa-image', 'endpoint': '/pdf-process/extract_images', 'inputs': []},
    'optimize': {'id': 'optimize', 'type': 'pdf', 'name': 'Optimize PDF', 'desc': 'Remove metadata and compress streams.', 'icon': 'fa-wrench', 'endpoint': '/pdf-process/optimize', 'inputs': []},
}

@pdf_bp.route('/pdf-tool/<tool_id>')
def dynamic_pdf_tool(tool_id):
    tool = PDF_TOOLS.get(tool_id)
    if not tool: return "Tool not found", 404
    return render_template('dynamic_tool.html', tool=tool)

@pdf_bp.route('/pdf-process/<tool_id>', methods=['POST'])
def process_dynamic_pdf(tool_id):
    if 'file' not in request.files: return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if file.filename == '': return jsonify({'error': 'No selected file'}), 400

    try:
        reader = PdfReader(file.stream)
        writer = PdfWriter()

        if tool_id == 'extract_text':
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            buf = io.BytesIO(text.encode('utf-8'))
            return send_file(buf, as_attachment=True, download_name="extracted_text.txt", mimetype='text/plain')

        elif tool_id == 'metadata':
            meta = reader.metadata
            text = str(meta) if meta else "No metadata found."
            buf = io.BytesIO(text.encode('utf-8'))
            return send_file(buf, as_attachment=True, download_name="metadata.txt", mimetype='text/plain')

        elif tool_id == 'protect':
            password = request.form.get('password', '')
            for page in reader.pages:
                writer.add_page(page)
            writer.encrypt(password)

        elif tool_id == 'unlock':
            password = request.form.get('password', '')
            if reader.is_encrypted:
                reader.decrypt(password)
            for page in reader.pages:
                writer.add_page(page)

        elif tool_id == 'rotate_pdf':
            angle = int(request.form.get('angle', 90))
            for page in reader.pages:
                page.rotate(angle)
                writer.add_page(page)

        elif tool_id == 'remove_page':
            page_num = int(request.form.get('page_num', 1)) - 1
            for i, page in enumerate(reader.pages):
                if i != page_num:
                    writer.add_page(page)

        elif tool_id == 'add_blank':
            for page in reader.pages:
                writer.add_page(page)
            writer.add_blank_page()

        # New tool implementations
        elif tool_id == 'compress':
            import subprocess, tempfile, os
            # Save uploaded PDF to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as src_tmp:
                src_tmp.write(file.read())
                src_tmp.flush()
                src_path = src_tmp.name
            out_path = src_path + '_compressed.pdf'
            gs_cmd = [
                'gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                '-dPDFSETTINGS=/ebook', '-dNOPAUSE', '-dQUIET', '-dBATCH',
                f'-sOutputFile={out_path}', src_path
            ]
            subprocess.run(gs_cmd, check=True)
            with open(out_path, 'rb') as f_out:
                compressed = io.BytesIO(f_out.read())
            os.remove(src_path)
            os.remove(out_path)
            compressed.seek(0)
            return send_file(compressed, as_attachment=True, download_name='compressed.pdf', mimetype='application/pdf')

        elif tool_id == 'convert_word':
            from pdf2docx import Converter
            import tempfile, os
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as src_tmp:
                src_tmp.write(file.read())
                src_tmp.flush()
                src_path = src_tmp.name
            docx_path = src_path + '.docx'
            cv = Converter(src_path)
            cv.convert(docx_path, start=0, end=None)
            cv.close()
            with open(docx_path, 'rb') as f_docx:
                docx_io = io.BytesIO(f_docx.read())
            os.remove(src_path)
            os.remove(docx_path)
            docx_io.seek(0)
            return send_file(docx_io, as_attachment=True, download_name='converted.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

        elif tool_id == 'convert_excel':
            import pandas as pd, tempfile, os
            from tabula import read_pdf
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as src_tmp:
                src_tmp.write(file.read())
                src_tmp.flush()
                src_path = src_tmp.name
            dfs = read_pdf(src_path, pages='all')
            os.remove(src_path)
            if not dfs:
                return jsonify({'error': 'No tables found in PDF'}), 400
            df = pd.concat(dfs, ignore_index=True)
            excel_io = io.BytesIO()
            with pd.ExcelWriter(excel_io, engine='openpyxl') as writer_excel:
                df.to_excel(writer_excel, index=False, sheet_name='Sheet1')
            excel_io.seek(0)
            return send_file(excel_io, as_attachment=True, download_name='converted.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        elif tool_id == 'watermark':
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            watermark_text = request.form.get('watermark_text', '')
            wm_io = io.BytesIO()
            c = canvas.Canvas(wm_io, pagesize=letter)
            c.setFont('Helvetica', 40)
            c.setFillAlpha(0.3)
            c.saveState()
            c.translate(300, 400)
            c.rotate(45)
            c.drawCentredString(0, 0, watermark_text)
            c.restoreState()
            c.save()
            wm_io.seek(0)
            watermark_reader = PdfReader(wm_io)
            for page in reader.pages:
                page.merge_page(watermark_reader.pages[0])
                writer.add_page(page)

        elif tool_id == 'ocr':
            from pdf2image import convert_from_bytes
            import pytesseract
            images = convert_from_bytes(file.read())
            text = ''
            for img in images:
                text += pytesseract.image_to_string(img) + '\n'
            buf = io.BytesIO(text.encode('utf-8'))
            return send_file(buf, as_attachment=True, download_name='ocr_text.txt', mimetype='text/plain')

        elif tool_id == 'extract_images':
            from pdf2image import convert_from_bytes
            import zipfile
            images = convert_from_bytes(file.read())
            zip_io = io.BytesIO()
            with zipfile.ZipFile(zip_io, 'w') as zipf:
                for i, img in enumerate(images, start=1):
                    img_bytes = io.BytesIO()
                    img.save(img_bytes, format='PNG')
                    img_bytes.seek(0)
                    zipf.writestr(f'page_{i}.png', img_bytes.read())
            zip_io.seek(0)
            return send_file(zip_io, as_attachment=True, download_name='extracted_images.zip', mimetype='application/zip')

        elif tool_id == 'optimize':
            for page in reader.pages:
                writer.add_page(page)
            # Metadata is omitted by not copying it
            buf = io.BytesIO()
            writer.write(buf)
            buf.seek(0)
            return send_file(buf, as_attachment=True, download_name='optimized.pdf', mimetype='application/pdf')

        else:
            # Existing processing paths fall through to generic writer below
            pass

        buf = io.BytesIO()
        writer.write(buf)
        buf.seek(0)
        return send_file(buf, as_attachment=True, download_name=f"processed_{tool_id}.pdf", mimetype='application/pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
