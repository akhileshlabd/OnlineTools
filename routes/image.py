from flask import Blueprint, render_template, request, jsonify, send_file
import io
from PIL import Image

image_bp = Blueprint('image', __name__)

@image_bp.route('/resizer')
def resizer():
    return render_template('resizer.html')

@image_bp.route('/resizer/resize', methods=['POST'])
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

@image_bp.route('/background_remover')
def background_remover():
    return render_template('background_remover.html')
   
@image_bp.route('/remove-bg', methods=['POST'])
def remove_bg():
    from rembg import remove
    try:
        file = request.files['image']
        hex_color = request.form.get('bgcolor', '#FFFFFF')

        input_data = file.read()
        result_data = remove(input_data)

        # Open output with alpha channel
        img = Image.open(io.BytesIO(result_data)).convert("RGBA")
        background = Image.new("RGBA", img.size, hex_color)
        composited = Image.alpha_composite(background, img).convert("RGB")

        output = io.BytesIO()
        composited.save(output, format='PNG')
        output.seek(0)

        return send_file(output, mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

