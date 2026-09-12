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
    'serp-simulator': {
        'id': 'serp-simulator',
        'name': 'Google SERP Simulator',
        'desc': 'Preview how your web page looks in Google Search results.',
        'icon': 'fa-search',
        'seo_title': 'Free Google SERP Simulator - Search Preview Tool',
        'seo_desc': 'Preview how your website title and meta description will appear in Google Search Results. Optimize your snippet for higher click-through rates.'
    },
    'keyword-density': {
        'id': 'keyword-density',
        'name': 'Keyword Density Checker',
        'desc': 'Analyze text to find the most frequently used keywords.',
        'icon': 'fa-chart-pie',
        'seo_title': 'Free Keyword Density Checker - SEO Tool',
        'seo_desc': 'Analyze your article or webpage text to find the most used words and phrases. Optimize your keyword density and avoid keyword stuffing.'
    },
    'slug-generator': {
        'id': 'slug-generator',
        'name': 'URL Slug Generator',
        'desc': 'Convert any text string into a clean, SEO-friendly URL slug.',
        'icon': 'fa-link',
        'seo_title': 'Free URL Slug Generator - Create SEO Friendly Links',
        'seo_desc': 'Instantly convert article titles and strings into clean, hyphenated, SEO-friendly URL slugs. Removes special characters automatically.'
    },
    'remove-line-breaks': {
        'id': 'remove-line-breaks',
        'name': 'Remove Line Breaks',
        'desc': 'Remove unwanted line breaks and extra spaces from text.',
        'icon': 'fa-eraser',
        'seo_title': 'Free Tool to Remove Line Breaks and Whitespace',
        'seo_desc': 'Instantly clean messy text formatting. Remove unwanted line breaks, paragraph breaks, and double spaces from copied PDF text.'
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
