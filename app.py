from flask import Flask, request, render_template, send_file, jsonify,make_response
from PIL import Image
from PyPDF2 import PdfMerger
from weasyprint import HTML
import io
# from rembg import remove

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

# @app.route('/generate_resume', methods=['POST'])
# def generate_resume():
#     data = request.form.to_dict()
#     rendered = render_template('resume_template.html', **data)
#     pdf = HTML(string=rendered).write_pdf()
#     response = make_response(pdf)
#     response.headers['Content-Type'] = 'application/pdf'
#     response.headers['Content-Disposition'] = 'inline; filename=resume.pdf'
#     return response
@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    data = request.form.to_dict()
    section_titles = request.form.getlist('section_title[]')
    section_contents = request.form.getlist('section_content[]')

    dynamic_sections = []
    for title, content in zip(section_titles, section_contents):
        if title.strip() and content.strip():
            dynamic_sections.append({'title': title.strip(), 'content': content.strip()})

    data['dynamic_sections'] = dynamic_sections

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
# ---------------- Background Remover ----------------
# @app.route('/background_remover')
# def background_remover():
#     return render_template('background_remover.html')

# @app.route('/background_remover/remove', methods=['POST'])
# def remove_background():
#     try:
#         if 'image' not in request.files:
#             return jsonify({'error': 'No image uploaded'}), 400

#         file = request.files['image']
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'}), 400

#         input_image = Image.open(file.stream).convert("RGBA")
#         output_image = remove(input_image)

#         buf = io.BytesIO()
#         output_image.save(buf, format='PNG')
#         buf.seek(0)

#         return send_file(
#             buf,
#             mimetype='image/png',
#             as_attachment=True,
#             download_name='no_background.png'
#         )
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
    
    
# @app.route('/remove-bg', methods=['POST'])
# def remove_bg():
#     try:
#         file = request.files['image']
#         hex_color = request.form.get('bgcolor', '#FFFFFF')

#         input_data = file.read()
#         result_data = remove(input_data)

#         # Open output with alpha channel
#         img = Image.open(io.BytesIO(result_data)).convert("RGBA")
#         background = Image.new("RGBA", img.size, hex_color)
#         composited = Image.alpha_composite(background, img).convert("RGB")

#         output = io.BytesIO()
#         composited.save(output, format='PNG')
#         output.seek(0)

#         return send_file(output, mimetype='image/png')

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500   


if __name__ == '__main__':
    app.run(debug=True)
