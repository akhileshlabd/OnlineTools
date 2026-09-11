from flask import Blueprint, render_template, request, make_response

resume_bp = Blueprint('resume', __name__)

@resume_bp.route('/resume_builder')
def resume_builder():
    return render_template('resume_builder.html')

@resume_bp.route('/generate_resume', methods=['POST'])
def generate_resume():
    from weasyprint import HTML
    data = request.form.to_dict()
    section_titles = request.form.getlist('section_title[]')
    section_contents = request.form.getlist('section_content[]')

    dynamic_sections = []
    for title, content in zip(section_titles, section_contents):
        if title.strip() and content.strip():
            dynamic_sections.append({'title': title.strip(), 'content': content.strip()})

    data['dynamic_sections'] = dynamic_sections

    rendered = render_template('resume_template.html', **data)
    pdf = HTML(string=rendered).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=resume.pdf'
    return response

@resume_bp.route('/preview_resume', methods=['POST'])
def preview_resume():
    data = request.form.to_dict()
    section_titles = request.form.getlist('section_title[]')
    section_contents = request.form.getlist('section_content[]')

    dynamic_sections = []
    for title, content in zip(section_titles, section_contents):
        if title.strip() and content.strip():
            dynamic_sections.append({'title': title.strip(), 'content': content.strip()})

    data['dynamic_sections'] = dynamic_sections

    return render_template('resume_template.html', **data)


# Career dynamic tools removed — they were producing low-quality output
# that hurt our reputation. Resume Builder is the only career tool we keep.
CAREER_TOOLS = {}

