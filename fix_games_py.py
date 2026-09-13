import re

with open('routes/games.py', 'r') as f:
    content = f.read()

new_game = """    'akinator-game': {
        'id': 'akinator-game',
        'name': 'Mind Reader (Akinator)',
        'desc': 'Think of a character and our client-side AI will guess who it is by asking 20 questions!',
        'icon': 'fa-brain',
        'seo_title': 'Play Mind Reader Guessing Game Online for Free',
        'seo_desc': 'Play our 100% client-side Mind Reader game. Think of any character and our zero-server AI will guess it instantly.'
    },
"""

if "'akinator-game'" not in content:
    content = content.replace("GAMES_TOOLS = {", "GAMES_TOOLS = {\n" + new_game)

# Update routing to serve custom template
old_routing = """@games_bp.route('/tool/<tool_id>')
def games_tool_page(tool_id):
    tool = GAMES_TOOLS.get(tool_id)
    if not tool:
        return "Game not found", 404
    return render_template('games_tool.html', tool=tool)"""

new_routing = """@games_bp.route('/tool/<tool_id>')
def games_tool_page(tool_id):
    tool = GAMES_TOOLS.get(tool_id)
    if not tool:
        return "Game not found", 404
    if tool_id == 'akinator-game':
        return render_template('akinator.html', tool=tool)
    return render_template('games_tool.html', tool=tool)"""

if "if tool_id == 'akinator-game':" not in content:
    content = content.replace(old_routing, new_routing)

with open('routes/games.py', 'w') as f:
    f.write(content)
