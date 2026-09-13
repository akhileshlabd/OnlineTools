import sys

with open('templates/video_tool.html', 'r') as f:
    content = f.read()

seo_content = """
<!-- SEO Content for AdSense Compliance -->
<div class="container bg-white p-4 p-md-5 rounded shadow-sm mt-5 mb-4">
    {% if tool.id == 'mute' %}
        <h3 class="h4 fw-bold">How to Mute a Video Free Online</h3>
        <p>If you have recorded a video with distracting background noise, wind, or private conversations, our free video muter tool is the perfect solution. You can quickly remove the audio track from any MP4, MOV, or WEBM file. Simply upload your video, click process, and download the completely silent video file instantly. This is incredibly useful for preparing clips for social media, creating GIFs, or layering new background music over your footage.</p>
    {% elif tool.id == 'extract_audio' %}
        <h3 class="h4 fw-bold">How to Extract Audio to MP3 from a Video</h3>
        <p>Have you ever watched a video clip or recorded a concert and wished you could save just the music? Our free Video to MP3 converter allows you to strip the audio track from any video file and save it as a high-quality MP3 file. Whether it is a podcast recording, an interview, or a music video, you can securely rip the audio directly in your browser without losing sound quality.</p>
    {% elif tool.id == 'trim' %}
        <h3 class="h4 fw-bold">How to Trim and Cut Videos Online</h3>
        <p>Our free online video trimmer allows you to cut out specific sections of your video without having to download complex video editing software. By entering the start time and end time of the clip you want to save, you can easily remove unnecessary intros, outtakes, or dead space. Because this tool utilizes direct stream copying, the trimmed video is exported instantly without any loss in video quality.</p>
    {% elif tool.id == 'convert_mp4' %}
        <h3 class="h4 fw-bold">Convert MOV, AVI, and MKV to MP4 Free</h3>
        <p>Sharing videos across different devices can be frustrating if you are dealing with incompatible formats like Apple's MOV or heavy MKV files. Our free video converter instantly packages your video into the highly compatible MP4 format. MP4 is the universal standard for video sharing, ensuring your clips will play perfectly on iPhones, Androids, Windows PCs, Macs, and all major web browsers.</p>
    {% elif tool.id == 'thumbnail' %}
        <h3 class="h4 fw-bold">How to Extract a JPG Thumbnail from a Video</h3>
        <p>Creating YouTube thumbnails or pulling a high-quality snapshot from a video recording is easy with our thumbnail extractor. Instead of pausing your video and taking a low-resolution screenshot, simply enter the exact timestamp (in seconds) of the frame you want to capture. Our tool instantly scans the video and exports that precise frame as a full-resolution JPG image file.</p>
    {% endif %}
    
    <h4 class="h5 fw-bold mt-4">100% Secure & Private Processing</h4>
    <p>Most online video editors force you to upload your massive video files to their cloud servers, putting your privacy at risk and forcing you to wait in slow upload queues. <strong>Free Qube is different.</strong> We utilize cutting-edge WebAssembly (FFmpeg.wasm) technology to process your videos entirely on your own device. Your files never leave your computer or phone. This guarantees absolute privacy, lightning-fast processing, and complete protection of your personal media.</p>
</div>
"""

# Insert the SEO content right before the FFmpeg script tag
insert_target = "<!-- FFmpeg.wasm v0.11.6 (Stable Single-Threaded Version) -->"
if insert_target in content:
    content = content.replace(insert_target, seo_content + "\n" + insert_target)
else:
    # Fallback to appending before block scripts
    content = content.replace('{% block scripts %}', seo_content + '\n{% block scripts %}')

with open('templates/video_tool.html', 'w') as f:
    f.write(content)
