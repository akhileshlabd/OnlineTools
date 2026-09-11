from flask import Blueprint, render_template, request, jsonify, send_file, current_app
import io
from PyPDF2 import PdfMerger
from PIL import Image

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

@pdf_bp.route('/image-to-pdf', methods=['GET', 'POST'])
def image_to_pdf():  
    if request.method == 'POST':
        images = request.files.getlist('images')
        image_list = []

        for image_file in images:
            if image_file and allowed_file(image_file.filename):
                img = Image.open(image_file).convert('RGB')
                image_list.append(img)

        if image_list:
            pdf_io = io.BytesIO()
            image_list[0].save(pdf_io, format='PDF', save_all=True, append_images=image_list[1:])
            pdf_io.seek(0)
            return send_file(pdf_io, mimetype='application/pdf', as_attachment=True, download_name='converted.pdf')
        else:
            return "No valid images uploaded.", 400

    return render_template('image_to_pdf.html')

