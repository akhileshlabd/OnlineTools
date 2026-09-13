import re

with open('routes/text.py', 'r') as f:
    content = f.read()

backend_route = """
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
"""

if "/api/tts-download" not in content:
    # Insert it right before @text_bp.route('/')
    content = content.replace("@text_bp.route('/')", backend_route + "\n@text_bp.route('/')")
    # Make sure imports are clean
    if "from flask import request" not in content:
        content = content.replace("from flask import Blueprint, render_template", "from flask import Blueprint, render_template, request, Response")

with open('routes/text.py', 'w') as f:
    f.write(content)
