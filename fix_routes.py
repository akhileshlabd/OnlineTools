import os

BASE_DIR = '/Users/darsana/Online-Tools/OnlineTools'
ROUTES_DIR = os.path.join(BASE_DIR, 'routes')

# Fix PDF Routes
pdf_path = os.path.join(ROUTES_DIR, 'pdf.py')
with open(pdf_path, 'r') as f:
    content = f.read()
content = content.replace("'/pdf-route/process/", "'/pdf-process/")
content = content.replace("@pdf_bp.route('/tool/<tool_id>')", "@pdf_bp.route('/pdf-tool/<tool_id>')")
content = content.replace("@pdf_bp.route('/process/<tool_id>'", "@pdf_bp.route('/pdf-process/<tool_id>'")
with open(pdf_path, 'w') as f:
    f.write(content)

# Fix Image Routes
img_path = os.path.join(ROUTES_DIR, 'image.py')
with open(img_path, 'r') as f:
    content = f.read()
content = content.replace("'/image/process/", "'/image-process/")
content = content.replace("@image_bp.route('/tool/<tool_id>')", "@image_bp.route('/image-tool/<tool_id>')")
content = content.replace("@image_bp.route('/process/<tool_id>'", "@image_bp.route('/image-process/<tool_id>'")
with open(img_path, 'w') as f:
    f.write(content)

# Fix Career Routes
res_path = os.path.join(ROUTES_DIR, 'resume.py')
with open(res_path, 'r') as f:
    content = f.read()
content = content.replace("'/resume/process/", "'/career-process/")
content = content.replace("@resume_bp.route('/tool/<tool_id>')", "@resume_bp.route('/career-tool/<tool_id>')")
content = content.replace("@resume_bp.route('/process/<tool_id>'", "@resume_bp.route('/career-process/<tool_id>'")
with open(res_path, 'w') as f:
    f.write(content)

print("Routes fixed")
