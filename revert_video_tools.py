import re

with open('templates/video_tool.html', 'r') as f:
    content = f.read()

# 1. Remove Trim UI
content = re.sub(r'\{\%\s*if\s*tool\.id\s*==\s*\'trim\'\s*\%\}.*?\{\%\s*endif\s*\%\}', '', content, flags=re.DOTALL)

# 2. Fix JS Block
old_js_block = """if (toolId === 'mute') {
            outputName = 'muted_' + Date.now() + '.mp4';
            cmd = ['-i', safeInputName, '-c', 'copy', '-an', outputName];
            mimeType = 'video/mp4';
        } else if (toolId === 'trim') {
            outputName = 'trimmed_' + Date.now() + '.mp4';
            const start = (document.getElementById('trimStart').value || '00:00:00').trim();
            const end = (document.getElementById('trimEnd').value || '00:00:10').trim();
            cmd = ['-i', safeInputName, '-ss', start, '-to', end, '-c', 'copy', outputName];
            mimeType = 'video/mp4';
        } else if (toolId === 'convert_mp4') {
            outputName = 'converted_' + Date.now() + '.mp4';
            cmd = ['-i', safeInputName, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', outputName];
            mimeType = 'video/mp4';
        }"""

new_js_block = """if (toolId === 'mute') {
            outputName = 'muted_' + Date.now() + '.mp4';
            cmd = ['-i', safeInputName, '-c', 'copy', '-an', outputName];
            mimeType = 'video/mp4';
        } else if (toolId === 'extract_audio') {
            outputName = 'audio_' + Date.now() + '.mp3';
            cmd = ['-i', safeInputName, '-q:a', '0', '-map', 'a', outputName];
            mimeType = 'audio/mp3';
        }"""
content = content.replace(old_js_block, new_js_block)

# 3. Fix SEO block
old_seo_block = """{% elif tool.id == 'trim' %}
        <h3 class="h4 fw-bold">How to Trim and Cut Videos Online</h3>
        <p>Our free online video trimmer allows you to cut out specific sections of your video without having to download complex video editing software. By entering the start time and end time of the clip you want to save, you can easily remove unnecessary intros, outtakes, or dead space. Because this tool utilizes direct stream copying, the trimmed video is exported instantly without any loss in video quality.</p>
    {% elif tool.id == 'convert_mp4' %}
        <h3 class="h4 fw-bold">Convert MOV, AVI, and MKV to MP4 Free</h3>
        <p>Sharing videos across different devices can be frustrating if you are dealing with incompatible formats like Apple's MOV or heavy MKV files. Our free video converter instantly packages your video into the highly compatible MP4 format. MP4 is the universal standard for video sharing, ensuring your clips will play perfectly on iPhones, Androids, Windows PCs, Macs, and all major web browsers.</p>
    {% endif %}"""

new_seo_block = """{% elif tool.id == 'extract_audio' %}
        <h3 class="h4 fw-bold">How to Extract Audio to MP3 from a Video</h3>
        <p>Have you ever watched a video clip or recorded a concert and wished you could save just the music? Our free Video to MP3 converter allows you to strip the audio track from any video file and save it as a high-quality MP3 file. Whether it is a podcast recording, an interview, or a music video, you can securely rip the audio directly in your browser without losing sound quality.</p>
    {% endif %}"""
content = content.replace(old_seo_block, new_seo_block)

# 4. Fix download button logic
old_dl_logic = """const prefix = toolId === 'mute' ? 'muted_' : toolId === 'trim' ? 'trimmed_' : toolId === 'convert_mp4' ? 'converted_' : 'processed_';
        let ext = '.mp4';
        downloadBtn.download = prefix + selectedFile.name.replace(/\.[^/.]+$/, "") + ext;"""

new_dl_logic = """const prefix = toolId === 'mute' ? 'muted_' : toolId === 'extract_audio' ? 'audio_' : 'processed_';
        let ext = toolId === 'mute' ? '.mp4' : '.mp3';
        downloadBtn.download = prefix + selectedFile.name.replace(/\.[^/.]+$/, "") + ext;"""
content = content.replace(old_dl_logic, new_dl_logic)

with open('templates/video_tool.html', 'w') as f:
    f.write(content)
