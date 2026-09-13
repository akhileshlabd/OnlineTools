import re

with open('routes/text.py', 'r') as f:
    content = f.read()

new_tool = """    'tts-converter': {
        'id': 'tts-converter',
        'name': 'Text to Speech (MP3)',
        'desc': 'Convert text to natural speech and download as MP3/WAV. 100% client-side.',
        'icon': 'fa-volume-up',
        'seo_title': 'Free Online Text to Speech Converter - Download MP3',
        'seo_desc': 'Convert any text to high-quality natural speech instantly. Adjust pitch, speed, and emotion. Download the audio as MP3/WAV entirely in your browser.'
    },
"""

if "'tts-converter'" not in content:
    content = content.replace("TEXT_TOOLS = {", "TEXT_TOOLS = {\n" + new_tool)

old_routing = """@text_bp.route('/tool/<tool_id>')
def text_tool_page(tool_id):
    tool = TEXT_TOOLS.get(tool_id)
    if not tool:
        return "Text Tool not found", 404
    return render_template('text_tool.html', tool=tool)"""

new_routing = """@text_bp.route('/tool/<tool_id>')
def text_tool_page(tool_id):
    tool = TEXT_TOOLS.get(tool_id)
    if not tool:
        return "Text Tool not found", 404
    if tool_id == 'tts-converter':
        return render_template('tts_converter.html', tool=tool)
    return render_template('text_tool.html', tool=tool)"""

if "if tool_id == 'tts-converter':" not in content:
    content = content.replace(old_routing, new_routing)

with open('routes/text.py', 'w') as f:
    f.write(content)
