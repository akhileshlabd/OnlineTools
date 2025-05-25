from flask import Flask, request, render_template, send_file, jsonify,make_response
from PIL import Image
from PyPDF2 import PdfMerger
from weasyprint import HTML
import io

app = Flask(__name__)

# ---------------- Home ----------------
@app.route('/')
def home():
    return render_template('index.html')

# ---------------- Image Resizer ----------------
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
        name, ext = file.filename.rsplit('.', 1)
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
# --------------- Resume Builder -------------
@app.route('/resume_builder')
def resume_builder():
    return render_template('resume_builder.html')

@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    data = request.form.to_dict()
    rendered = render_template('resume_template.html', **data)
    pdf = HTML(string=rendered).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=resume.pdf'
    return response

@app.route('/preview_resume', methods=['POST'])
def preview_resume():
    data = {
        "name": request.form['name'],
        "job_title": request.form['job_title'],
        "contact": request.form['contact'],
        "profile": request.form['profile'],
        "experience": request.form['experience'],
        "education": request.form['education'],
        "skills": request.form['skills'],
    }
    return render_template('resume_template.html', **data)
# ---------------- PDF Merger ----------------
@app.route('/pdf-merger')
def pdf_merger_page():
    return render_template('pdf_merger.html')

@app.route('/pdf-merger/merge', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True)
