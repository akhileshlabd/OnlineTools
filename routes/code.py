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
    },
    'jwt-decoder': {
        'id': 'jwt-decoder',
        'name': 'JWT Decoder',
        'desc': 'Instantly decode JSON Web Tokens (JWT) to view headers and payloads.',
        'icon': 'fa-key',
        'seo_title': 'Free Online JWT Decoder - Decode JSON Web Tokens',
        'seo_desc': 'Decode JSON Web Tokens (JWT) instantly online. View the decoded JSON header and payload with 100% secure client-side processing.'
    },
    'url-encode-decode': {
        'id': 'url-encode-decode',
        'name': 'URL Encoder & Decoder',
        'desc': 'Encode strings for safe URL transmission or decode URL query strings.',
        'icon': 'fa-link',
        'seo_title': 'Free URL Encoder and Decoder Online',
        'seo_desc': 'Instantly URL-encode or URL-decode text strings and query parameters. Safe, private, and runs entirely in your browser.'
    },
    'uuid-generator': {
        'id': 'uuid-generator',
        'name': 'UUID / GUID Generator',
        'desc': 'Bulk generate cryptographically secure v4 UUIDs instantly.',
        'icon': 'fa-fingerprint',
        'seo_title': 'Free UUID v4 Generator - Bulk GUID Generator',
        'seo_desc': 'Generate cryptographically secure Version 4 UUIDs (GUIDs) instantly. Generate up to 500 unique identifiers at once for database seeding.'
    },
    'color-converter': {
        'id': 'color-converter',
        'name': 'HEX to RGB Color Converter',
        'desc': 'Convert CSS color formats between HEX, RGB, and HSL.',
        'icon': 'fa-palette',
        'seo_title': 'Free HEX to RGB Color Converter',
        'seo_desc': 'Instantly convert CSS color codes between HEX, RGB, and HSL formats. Perfect tool for frontend web developers and designers.'
    },
    'box-shadow-generator': {
        'id': 'box-shadow-generator',
        'name': 'CSS Box Shadow Generator',
        'desc': 'Visually design CSS box shadows and generate the code.',
        'icon': 'fa-clone',
        'seo_title': 'Free CSS Box Shadow Generator - Visual Tool',
        'seo_desc': 'Visually generate beautiful CSS3 box shadows. Adjust blur, spread, X/Y offsets, and colors to get instant CSS code for your web design.'
    },
    'markdown-editor': {
        'id': 'markdown-editor',
        'name': 'Markdown Editor & Preview',
        'desc': 'Write Markdown and preview the HTML rendering in real-time.',
        'icon': 'fa-markdown',
        'seo_title': 'Free Online Markdown Editor & Real-Time Preview',
        'seo_desc': 'Write and edit Markdown files with an instant, real-time HTML preview. A lightweight, client-side tool for developers to draft README files.'
    },
    'html-entities': {
        'id': 'html-entities',
        'name': 'HTML Entity Encoder',
        'desc': 'Encode or decode HTML characters securely.',
        'icon': 'fa-file-code',
        'seo_title': 'Free HTML Entity Encoder and Decoder Online',
        'seo_desc': 'Convert special characters to their corresponding HTML entities, or decode HTML entities back to plain text. 100% secure client-side processing.'
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
