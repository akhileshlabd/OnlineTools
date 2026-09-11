from flask import Blueprint, render_template

code_bp = Blueprint('code', __name__, url_prefix='/dev')

CODE_TOOLS = {
    'json-formatter': {
        'id': 'json-formatter',
        'name': 'JSON Formatter & Validator',
        'desc': 'Format, beautify, and validate JSON data instantly.',
        'icon': 'fa-code',
        'seo_title': 'Free Online JSON Formatter and Validator',
        'seo_desc': 'Beautify, format, and validate your JSON code online for free. Features instant syntax checking and clean formatting. 100% secure and runs in your browser.'
    },
    'code-diff': {
        'id': 'code-diff',
        'name': 'Text & Code Diff Checker',
        'desc': 'Compare two pieces of text or code to find differences.',
        'icon': 'fa-exchange-alt',
        'seo_title': 'Free Online Text and Code Diff Checker',
        'seo_desc': 'Compare two text files or code blocks to instantly highlight the differences, additions, and deletions. Completely free and secure client-side processing.'
    },
    'base64': {
        'id': 'base64',
        'name': 'Base64 Encoder/Decoder',
        'desc': 'Encode strings to Base64 or decode Base64 back to text.',
        'icon': 'fa-file-code',
        'seo_title': 'Free Online Base64 Encoder and Decoder',
        'seo_desc': 'Encode normal text into Base64 format or decode Base64 strings back into readable text. Free, fast, and fully runs in your local web browser.'
    },
    'hash-generator': {
        'id': 'hash-generator',
        'name': 'MD5 & SHA Hash Generator',
        'desc': 'Generate MD5, SHA-1, and SHA-256 cryptographic hashes.',
        'icon': 'fa-lock',
        'seo_title': 'Free MD5, SHA-1, SHA-256 Hash Generator',
        'seo_desc': 'Generate secure MD5, SHA-1, SHA-256, and SHA-512 hashes instantly from any text string. Built for developers with 100% local processing.'
    }
}

@code_bp.route('/tool/<tool_id>')
def code_tool_page(tool_id):
    tool = CODE_TOOLS.get(tool_id)
    if not tool:
        return "Developer Tool not found", 404
    return render_template('code_tool.html', tool=tool)

@code_bp.route('/')
def code_hub():
    return render_template('hub_code.html', code_tools=CODE_TOOLS)
