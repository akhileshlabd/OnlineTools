import re

with open('templates/video_tool.html', 'r') as f:
    content = f.read()

# Remove thumbnail UI
content = re.sub(r'\{\%\s*if\s*tool\.id\s*==\s*\'thumbnail\'\s*\%\}.*?\{\%\s*endif\s*\%\}', '', content, flags=re.DOTALL)

# Remove JS logic
content = re.sub(r'\s*\}\s*else\s*if\s*\(toolId\s*===\s*\'extract_audio\'\)\s*\{[^\}]+\}', '', content)
content = re.sub(r'\s*\}\s*else\s*if\s*\(toolId\s*===\s*\'thumbnail\'\)\s*\{[^\}]+\}', '', content)

# Remove SEO logic
content = re.sub(r'\{\%\s*elif\s*tool\.id\s*==\s*\'extract_audio\'\s*\%\}.*?(?=\{\%\s*elif)', '', content, flags=re.DOTALL)
content = re.sub(r'\{\%\s*elif\s*tool\.id\s*==\s*\'thumbnail\'\s*\%\}.*?(?=\{\%\s*endif)', '', content, flags=re.DOTALL)

# Fix download logic
old_dl = """const prefix = toolId === 'mute' ? 'muted_' : toolId === 'extract_audio' ? 'audio_' : toolId === 'trim' ? 'trimmed_' : toolId === 'convert_mp4' ? 'converted_' : 'thumb_';
        let ext = '.mp4';
        if (toolId === 'extract_audio') ext = '.mp3';
        if (toolId === 'thumbnail') ext = '.jpg';"""
new_dl = """const prefix = toolId === 'mute' ? 'muted_' : toolId === 'trim' ? 'trimmed_' : toolId === 'convert_mp4' ? 'converted_' : 'processed_';
        let ext = '.mp4';"""
content = content.replace(old_dl, new_dl)

with open('templates/video_tool.html', 'w') as f:
    f.write(content)
