from flask import Blueprint, render_template

health_bp = Blueprint('health', __name__, url_prefix='/health')

HEALTH_TOOLS = {
    'bmi': {
        'id': 'bmi',
        'name': 'BMI Calculator',
        'desc': 'Calculate your Body Mass Index and check your health category.',
        'icon': 'fa-weight',
        'seo_title': 'Free BMI Calculator - Check Your Body Mass Index',
        'seo_desc': 'Calculate your Body Mass Index (BMI) instantly. Find out if you are at a healthy weight using our free, private online BMI calculator.'
    },
    'calorie': {
        'id': 'calorie',
        'name': 'Calorie & TDEE Calculator',
        'desc': 'Calculate your daily calorie needs for weight loss or maintenance.',
        'icon': 'fa-fire',
        'seo_title': 'Free Calorie and TDEE Calculator',
        'seo_desc': 'Calculate your Total Daily Energy Expenditure (TDEE) and find out exactly how many calories you need to eat to lose, maintain, or gain weight.'
    },
    'due-date': {
        'id': 'due-date',
        'name': 'Pregnancy Due Date Calculator',
        'desc': 'Calculate your estimated delivery date based on your LMP.',
        'icon': 'fa-baby',
        'seo_title': 'Free Pregnancy Due Date Calculator',
        'seo_desc': 'Calculate your exact pregnancy due date easily. Enter the first day of your last menstrual period (LMP) to instantly get your estimated delivery date.'
    }
}

@health_bp.route('/')
def health_hub():
    return render_template('hub_health.html', health_tools=HEALTH_TOOLS)

@health_bp.route('/tool/<tool_id>')
def health_tool_page(tool_id):
    tool = HEALTH_TOOLS.get(tool_id)
    if not tool:
        return "Health Tool not found", 404
    return render_template('health_tool.html', tool=tool)
