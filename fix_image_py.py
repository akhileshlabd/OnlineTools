import re

with open('routes/image.py', 'r') as f:
    content = f.read()

bg_remover_dict = """    'bg_remover': {'id': 'bg_remover', 'type': 'image', 'name': 'Remove Background', 'desc': 'Instantly remove or change image backgrounds locally using AI.', 'icon': 'fa-user-slash', 'url': 'image.bg_remover_page'},
"""

if "'bg_remover'" not in content:
    content = content.replace('IMAGE_TOOLS = {', 'IMAGE_TOOLS = {\n' + bg_remover_dict)

# Fix the route definition
old_route = """@image_bp.route('/background-remover')
def bg_remover_page():
    tool = next((t for t in IMAGE_TOOLS if t['id'] == 'bg_remover'), None)
    return render_template('bg_remover.html', tool=tool)"""

new_route = """@image_bp.route('/background-remover')
def bg_remover_page():
    tool = IMAGE_TOOLS.get('bg_remover')
    return render_template('bg_remover.html', tool=tool)"""

if "def bg_remover_page" in content:
    content = content.replace(old_route, new_route)
else:
    content += "\n" + new_route + "\n"

with open('routes/image.py', 'w') as f:
    f.write(content)
