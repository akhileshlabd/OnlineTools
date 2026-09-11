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

IMAGE_TOOLS = {
    'grayscale': {'id': 'grayscale', 'type': 'image', 'name': 'Grayscale Image', 'desc': 'Convert your image to black and white.', 'icon': 'fa-adjust', 'endpoint': '/image-process/grayscale', 'inputs': []},
    'blur': {'id': 'blur', 'type': 'image', 'name': 'Blur Image', 'desc': 'Apply a gaussian blur to your image.', 'icon': 'fa-tint', 'endpoint': '/image-process/blur', 'inputs': [{'name': 'radius', 'type': 'number', 'label': 'Blur Radius', 'min': 1, 'max': 50}]},
    'flip_h': {'id': 'flip_h', 'type': 'image', 'name': 'Flip Horizontal', 'desc': 'Mirror your image horizontally.', 'icon': 'fa-arrows-alt-h', 'endpoint': '/image-process/flip_h', 'inputs': []},
    'flip_v': {'id': 'flip_v', 'type': 'image', 'name': 'Flip Vertical', 'desc': 'Mirror your image vertically.', 'icon': 'fa-arrows-alt-v', 'endpoint': '/image-process/flip_v', 'inputs': []},
    'rotate_tool': {'id': 'rotate_tool', 'type': 'image', 'name': 'Rotate Image', 'desc': 'Rotate your image by any degree.', 'icon': 'fa-sync', 'endpoint': '/image-process/rotate_tool', 'inputs': [{'name': 'angle', 'type': 'number', 'label': 'Angle (Degrees)', 'min': -360, 'max': 360}]},
    'brightness': {'id': 'brightness', 'type': 'image', 'name': 'Adjust Brightness', 'desc': 'Change the brightness of your image.', 'icon': 'fa-sun', 'endpoint': '/image-process/brightness', 'inputs': [{'name': 'factor', 'type': 'number', 'label': 'Brightness Factor (1.0 = normal)', 'min': 0, 'max': 5}]},
    'contrast': {'id': 'contrast', 'type': 'image', 'name': 'Adjust Contrast', 'desc': 'Change the contrast of your image.', 'icon': 'fa-adjust', 'endpoint': '/image-process/contrast', 'inputs': [{'name': 'factor', 'type': 'number', 'label': 'Contrast Factor (1.0 = normal)', 'min': 0, 'max': 5}]}
}

@image_bp.route('/image-tool/<tool_id>')
def dynamic_image_tool(tool_id):
    tool = IMAGE_TOOLS.get(tool_id)
    if not tool: return "Tool not found", 404
    return render_template('dynamic_tool.html', tool=tool)

@image_bp.route('/image-process/<tool_id>', methods=['POST'])
def process_dynamic_image(tool_id):
    from PIL import ImageFilter, ImageEnhance
    if 'file' not in request.files: return jsonify({'error': 'No image uploaded'}), 400
    file = request.files['file']
    if file.filename == '': return jsonify({'error': 'No selected file'}), 400

    try:
        img = Image.open(file.stream)
        
        if tool_id == 'grayscale':
            img = img.convert('L')
        elif tool_id == 'blur':
            radius = float(request.form.get('radius', 2))
            img = img.filter(ImageFilter.GaussianBlur(radius))
        elif tool_id == 'flip_h':
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        elif tool_id == 'flip_v':
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
        elif tool_id == 'rotate_tool':
            angle = float(request.form.get('angle', 90))
            img = img.rotate(-angle, expand=True) # Negative so positive = clockwise
        elif tool_id == 'brightness':
            factor = float(request.form.get('factor', 1.0))
            img = ImageEnhance.Brightness(img).enhance(factor)
        elif tool_id == 'contrast':
            factor = float(request.form.get('factor', 1.0))
            img = ImageEnhance.Contrast(img).enhance(factor)
            
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        
        return send_file(buf, mimetype='image/png', as_attachment=True, download_name=f"processed_{tool_id}.png")
    except Exception as e:
        return jsonify({'error': str(e)}), 500
