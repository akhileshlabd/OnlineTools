import re

with open('templates/dynamic_tool.html', 'r') as f:
    content = f.read()

# Try to find the block
pattern = r'(<input class="d-none" type="file" id="fileInput" name="file" accept="\{% if tool\.type == \'image\' %\}image/\*\{% else %\}application/pdf\{% endif %\}" >\n\s*</div>)'

# Remove the messed up lines if they exist
content = re.sub(r'\s*<div class="alert alert-success border-0 shadow-sm mt-3 mb-4 text-center">\\?\n\s*<i class="fas fa-shield-alt text-success me-2"></i> <strong>100% Secure & Zero Uploads:</strong> Files are processed locally on your device.\n\s*</div>\n\s*</div>', '', content)
content = re.sub(r'\s*<i class="fas fa-shield-alt text-success me-2"></i> <strong>100% Secure & Zero Uploads:</strong> Files are processed locally on your device.\n\s*</div>\n\s*</div>', '', content)

replacement = r'''\1
        <div class="alert alert-success border-0 shadow-sm mt-3 mb-4 text-center">
            <i class="fas fa-shield-alt text-success me-2"></i> <strong>100% Secure & Zero Uploads:</strong> Files are processed locally on your device.
        </div>'''

new_content = re.sub(pattern, replacement, content)

with open('templates/dynamic_tool.html', 'w') as f:
    f.write(new_content)
