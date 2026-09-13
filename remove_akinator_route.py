import re

with open('routes/games.py', 'r') as f:
    content = f.read()

# Remove Akinator from GAMES_TOOLS
akinator_dict = """    'akinator-game': {
        'id': 'akinator-game',
        'name': 'Mind Reader (Akinator)',
        'desc': 'Think of a character and our client-side AI will guess who it is by asking 20 questions!',
        'icon': 'fa-brain',
        'seo_title': 'Play Mind Reader Guessing Game Online for Free',
        'seo_desc': 'Play our 100% client-side Mind Reader game. Think of any character and our zero-server AI will guess it instantly.'
    },

"""
content = content.replace(akinator_dict, '')

# Remove routing logic
akinator_routing = """    if tool_id == 'akinator-game':
        return render_template('akinator.html', tool=tool)
"""
content = content.replace(akinator_routing, '')

with open('routes/games.py', 'w') as f:
    f.write(content)
