from flask import Blueprint, render_template

learn_bp = Blueprint('learn', __name__, url_prefix='/learn')

LEARN_MODULES = {
    'salesforce': {
        'id': 'salesforce',
        'title': 'Salesforce Complete Masterclass',
        'subtitle': 'Zero to Hero: Admin, Apex, LWC, Integrations, DevOps CI/CD & Agentforce AI',
        'badge': 'Comprehensive Guide',
        'badge_color': 'primary',
        'icon': 'fa-cloud',
        'color': '#00a1e0',
        'duration': '8 Sections • 60+ In-Depth Lessons',
        'description': 'Master the world’s #1 enterprise cloud platform from scratch. Modular, child-friendly explanations covering Administrator Security, Flows, Apex, LWC, Enterprise Integrations, VS Code & CI/CD DevOps, and the revolutionary Agentforce AI platform.'
    },
    'html': {
        'id': 'html',
        'title': 'Modern HTML5 Fundamentals',
        'subtitle': 'The Structural Foundation of the Web: Semantics, Forms, SEO & Interactive Hands-On Lab',
        'badge': 'Live Hands-On Lab',
        'badge_color': 'danger',
        'icon': 'fa-html5',
        'color': '#e34f26',
        'duration': '9 Modules • Live Sandbox Lab',
        'description': 'Learn HTML5 from the ground up with intuitive analogies. Master modern semantic markup, responsive multimedia, accessible forms, DOM architecture, and practice with our interactive split-screen HTML lab.'
    },
    'javascript': {
        'id': 'javascript',
        'title': 'Modern JavaScript (ES6+)',
        'subtitle': 'Interactive Web Programming: Variables, Functions, DOM, Async/Await & Algorithms',
        'badge': 'Interactive Sandbox',
        'badge_color': 'warning',
        'icon': 'fa-js',
        'color': '#f7df1e',
        'duration': '10 Modules • 38 Lessons',
        'description': 'Understand how JavaScript brings websites to life. From fundamental logic and array transformations to async programming and live browser DOM manipulation with our in-browser JS Runner.'
    }
}

@learn_bp.route('/')
def learn_hub():
    return render_template('learn/hub.html', modules=LEARN_MODULES)

@learn_bp.route('/salesforce')
def learn_salesforce():
    return render_template('learn/salesforce.html', module=LEARN_MODULES['salesforce'])

@learn_bp.route('/html')
def learn_html():
    return render_template('learn/html.html', module=LEARN_MODULES['html'])

@learn_bp.route('/javascript')
def learn_javascript():
    return render_template('learn/javascript.html', module=LEARN_MODULES['javascript'])

