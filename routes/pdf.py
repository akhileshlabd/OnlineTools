from flask import Blueprint, render_template

pdf_bp = Blueprint('pdf', __name__, url_prefix='/pdf')

@pdf_bp.route('/pdf-merger', methods=['GET'])
def pdf_merger():
    return render_template('pdf_merger.html')

@pdf_bp.route('/pdf-splitter', methods=['GET'])
def pdf_splitter():
    return render_template('pdf_split.html')

@pdf_bp.route('/image-to-pdf', methods=['GET'])
def image_to_pdf():  
    return render_template('image_to_pdf.html')

PDF_TOOLS = {
    'rotate_pdf': {'id': 'rotate_pdf', 'type': 'pdf', 'name': 'Rotate PDF', 'desc': 'Rotate all pages by 90, 180, or 270 degrees.', 'icon': 'fa-sync', 'inputs': [{'name': 'angle', 'type': 'number', 'label': 'Angle (90, 180, 270)', 'min': 90, 'max': 270}]},
    'remove_page': {'id': 'remove_page', 'type': 'pdf', 'name': 'Remove Page', 'desc': 'Delete a specific page from your PDF.', 'icon': 'fa-trash-alt', 'inputs': [{'name': 'page_num', 'type': 'number', 'label': 'Page Number to Remove', 'min': 1}]},
    'add_blank': {'id': 'add_blank', 'type': 'pdf', 'name': 'Add Blank Page', 'desc': 'Add a blank page to the end of the document.', 'icon': 'fa-plus-square', 'inputs': []},
    'watermark': {'id': 'watermark', 'type': 'pdf', 'name': 'Add Watermark', 'desc': 'Add text or image watermark.', 'icon': 'fa-water', 'inputs': [{'name': 'watermark_text', 'type': 'text', 'label': 'Watermark Text'}]}
}

@pdf_bp.route('/pdf-tool/<tool_id>')
def dynamic_pdf_tool(tool_id):
    tool = PDF_TOOLS.get(tool_id)
    if not tool: return "Tool not found", 404
    return render_template('dynamic_tool.html', tool=tool)

@pdf_bp.route('/')
def pdf_hub():
    return render_template('hub_pdf.html', pdf_tools=PDF_TOOLS)
