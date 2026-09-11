from flask import Blueprint, render_template

math_bp = Blueprint('math', __name__, url_prefix='/math')

MATH_TOOLS = {
    'percentage': {
        'id': 'percentage',
        'name': 'Percentage Calculator',
        'desc': 'Calculate percentages, increases, and decreases instantly.',
        'icon': 'fa-percentage',
        'seo_title': 'Free Percentage Calculator - Fast & Online',
        'seo_desc': 'Calculate percentages instantly. Find out what X percent of Y is, or calculate percentage increases and decreases. Free, fast, and private.'
    },
    'age': {
        'id': 'age',
        'name': 'Age Calculator',
        'desc': 'Calculate your exact age in years, months, days, and hours.',
        'icon': 'fa-birthday-cake',
        'seo_title': 'Free Exact Age Calculator - Chronological Age',
        'seo_desc': 'Enter your date of birth to calculate your exact chronological age in years, months, weeks, and days. 100% private and runs in your browser.'
    },
    'discount': {
        'id': 'discount',
        'name': 'Discount & Sale Calculator',
        'desc': 'Calculate your final price and total savings during sales.',
        'icon': 'fa-tags',
        'seo_title': 'Free Discount & Sale Price Calculator',
        'seo_desc': 'Calculate the final sale price of an item after applying a percentage discount. Instantly see how much money you save.'
    }
}

@math_bp.route('/')
def math_hub():
    return render_template('hub_math.html', math_tools=MATH_TOOLS)

@math_bp.route('/tool/<tool_id>')
def math_tool_page(tool_id):
    tool = MATH_TOOLS.get(tool_id)
    if not tool:
        return "Math Tool not found", 404
    return render_template('math_tool.html', tool=tool)
