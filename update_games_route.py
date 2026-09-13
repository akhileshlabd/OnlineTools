import re

with open('routes/games.py', 'r') as f:
    content = f.read()

# Add Sudoku to GAMES_TOOLS
sudoku_dict = """    'sudoku-game': {
        'id': 'sudoku-game',
        'name': 'Sudoku (Easy Mode)',
        'desc': 'Play classic Sudoku online. Designed with a relaxing easy mode for casual puzzle solving.',
        'icon': 'fa-th',
        'seo_title': 'Play Free Online Sudoku (Easy Mode)',
        'seo_desc': 'Play classic Sudoku online for free. Clean interface, responsive design, and perfect for beginners looking for a relaxing brain puzzle.'
    },
"""

# Insert right after GAMES_TOOLS = {
if "'sudoku-game'" not in content:
    content = content.replace("GAMES_TOOLS = {", "GAMES_TOOLS = {\n" + sudoku_dict)

# Add routing logic
sudoku_routing = """    if tool_id == 'sudoku-game':
        return render_template('sudoku.html', tool=tool)
"""

if "if tool_id == 'sudoku-game':" not in content:
    content = content.replace("return render_template('games_tool.html', tool=tool)", sudoku_routing + "    return render_template('games_tool.html', tool=tool)")

with open('routes/games.py', 'w') as f:
    f.write(content)
