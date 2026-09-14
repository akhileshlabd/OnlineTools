with open('templates/hub_games.html', 'r') as f:
    content = f.read()
    
# Manual replacement
content = content.replace('    <div class="col-md-6 col-lg-4 d-flex">', '    {% if features["feature_game_" ~ tool.id] %}\n    <div class="col-md-6 col-lg-4 d-flex">')
content = content.replace('        </a>\n    </div>', '        </a>\n    </div>\n    {% endif %}')

with open('templates/hub_games.html', 'w') as f:
    f.write(content)
