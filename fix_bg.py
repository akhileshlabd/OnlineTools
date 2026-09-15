import re

with open('templates/bg_remover.html', 'r') as f:
    content = f.read()

pattern = r'(<input class="d-none" type="file" id="imageInput" name="file" accept="image/\*" >\n\s*</div>)'

replacement = r'''\1
        <div class="alert alert-success border-0 shadow-sm mt-3 mb-4 text-center">
            <i class="fas fa-shield-alt text-success me-2"></i> <strong>100% Secure & Zero Uploads:</strong> AI runs locally on your device.
        </div>'''

new_content = re.sub(pattern, replacement, content)

with open('templates/bg_remover.html', 'w') as f:
    f.write(new_content)
