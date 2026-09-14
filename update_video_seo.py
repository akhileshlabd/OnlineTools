import re

filepath = 'templates/video_tool.html'
with open(filepath, 'r') as f:
    content = f.read()

content = re.sub(r'{% block title %}.*?{% endblock %}\n*', '', content, flags=re.DOTALL)
content = re.sub(r'{% block meta_desc %}.*?{% endblock %}\n*', '', content, flags=re.DOTALL)
content = re.sub(r'{% block meta_keywords %}.*?{% endblock %}\n*', '', content, flags=re.DOTALL)
content = re.sub(r'<!-- SEO Content for AdSense Compliance -->.*?(?=<script)', '', content, flags=re.DOTALL)

blocks = """{% block title %}
{% if tool.id == 'mute' %}Mute Video Free Online | Remove Audio from MP4 - Free Qube
{% elif tool.id == 'extract_audio' %}Video to MP3 Converter Free | Extract Audio - Free Qube
{% else %}{{ tool.name }} - Free Qube{% endif %}
{% endblock %}

{% block meta_desc %}
{% if tool.id == 'mute' %}Remove audio from video files for free. Mute MP4, MOV, and WEBM securely with our 100% local client-side muter tool. No watermarks.
{% elif tool.id == 'extract_audio' %}Extract high-quality audio from any video. Convert MP4 to MP3 securely in your browser without uploading to any server. Completely free.
{% else %}{{ tool.desc }}{% endif %}
{% endblock %}

{% block meta_keywords %}
{% if tool.id == 'mute' %}mute video, remove audio from video, mute mp4, remove sound from video free, mute video online, remove audio track
{% elif tool.id == 'extract_audio' %}video to mp3, extract audio from video, mp4 to mp3, free video to mp3 converter, rip audio from video
{% endif %}
{% endblock %}
"""

seo_html = """<!-- SEO Content for AdSense Compliance -->
<div class="container bg-white p-4 p-md-5 rounded shadow-sm mt-5 mb-4">
    {% if tool.id == 'mute' %}
        <h2 class="fw-bold mb-3">Mute Video Free Online: Remove Audio Instantly</h2>
        <p>If you have recorded a video with distracting background noise, heavy wind, or private background conversations, our <strong>Free Video Muter</strong> tool is the perfect solution. You can quickly strip the audio track from any MP4, MOV, or WEBM file to create a completely silent video. This is incredibly useful for preparing b-roll clips for social media, creating clean GIFs, or layering new background music over your footage.</p>
        <h3 class="fw-bold mt-4">100% Secure & Private Video Processing</h3>
        <p>Most online video editors force you to upload your massive, private video files to their cloud servers, putting your privacy at risk and forcing you to wait in slow upload queues. <strong>Free Qube is different.</strong> We utilize cutting-edge WebAssembly (FFmpeg.wasm) technology to mute your videos entirely on your own device. Your files never leave your computer or phone. This guarantees absolute privacy, lightning-fast processing, and complete protection of your personal media.</p>
    {% elif tool.id == 'extract_audio' %}
        <h2 class="fw-bold mb-3">Video to MP3 Converter: Extract Audio Free</h2>
        <p>Have you ever watched a video clip, a recorded lecture, or a concert and wished you could save just the music? Our free <strong>Video to MP3 converter</strong> allows you to effortlessly strip the audio track from any video file and save it as a high-quality MP3. Whether it is a podcast recording, an interview, or a music video, you can securely rip the audio directly in your browser without losing sound quality.</p>
        <h3 class="fw-bold mt-4">The Safest Way to Convert MP4 to MP3</h3>
        <p>Why risk uploading your personal home videos or proprietary corporate recordings to a random server? By leveraging WebAssembly and FFmpeg, our tool parses your video and extracts the MP3 locally using your own computer's RAM. No data is ever transmitted, there are no file size upload limits, and you will never see a watermark.</p>
    {% endif %}
</div>
"""

content = re.sub(r'({% extends "base.html" %}\n)', r'\1\n' + blocks + '\n', content)
content = re.sub(r'(<script src="https://cdn.jsdelivr.net/npm/@ffmpeg/ffmpeg@0.11.6/dist/ffmpeg.min.js">)', seo_html + r'\n\1', content)

with open(filepath, 'w') as f:
    f.write(content)
print(f"Updated {filepath} successfully.")
