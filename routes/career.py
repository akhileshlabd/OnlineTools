from flask import Blueprint, render_template

career_bp = Blueprint('career', __name__, url_prefix='/career')

CAREER_TOOLS = {
    'resume-builder': {
        'id': 'resume-builder',
        'name': 'Free Resume Builder',
        'desc': 'Build a professional, ATS-friendly resume in minutes. 100% free and private.',
        'icon': 'fa-file-invoice',
        'seo_title': 'Free Online Resume Builder - ATS Friendly CV Maker',
        'seo_desc': 'Create a professional, ATS-friendly resume instantly. No sign-up required. Your data never leaves your browser for maximum privacy. Download as PDF.'
    }
}

@career_bp.route('/')
def career_hub():
    return render_template('hub_career.html', career_tools=CAREER_TOOLS)

@career_bp.route('/tool/<tool_id>')
def career_tool_page(tool_id):
    tool = CAREER_TOOLS.get(tool_id)
    if not tool:
        return "Career Tool not found", 404
    return render_template('career_tool.html', tool=tool)
