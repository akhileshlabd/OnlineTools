import re

with open('routes/image.py', 'r') as f:
    content = f.read()

# Make sure we actually inject it into the dictionary
bg_remover_dict = "    'bg_remover': {'id': 'bg_remover', 'type': 'image', 'name': 'Remove Background', 'desc': 'Instantly remove or change image backgrounds locally using AI.', 'icon': 'fa-user-slash', 'endpoint': '/image-process/bg_remover', 'inputs': []},\n"

if "'id': 'bg_remover'" not in content:
    content = content.replace('IMAGE_TOOLS = {\n', 'IMAGE_TOOLS = {\n' + bg_remover_dict)

with open('routes/image.py', 'w') as f:
    f.write(content)
