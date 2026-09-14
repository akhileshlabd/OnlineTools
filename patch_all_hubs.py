import re
import glob

# For generic loops like:
# {% for key, tool in math_tools.items() %}
#   <div class="col-md-6 col-lg-4 d-flex">...
# {% endfor %}

def patch_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Find the loop variable e.g. math_tools, network_tools
    match = re.search(r'{%\s*for\s+key,\s+tool\s+in\s+([a-zA-Z0-9_]+)\.items\(\)\s*%}', content)
    if not match:
        return
        
    loop_var = match.group(1) # e.g. finance_tools
    # Extract the prefix e.g. finance_tools -> finance
    prefix = loop_var.split('_')[0]
    # some custom mappings: 
    if prefix == 'network': prefix = 'net'
    if prefix == 'code': prefix = 'dev'
    if prefix == 'video': prefix = 'vid'
    if prefix == 'games': prefix = 'game'

    pattern = r'({%\s*for\s+key,\s+tool\s+in\s+' + loop_var + r'\.items\(\)\s*%}\s*)(<div.*?</div>)(\s*{%\s*endfor\s*%})'
    
    def replacer(m):
        pre = m.group(1)
        inner = m.group(2)
        post = m.group(3)
        if '{% if features' in inner: return m.group(0)
        return f"{pre}{{% if features['feature_{prefix}_' ~ tool.id] %}}\n{inner}\n{{% endif %}}{post}"

    new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)
    if new_content != content:
        with open(filename, 'w') as f:
            f.write(new_content)
        print(f"Patched {filename} dynamically.")
    else:
        # Maybe it doesn't have the exact div layout, let's just do manual string replace
        parts = content.split(f'{{% for key, tool in {loop_var}.items() %}}')
        if len(parts) > 1:
            for i in range(1, len(parts)):
                if '{% if features' not in parts[i]:
                    parts[i] = f"\n{{% if features['feature_{prefix}_' ~ tool.id] %}}" + parts[i].replace('{% endfor %}', '{% endif %}\n{% endfor %}', 1)
            final_content = f'{{% for key, tool in {loop_var}.items() %}}'.join(parts)
            with open(filename, 'w') as f:
                f.write(final_content)
            print(f"Patched {filename} using string replace.")

for file in glob.glob('templates/hub_*.html'):
    patch_file(file)
