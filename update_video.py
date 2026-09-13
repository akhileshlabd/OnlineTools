import sys

with open('templates/video_tool.html', 'r') as f:
    content = f.read()

# Insert the HTML options
html_to_insert = """
            {% if tool.id == 'trim' %}
            <div class="row g-3 justify-content-center mb-4 text-start">
                <div class="col-md-5">
                    <label class="form-label fw-bold">Start Time</label>
                    <input type="text" class="form-control" id="trimStart" placeholder="00:00:00" value="00:00:00">
                </div>
                <div class="col-md-5">
                    <label class="form-label fw-bold">End Time</label>
                    <input type="text" class="form-control" id="trimEnd" placeholder="00:00:10" value="00:00:10">
                </div>
            </div>
            {% endif %}
            {% if tool.id == 'thumbnail' %}
            <div class="row g-3 justify-content-center mb-4 text-start">
                <div class="col-md-6">
                    <label class="form-label fw-bold">Snapshot Time (Seconds)</label>
                    <input type="number" class="form-control" id="thumbTime" placeholder="e.g. 5" value="1" min="0" step="0.1">
                </div>
            </div>
            {% endif %}
"""

# Find the button insertion point
content = content.replace('<button class="btn btn-primary btn-lg rounded-pill px-5 fw-bold shadow-sm mt-3" id="startBtn">', html_to_insert + '\n            <button class="btn btn-primary btn-lg rounded-pill px-5 fw-bold shadow-sm mt-3" id="startBtn">')

# Replace the command logic in JS
old_logic = """
        if (toolId === 'mute') {
            outputName = 'muted_' + Date.now() + '.mp4';
            cmd = ['-i', safeInputName, '-c', 'copy', '-an', outputName];
            mimeType = 'video/mp4';
        } else if (toolId === 'extract_audio') {
            outputName = 'audio_' + Date.now() + '.mp3';
            cmd = ['-i', safeInputName, '-q:a', '0', '-map', 'a', outputName];
            mimeType = 'audio/mp3';
        }
"""

new_logic = """
        if (toolId === 'mute') {
            outputName = 'muted_' + Date.now() + '.mp4';
            cmd = ['-i', safeInputName, '-c', 'copy', '-an', outputName];
            mimeType = 'video/mp4';
        } else if (toolId === 'extract_audio') {
            outputName = 'audio_' + Date.now() + '.mp3';
            cmd = ['-i', safeInputName, '-q:a', '0', '-map', 'a', outputName];
            mimeType = 'audio/mp3';
        } else if (toolId === 'trim') {
            outputName = 'trimmed_' + Date.now() + '.mp4';
            const start = document.getElementById('trimStart').value || '00:00:00';
            const end = document.getElementById('trimEnd').value || '00:00:10';
            // -ss and -to before -i is faster for ffmpeg
            cmd = ['-ss', start, '-to', end, '-i', safeInputName, '-c', 'copy', outputName];
            mimeType = 'video/mp4';
        } else if (toolId === 'convert_mp4') {
            outputName = 'converted_' + Date.now() + '.mp4';
            // Copy video, encode audio to aac for compatibility
            cmd = ['-i', safeInputName, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', outputName];
            mimeType = 'video/mp4';
        } else if (toolId === 'thumbnail') {
            outputName = 'thumbnail_' + Date.now() + '.jpg';
            const t = document.getElementById('thumbTime').value || '1';
            cmd = ['-ss', t, '-i', safeInputName, '-vframes', '1', '-q:v', '2', outputName];
            mimeType = 'image/jpeg';
        }
"""
content = content.replace(old_logic, new_logic)

# Replace the download button logic
old_download = "downloadBtn.download = (toolId === 'mute' ? 'muted_' : 'audio_') + selectedFile.name.replace(/\.[^/.]+$/, \"\") + (toolId === 'mute' ? '.mp4' : '.mp3');"
new_download = """
        const prefix = toolId === 'mute' ? 'muted_' : toolId === 'extract_audio' ? 'audio_' : toolId === 'trim' ? 'trimmed_' : toolId === 'convert_mp4' ? 'converted_' : 'thumb_';
        let ext = '.mp4';
        if (toolId === 'extract_audio') ext = '.mp3';
        if (toolId === 'thumbnail') ext = '.jpg';
        downloadBtn.download = prefix + selectedFile.name.replace(/\.[^/.]+$/, "") + ext;
"""
content = content.replace(old_download, new_download)

# Allow more formats in file input
content = content.replace('accept="video/mp4,video/webm,video/quicktime"', 'accept="video/*"')
content = content.replace('or drag and drop here (MP4, WEBM, MOV)', 'or drag and drop here (MP4, MOV, AVI, MKV)')


with open('templates/video_tool.html', 'w') as f:
    f.write(content)

