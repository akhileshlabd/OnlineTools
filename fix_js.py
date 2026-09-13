import re

with open('templates/video_tool.html', 'r') as f:
    content = f.read()

# Fix the broken JS block
bad_block_start = "if (toolId === 'mute') {"
bad_block_end = "processStatus.textContent = 'Executing FFmpeg command...';"

new_block = """if (toolId === 'mute') {
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
        }

        processStatus.textContent = 'Executing FFmpeg command...';"""

content = re.sub(r'if \(toolId === \'mute\'\) \{.*?processStatus\.textContent = \'Executing FFmpeg command\.\.\.\';', new_block, content, flags=re.DOTALL)

with open('templates/video_tool.html', 'w') as f:
    f.write(content)

