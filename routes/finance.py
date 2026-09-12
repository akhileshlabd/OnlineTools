from flask import Blueprint, render_template

finance_bp = Blueprint('finance', __name__, url_prefix='/finance')

FINANCE_TOOLS = {
    'sip': {
        'id': 'sip',
        'name': 'SIP Calculator',
        'desc': 'Calculate the future value of your monthly Systematic Investment Plan.',
        'icon': 'fa-chart-line',
        'seo_title': 'Free SIP Calculator Online - Calculate Mutual Fund Returns',
        'seo_desc': 'Use our free SIP calculator to estimate your mutual fund returns. Plan your monthly investments with our interactive charts and accurate future value projections.',
        'formula': 'sip',
        'inputs': [
            {'id': 'amount', 'label': 'Monthly Investment', 'min': 500, 'max': 100000, 'step': 500, 'default': 5000, 'prefix': '₹'},
            {'id': 'rate', 'label': 'Expected Return Rate (p.a)', 'min': 1, 'max': 30, 'step': 0.1, 'default': 12, 'suffix': '%'},
            {'id': 'years', 'label': 'Time Period', 'min': 1, 'max': 40, 'step': 1, 'default': 10, 'suffix': 'Yr'}
        ]
    },
    'lumpsum': {
        'id': 'lumpsum',
        'name': 'Lumpsum Calculator',
        'desc': 'Calculate the wealth you can generate from a one-time investment.',
        'icon': 'fa-piggy-bank',
        'seo_title': 'Free Lumpsum Investment Calculator',
        'seo_desc': 'Estimate the future value of your one-time investments with our free lumpsum calculator. See your wealth grow with compound interest.',
        'formula': 'lumpsum',
        'inputs': [
            {'id': 'amount', 'label': 'Total Investment', 'min': 1000, 'max': 5000000, 'step': 1000, 'default': 100000, 'prefix': '₹'},
            {'id': 'rate', 'label': 'Expected Return Rate (p.a)', 'min': 1, 'max': 30, 'step': 0.1, 'default': 12, 'suffix': '%'},
            {'id': 'years', 'label': 'Time Period', 'min': 1, 'max': 40, 'step': 1, 'default': 10, 'suffix': 'Yr'}
        ]
    },
    'emi': {
        'id': 'emi',
        'name': 'EMI Calculator',
        'desc': 'Calculate your monthly EMI for Home, Car, or Personal Loans.',
        'icon': 'fa-home',
        'seo_title': 'Free Loan EMI Calculator Online',
        'seo_desc': 'Calculate your monthly EMI for home, car, or personal loans instantly. Break down your principal and interest amounts with our interactive charts.',
        'formula': 'emi',
        'inputs': [
            {'id': 'amount', 'label': 'Loan Amount', 'min': 10000, 'max': 50000000, 'step': 10000, 'default': 1000000, 'prefix': '₹'},
            {'id': 'rate', 'label': 'Interest Rate (p.a)', 'min': 1, 'max': 30, 'step': 0.1, 'default': 8.5, 'suffix': '%'},
            {'id': 'years', 'label': 'Loan Tenure', 'min': 1, 'max': 30, 'step': 1, 'default': 5, 'suffix': 'Yr'}
        ]
    },
    'fd': {
        'id': 'fd',
        'name': 'FD Calculator',
        'desc': 'Calculate your Fixed Deposit maturity amount and interest earned.',
        'icon': 'fa-building-columns',
        'seo_title': 'Free FD Calculator - Fixed Deposit Maturity Calculator',
        'seo_desc': 'Calculate the maturity amount and interest earned on your Fixed Deposits. Free, accurate, and completely private.',
        'formula': 'fd',
        'inputs': [
            {'id': 'amount', 'label': 'Total Investment', 'min': 5000, 'max': 10000000, 'step': 1000, 'default': 100000, 'prefix': '₹'},
            {'id': 'rate', 'label': 'Interest Rate (p.a)', 'min': 1, 'max': 15, 'step': 0.1, 'default': 6.5, 'suffix': '%'},
            {'id': 'years', 'label': 'Time Period', 'min': 1, 'max': 25, 'step': 1, 'default': 5, 'suffix': 'Yr'}
        ]
    },
    'compound': {
        'id': 'compound',
        'name': 'Compound Interest Calculator',
        'desc': 'Visualize the power of compounding on your investments over time.',
        'icon': 'fa-chart-pie',
        'seo_title': 'Free Compound Interest Calculator Online',
        'seo_desc': 'Calculate compound interest effortlessly. Visualize your wealth growth with our interactive charts breaking down principal and total interest.',
        'formula': 'compound',
        'inputs': [
            {'id': 'amount', 'label': 'Initial Principal', 'min': 1000, 'max': 5000000, 'step': 1000, 'default': 100000, 'prefix': '₹'},
            {'id': 'rate', 'label': 'Interest Rate (p.a)', 'min': 1, 'max': 30, 'step': 0.1, 'default': 12, 'suffix': '%'},
            {'id': 'years', 'label': 'Time Period', 'min': 1, 'max': 40, 'step': 1, 'default': 10, 'suffix': 'Yr'},
            {'id': 'freq', 'label': 'Compounds per Year', 'min': 1, 'max': 12, 'step': 1, 'default': 1, 'suffix': 'x'}
        ]
    }
}

@finance_bp.route('/calculator/<tool_id>')
def calculator_page(tool_id):
    tool = FINANCE_TOOLS.get(tool_id)
    if not tool:
        return "Calculator not found", 404
    return render_template('finance_calculator.html', tool=tool)

@finance_bp.route('/')
def finance_hub():
    return render_template('hub_finance.html', finance_tools=FINANCE_TOOLS)
