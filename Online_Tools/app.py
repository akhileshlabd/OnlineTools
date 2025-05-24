from flask import Flask, request, render_template, send_file, jsonify
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/resizer')
def resizer():
    return render_template('resizer.html')

@app.route('/resizer/resize', methods=['POST'])
def resize():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        width = request.form.get('width', type=int)
        height = request.form.get('height', type=int)
        keep_ratio = request.form.get('keep_ratio', 'false').lower() == 'true'

        if not width or not height or width <= 0 or height <= 0:
            return jsonify({'error': 'Width and height must be positive integers'}), 400

        img = Image.open(file.stream)
        orig_width, orig_height = img.size

        if keep_ratio:
            aspect_ratio = orig_width / orig_height
            if width / height > aspect_ratio:
                width = int(height * aspect_ratio)
            else:
                height = int(width / aspect_ratio)

        resized_img = img.resize((width, height), Image.LANCZOS)

        buf = io.BytesIO()

        orig_filename = file.filename
        name, ext = orig_filename.rsplit('.', 1)
        ext = ext.lower()

        if ext in ['jpg', 'jpeg']:
            save_format = 'JPEG'
            save_ext = 'jpg'
        elif ext == 'png':
            save_format = 'PNG'
            save_ext = 'png'
        elif ext == 'gif':
            save_format = 'GIF'
            save_ext = 'gif'
        else:
            save_format = 'PNG'
            save_ext = 'png'

        resized_img.save(buf, format=save_format)
        buf.seek(0)

        return send_file(
            buf,
            mimetype=f'image/{save_ext}',
            as_attachment=True,
            download_name=f"resized_{name}.{save_ext}"
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ---------------- PDF Merger ----------------
@app.route('/pdf-merger', methods=['GET', 'POST'])
def pdf_merger():
    if request.method == 'POST':
        files = request.files.getlist('pdfs')
        if not files or all(f.filename == '' for f in files):
            flash('No files selected. Please upload at least two PDFs.', 'danger')
            return redirect(request.url)

        pdfs = []
        for file in files:
            if file and allowed_file(file.filename, ALLOWED_PDF_EXTENSIONS):
                pdfs.append(file)
            else:
                flash(f"File {file.filename} is not a valid PDF.", 'danger')
                return redirect(request.url)

        if len(pdfs) < 2:
            flash('Please upload at least two PDF files to merge.', 'warning')
            return redirect(request.url)

        merger = PdfMerger()
        try:
            for pdf in pdfs:
                merger.append(pdf.stream)
            output_stream = io.BytesIO()
            merger.write(output_stream)
            merger.close()
            output_stream.seek(0)
            return send_file(
                output_stream,
                download_name='merged.pdf',
                as_attachment=True,
                mimetype='application/pdf'
            )
        except Exception as e:
            flash(f'Error merging PDFs: {str(e)}', 'danger')
            return redirect(request.url)

    return render_template('pdf_merger.html')

if __name__ == '__main__':
    app.run(debug=True)
