import re

with open('routes/image.py', 'r') as f:
    content = f.read()

old_dynamic = """def dynamic_image_tool(tool_id):
    tool = IMAGE_TOOLS.get(tool_id)
    if not tool: return "Tool not found", 404
    return render_template('dynamic_tool.html', tool=tool)"""

new_dynamic = """def dynamic_image_tool(tool_id):
    tool = IMAGE_TOOLS.get(tool_id)
    if not tool: return "Tool not found", 404
    if tool_id == 'bg_remover':
        return render_template('bg_remover.html', tool=tool)
    return render_template('dynamic_tool.html', tool=tool)"""

content = content.replace(old_dynamic, new_dynamic)

# Remove the redundant bg_remover_page route
content = re.sub(r'@image_bp\.route\(\'/background-remover\'\)\ndef bg_remover_page\(\):.*?return render_template\(\'bg_remover\.html\', tool=tool\)', '', content, flags=re.DOTALL)

with open('routes/image.py', 'w') as f:
    f.write(content)

