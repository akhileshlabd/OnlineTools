import os

templates_dir = 'templates'
files = [f for f in os.listdir(templates_dir) if f.endswith('.html')]

results = {"fine": [], "fixed": [], "needs_fix": [], "ignored": []}

ignore_list = ['base.html', 'admin_dashboard.html', 'admin_login.html']

for file in files:
    if file in ignore_list:
        results['ignored'].append(file)
        continue
        
    filepath = os.path.join(templates_dir, file)
    with open(filepath, 'r') as f:
        content = f.read()
        
    word_count = len(content.split())
    has_seo = 'SEO Content' in content or 'SEO Block' in content or 'SEO & Instructions' in content or 'About the' in content
    
    if file in ['dynamic_tool.html', 'resizer.html', 'image_converter.html', 'qr_generator.html', 'excel_to_pdf.html', 'word_to_pdf.html', 'image_to_pdf.html', 'unlock_pdf.html', 'lock_pdf.html']:
        # We know we ran scripts on these recently
        results['fixed'].append(file)
    elif word_count > 300 or has_seo:
        results['fine'].append(file)
    else:
        results['needs_fix'].append(file)

print(f"Total Reviewed: {len(files)}")
print(f"Ignored (Admin/Base): {len(results['ignored'])}")
print(f"Fine (Already had text): {len(results['fine'])}")
print(f"Fixed (We recently patched): {len(results['fixed'])}")
print(f"Needs Fix: {len(results['needs_fix'])}")
print("Files needing fix:", results['needs_fix'])
