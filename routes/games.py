from flask import Blueprint, render_template

games_bp = Blueprint('games', __name__, url_prefix='/games')

GAMES_TOOLS = {
    'brick-breaker': {
        'id': 'brick-breaker',
        'name': 'Classic Brick Breaker',
        'desc': 'Play the classic retro Brick Breaker game directly in your browser.',
        'icon': 'fa-gamepad',
        'seo_title': 'Play Classic Brick Breaker Game Online for Free',
        'seo_desc': 'Play the ultimate retro Brick Breaker arcade game online for free. No downloads required, perfectly optimized for desktop and mobile browsers.'
    },
    'snake-game': {
        'id': 'snake-game',
        'name': 'Retro Snake',
        'desc': 'The timeless classic Snake game. Eat the apples and grow your high score!',
        'icon': 'fa-staff-snake',
        'seo_title': 'Play Retro Snake Game Online for Free',
        'seo_desc': 'Play the classic retro Snake game online for free. Control the snake, eat the apples, and compete for the highest score directly in your browser.'
    }
}

@games_bp.route('/tool/<tool_id>')
def games_tool_page(tool_id):
    tool = GAMES_TOOLS.get(tool_id)
    if not tool:
        return "Game not found", 404
    return render_template('games_tool.html', tool=tool)

@games_bp.route('/')
def games_hub():
    return render_template('hub_games.html', games_tools=GAMES_TOOLS)
