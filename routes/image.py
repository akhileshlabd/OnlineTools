from flask import Blueprint, render_template, request, jsonify, send_file
import io
from PIL import Image
from werkzeug.utils import secure_filename

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

        try:
            img = Image.open(file.stream)
        except Exception:
            return jsonify({'error': 'Invalid image file.'}), 400
            
        orig_width, orig_height = img.size

        if keep_ratio:
            aspect_ratio = orig_width / orig_height
            if width / height > aspect_ratio:
                width = int(height * aspect_ratio)
            else:
                height = int(width / aspect_ratio)

        resized_img = img.resize((width, height), Image.LANCZOS)

        buf = io.BytesIO()
        filename = secure_filename(file.filename)
        name = filename.rsplit('.', 1)[0] if '.' in filename else 'image'
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'png'

        if ext in ['jpg', 'jpeg']:
            save_format = 'JPEG'
            save_ext = 'jpg'
        elif ext == 'png':
            save_format = 'PNG'
            save_ext = 'png'
        elif ext == 'webp':
            save_format = 'WEBP'
            save_ext = 'webp'
        else:
            save_format = 'PNG'
            save_ext = 'png'

        # Ensure mode is correct for JPEG
        if save_format == 'JPEG' and resized_img.mode in ("RGBA", "P"):
            resized_img = resized_img.convert("RGB")

        resized_img.save(buf, format=save_format, optimize=True)
        buf.seek(0)

        return send_file(
            buf,
            mimetype=f'image/{save_ext}',
            as_attachment=True,
            download_name=f"resized_{name}.{save_ext}"
        )
    except Exception as e:
        return jsonify({'error': f'Failed to resize: {str(e)}'}), 500

@image_bp.route('/background_remover')
def background_remover():
    return render_template('background_remover.html')

@image_bp.route('/converter')
def image_converter_page():
    return render_template('image_converter.html')

@image_bp.route('/converter/convert', methods=['POST'])
def convert_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    target_format = request.form.get('format', 'JPEG').upper()
    try:
        quality = int(request.form.get('quality', 85))
    except ValueError:
        quality = 85

    # Validate target format
    if target_format not in ['JPEG', 'PNG', 'WEBP']:
        return jsonify({'error': 'Unsupported target format'}), 400

    try:
        img = Image.open(file.stream)
        
        # Handle RGBA/P formats being saved as JPEG
        if img.mode in ("RGBA", "P") and target_format == "JPEG":
            # Create a white background to paste the transparent image on
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "RGBA":
                background.paste(img, mask=img.split()[3]) # 3 is the alpha channel
            else:
                background.paste(img)
            img = background
        elif img.mode == "P":
            img = img.convert("RGBA")

        buf = io.BytesIO()
        filename = secure_filename(file.filename)
        name = filename.rsplit('.', 1)[0] if '.' in filename else 'image'
        
        save_ext = target_format.lower()
        if target_format == 'JPEG':
            save_ext = 'jpg'

        # Optimize and set quality
        save_kwargs = {'format': target_format, 'optimize': True}
        if target_format in ['JPEG', 'WEBP']:
            save_kwargs['quality'] = quality

        img.save(buf, **save_kwargs)
        buf.seek(0)

        return send_file(
            buf,
            mimetype=f'image/{save_ext}',
            as_attachment=True,
            download_name=f"{name}_converted.{save_ext}"
        )
    except Exception as e:
        return jsonify({'error': f"Failed to convert image: {str(e)}"}), 500
