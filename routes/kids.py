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
    },
    'animal-sounds': {
        'id': 'animal-sounds',
        'name': 'Interactive Animal Sounds',
        'desc': 'Learn animal names and sounds with these interactive flashcards. Click on any animal to hear it!',
        'icon': 'fa-paw',
        'seo_title': 'Interactive Animal Sounds & Flashcards for Kids',
        'seo_desc': 'Free educational animal sounds flashcard game for toddlers and kids. 100% safe, no downloads required.'
    },
    'color-mixer': {
        'id': 'color-mixer',
        'name': 'Magic Color Mixer',
        'desc': 'Discover how primary colors combine to make new colors! A fun, interactive color learning tool.',
        'icon': 'fa-palette',
        'seo_title': 'Interactive Color Mixing Game for Kids',
        'seo_desc': 'Educational color mixing game for toddlers. Learn primary and secondary colors in a safe, interactive environment.'
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
