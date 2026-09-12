from flask import Blueprint, render_template

text_bp = Blueprint('text', __name__, url_prefix='/text')

TEXT_TOOLS = {
    'word-counter': {
        'id': 'word-counter',
        'name': 'Word & Character Counter',
        'desc': 'Count words, characters, and estimate reading time instantly.',
        'icon': 'fa-font',
        'seo_title': 'Free Online Word and Character Counter',
        'seo_desc': 'Instantly count words, characters, sentences, and paragraphs in your text. Perfect for essays, SEO writing, and social media posts. 100% free.'
    },
    'case-converter': {
        'id': 'case-converter',
        'name': 'Case Converter',
        'desc': 'Change text to UPPERCASE, lowercase, Title Case, and more.',
        'icon': 'fa-text-height',
        'seo_title': 'Free Text Case Converter Online',
        'seo_desc': 'Easily convert your text to uppercase, lowercase, title case, or sentence case. Fast, free, and completely secure client-side processing.'
    },
    'lorem-ipsum': {
        'id': 'lorem-ipsum',
        'name': 'Lorem Ipsum Generator',
        'desc': 'Generate dummy text for web design and mockups.',
        'icon': 'fa-paragraph',
        'seo_title': 'Free Lorem Ipsum Dummy Text Generator',
        'seo_desc': 'Generate custom Lorem Ipsum placeholder text for your web design, layouts, and mockups. Fast, free, and highly customizable.'
    },
    'meta-tags': {
        'id': 'meta-tags',
        'name': 'Meta Tag Generator',
        'desc': 'Generate SEO-optimized HTML meta tags for your website.',
        'icon': 'fa-tags',
        'seo_title': 'Free Meta Tag Generator Tool - SEO Tags',
        'seo_desc': 'Easily generate custom HTML meta tags for your website. Improve your search engine rankings with perfectly formatted title and description tags.'
    },
    'keyword-density': {
        'id': 'keyword-density',
        'name': 'Keyword Density Checker',
        'desc': 'Analyze text to find the most frequently used keywords.',
        'icon': 'fa-chart-pie',
        'seo_title': 'Free Keyword Density Checker - SEO Tool',
        'seo_desc': 'Analyze your article or webpage text to find the most used words and phrases. Optimize your keyword density and avoid keyword stuffing.'
    }
}

@text_bp.route('/')
def text_hub():
    return render_template('hub_text.html', text_tools=TEXT_TOOLS)

@text_bp.route('/tool/<tool_id>')
def text_tool_page(tool_id):
    tool = TEXT_TOOLS.get(tool_id)
    if not tool:
        return "Text Tool not found", 404
    return render_template('text_tool.html', tool=tool)
