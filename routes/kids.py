from flask import Blueprint, render_template

kids_bp = Blueprint('kids', __name__, url_prefix='/kids')

KIDS_TOOLS = {
    'smash-toy': {
        'id': 'smash-toy',
        'name': 'Baby Smash Toy',
        'desc': 'Opens directly in fullscreen! Smashes keyboard to learn letters and numbers with playful sounds and glitters.',
        'icon': 'fa-baby',
        'seo_title': 'Baby Smash Toy - Fullscreen Keyboard Game for Toddlers',
        'seo_desc': 'An instant fullscreen smash toy for babies and toddlers. Safe, colorful, and fun. Works with touch, keyboard, and mouse.'
    }
}

@kids_bp.route('/tool/<tool_id>')
def kids_tool_page(tool_id):
    tool = KIDS_TOOLS.get(tool_id)
    if not tool:
        return "Tool not found", 404
    return render_template('kids_tool.html', tool=tool)

@kids_bp.route('/')
def kids_hub():
    return render_template('hub_kids.html', kids_tools=KIDS_TOOLS)
