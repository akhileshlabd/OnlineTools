from flask import Blueprint, render_template, request, jsonify, send_file, current_app
import io
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PIL import Image
from werkzeug.utils import secure_filename

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
