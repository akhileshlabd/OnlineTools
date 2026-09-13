import sys

with open('templates/video_tool.html', 'r') as f:
    content = f.read()

old_trim = """        } else if (toolId === 'trim') {
            outputName = 'trimmed_' + Date.now() + '.mp4';
            const start = document.getElementById('trimStart').value || '00:00:00';
            const end = document.getElementById('trimEnd').value || '00:00:10';
            // -ss and -to before -i is faster for ffmpeg
            cmd = ['-ss', start, '-to', end, '-i', safeInputName, '-c', 'copy', outputName];
            mimeType = 'video/mp4';"""

new_trim = """        } else if (toolId === 'trim') {
            outputName = 'trimmed_' + Date.now() + '.mp4';
            const start = (document.getElementById('trimStart').value || '00:00:00').trim();
            const end = (document.getElementById('trimEnd').value || '00:00:10').trim();
            // Placing -ss and -to AFTER -i is much more reliable for stream copying and prevents exit(1) crashes
            cmd = ['-i', safeInputName, '-ss', start, '-to', end, '-c', 'copy', outputName];
            mimeType = 'video/mp4';"""

content = content.replace(old_trim, new_trim)

old_thumb = """        } else if (toolId === 'thumbnail') {
            outputName = 'thumbnail_' + Date.now() + '.jpg';
            const t = document.getElementById('thumbTime').value || '1';
            cmd = ['-ss', t, '-i', safeInputName, '-vframes', '1', '-q:v', '2', outputName];
            mimeType = 'image/jpeg';"""

new_thumb = """        } else if (toolId === 'thumbnail') {
            outputName = 'thumbnail_' + Date.now() + '.jpg';
            const t = String(document.getElementById('thumbTime').value || '1').trim();
            cmd = ['-ss', t, '-i', safeInputName, '-vframes', '1', '-q:v', '2', outputName];
            mimeType = 'image/jpeg';"""

content = content.replace(old_thumb, new_thumb)

with open('templates/video_tool.html', 'w') as f:
    f.write(content)
