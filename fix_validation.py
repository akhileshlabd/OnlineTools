import os
import re

TEMPLATES_DIR = '/Users/darsana/Online-Tools/OnlineTools/templates'

for filename in os.listdir(TEMPLATES_DIR):
    if not filename.endswith('.html'): continue
    filepath = os.path.join(TEMPLATES_DIR, filename)
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Remove 'required' from hidden file inputs to prevent "invalid form control is not focusable"
    content = re.sub(r'(<input[^>]+class="[^"]*d-none[^"]*"[^>]+type="file"[^>]+)required(>)', r'\1\2', content)
    
    with open(filepath, 'w') as f:
        f.write(content)

print("Validation fixed!")
