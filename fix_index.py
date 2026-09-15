import re

with open('templates/index.html', 'r') as f:
    content = f.read()

pattern = r'<div class="text-center mb-5">.*?</div>\n\s*</div>'
replacement = r'''<div class="text-center mb-5">
    <div class="d-inline-flex align-items-center justify-content-center bg-primary text-white rounded-pill px-3 py-1 mb-3 shadow-sm">
        <i class="fas fa-shield-alt me-2"></i> <span class="fw-bold text-uppercase" style="letter-spacing: 1px; font-size: 0.85rem;">Privacy First Platform</span>
    </div>
    <h1 class="fw-bolder text-dark mb-3 display-4" style="letter-spacing: -1px;">{{ t('hero_title') }}</h1>
    <p class="text-secondary fs-5 mx-auto" style="max-width: 800px; line-height: 1.6;">{{ t('hero_subtitle') }}</p>
</div>'''

# We know the content starts with `<div class="text-center mb-5">` and is followed by Main Categories Grid
# So let's just do a string replacement.
start_idx = content.find('<div class="text-center mb-5">')
end_idx = content.find('<!-- Main Categories Grid -->')

if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx] + replacement + "\n\n" + content[end_idx:]
    with open('templates/index.html', 'w') as f:
        f.write(new_content)
