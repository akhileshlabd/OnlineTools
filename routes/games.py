from flask import Blueprint, render_template

games_bp = Blueprint('games', __name__, url_prefix='/games')

GAMES_TOOLS = {
    'tetris-game': {
        'id': 'tetris-game',
        'name': 'Classic Brick Game',
        'desc': 'Opens directly in fullscreen! The iconic block-stacking puzzle game. Clear lines to score points!',
        'icon': 'fa-cubes',
        'seo_title': 'Play Classic Brick Game (Tetris) Online for Free',
        'seo_desc': 'Play the ultimate classic Brick Game online for free. Stack the blocks, clear the lines, and beat your high score directly in your browser.'
    },
    'brick-breaker': {
        'id': 'brick-breaker',
        'name': 'Classic Brick Breaker',
        'desc': 'Opens directly in fullscreen! Play the classic retro Brick Breaker game with high-quality relaxed visuals.',
        'icon': 'fa-gamepad',
        'seo_title': 'Play Classic Brick Breaker Game Online for Free',
        'seo_desc': 'Play the ultimate retro Brick Breaker arcade game online for free. No downloads required, perfectly optimized for desktop and mobile browsers.'
    },
    'snake-game': {
        'id': 'snake-game',
        'name': 'Retro Snake',
        'desc': 'Opens directly in fullscreen! The timeless classic Snake game. Eat the apples and grow your high score!',
        'icon': 'fa-staff-snake',
        'seo_title': 'Play Retro Snake Game Online for Free',
        'seo_desc': 'Play the classic retro Snake game online for free. Control the snake, eat the apples, and compete for the highest score directly in your browser.'
    },
    'neon-qube': {
        'id': 'neon-qube',
        'name': 'Neon Qube Runner (Exclusive)',
        'desc': 'Opens directly in fullscreen! An exclusive, thrilling neon infinite runner game only available on FreeQube.',
        'icon': 'fa-cube',
        'seo_title': 'Play Neon Qube Runner Game - Exclusive on FreeQube',
        'seo_desc': 'Play Neon Qube Runner, an exclusive, relaxing yet thrilling retro arcade game only found on FreeQube. Play directly in your browser in full screen.'
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
