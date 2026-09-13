from flask import Blueprint, render_template

text_bp = Blueprint('text', __name__, url_prefix='/text')

TEXT_TOOLS = {
    'tts-converter': {
        'id': 'tts-converter',
        'name': 'Text to Speech (MP3)',
        'desc': 'Convert text to natural speech and download as MP3/WAV. 100% client-side.',
        'icon': 'fa-volume-up',
        'seo_title': 'Free Online Text to Speech Converter - Download MP3',
        'seo_desc': 'Convert any text to high-quality natural speech instantly. Adjust pitch, speed, and emotion. Download the audio as MP3/WAV entirely in your browser.'
    },

    'word-counter': {
        'id': 'word-counter',
        'name': 'Word & Character Counter',
        'desc': 'Count words, characters, and estimate reading time instantly.',
        'icon': 'fa-font',
        'seo_title': 'Free Online Word and Character Counter',
        'seo_desc': 'Instantly count words, characters, sentences, and paragraphs in your text. Perfect for essays, SEO writing, and social media posts. 100% free.'
    },
    'case-converter': {
        'id': 'case-converter',
        'name': 'Case Converter',
        'desc': 'Change text to UPPERCASE, lowercase, Title Case, and more.',
        'icon': 'fa-text-height',
        'seo_title': 'Free Text Case Converter Online',
        'seo_desc': 'Easily convert your text to uppercase, lowercase, title case, or sentence case. Fast, free, and completely secure client-side processing.'
    },
    'lorem-ipsum': {
        'id': 'lorem-ipsum',
        'name': 'Lorem Ipsum Generator',
        'desc': 'Generate dummy text for web design and mockups.',
        'icon': 'fa-paragraph',
        'seo_title': 'Free Lorem Ipsum Dummy Text Generator',
        'seo_desc': 'Generate custom Lorem Ipsum placeholder text for your web design, layouts, and mockups. Fast, free, and highly customizable.'
    }
}


import urllib.request
import urllib.parse
from flask import request, Response
import time

@text_bp.route('/api/tts-download', methods=['POST'])
def tts_download():
    text = request.form.get('text', '').strip()
    if not text:
        return "No text provided", 400
        
    # Google TTS allows ~200 chars per request. We chunk it.
    chunks = [text[i:i+200] for i in range(0, len(text), 200)]
    
    mp3_data = b''
    for chunk in chunks:
        url = f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=en&q={urllib.parse.quote(chunk)}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            mp3_data += response.read()
        except Exception as e:
            print(f"TTS Download Error: {e}")
            
    if not mp3_data:
        return "Error generating audio", 500
        
    filename = f"text_to_speech_{int(time.time())}.mp3"
    headers = {
        "Content-Disposition": f"attachment;filename={filename}",
        "Content-Type": "audio/mpeg"
    }
    return Response(mp3_data, headers=headers)

@text_bp.route('/')
def text_hub():
    return render_template('hub_text.html', text_tools=TEXT_TOOLS)

@text_bp.route('/tool/<tool_id>')
def text_tool_page(tool_id):
    tool = TEXT_TOOLS.get(tool_id)
    if not tool:
        return "Text Tool not found", 404
    if tool_id == 'tts-converter':
        return render_template('tts_converter.html', tool=tool)
    return render_template('text_tool.html', tool=tool)
