import re

with open('templates/akinator.html', 'r') as f:
    content = f.read()

# Replace the giant script block with the modular import
old_script_start = "<script type=\"module\">"
old_script_end = "</script>"

script_content = content[content.find(old_script_start):content.find(old_script_end) + len(old_script_end)]

new_script = """<script type="module">
    import { AkinatorEngine } from "{{ url_for('static', filename='js/akinatorEngine.js') }}";
    import { AkinatorUI } from "{{ url_for('static', filename='js/akinatorUI.js') }}";

    const engine = new AkinatorEngine();
    const ui = new AkinatorUI(engine);
    
    // Start game and pass the JSON URL from the server
    ui.initGame("{{ url_for('static', filename='data/characters.json') }}");
</script>"""

content = content.replace(script_content, new_script)

with open('templates/akinator.html', 'w') as f:
    f.write(content)
