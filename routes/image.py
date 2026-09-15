from flask import Blueprint, render_template

image_bp = Blueprint('image', __name__)

@image_bp.route('/resizer')
def resizer():
    return render_template('resizer.html')

@image_bp.route('/converter')
def image_converter_page():
    return render_template('image_converter.html')

IMAGE_TOOLS = {
    'passport_maker': {'id': 'passport_maker', 'type': 'image', 'name': 'Passport Photo Maker', 'desc': 'Create standard 2x2 passport photos with auto-alignment and background removal.', 'icon': 'fa-id-badge', 'endpoint': '/image-process/passport_maker', 'inputs': []},
    'bg_remover': {'id': 'bg_remover', 'type': 'image', 'name': 'Remove Background', 'desc': 'Instantly remove or change image backgrounds locally using AI.', 'icon': 'fa-user-slash', 'endpoint': '/image-process/bg_remover', 'inputs': []},
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
    if tool_id == 'bg_remover':
        return render_template('bg_remover.html', tool=tool)
    if tool_id == 'passport_maker':
        return render_template('passport_maker.html', tool=tool)
    return render_template('dynamic_tool.html', tool=tool)

@image_bp.route('/qr-generator')
def qr_generator():
    return render_template('qr_generator.html')

@image_bp.route('/image')
def image_hub():
    return render_template('hub_image.html', image_tools=IMAGE_TOOLS)
