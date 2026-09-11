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


CAREER_TOOLS = {
    'cover_letter': {'id': 'cover_letter', 'type': 'career', 'name': 'Cover Letter Builder', 'desc': 'Generate a professional cover letter.', 'icon': 'fa-envelope-open-text', 'endpoint': '/career-process/cover_letter', 'inputs': [{'name': 'hiring_manager', 'type': 'text', 'label': 'Hiring Manager Name'}, {'name': 'company', 'type': 'text', 'label': 'Company Name'}, {'name': 'role', 'type': 'text', 'label': 'Target Role'}, {'name': 'skills', 'type': 'textarea', 'label': 'Key Skills & Why you are a fit'}]},
    'resignation': {'id': 'resignation', 'type': 'career', 'name': 'Resignation Letter', 'desc': 'Generate a standard two-week notice.', 'icon': 'fa-door-open', 'endpoint': '/career-process/resignation', 'inputs': [{'name': 'manager', 'type': 'text', 'label': 'Manager Name'}, {'name': 'date', 'type': 'date', 'label': 'Last Day of Work'}]},
    'thank_you': {'id': 'thank_you', 'type': 'career', 'name': 'Interview Thank You', 'desc': 'Follow up professionally after an interview.', 'icon': 'fa-handshake', 'endpoint': '/career-process/thank_you', 'inputs': [{'name': 'interviewer', 'type': 'text', 'label': 'Interviewer Name'}, {'name': 'role', 'type': 'text', 'label': 'Interviewed Role'}]},
    'cold_email': {'id': 'cold_email', 'type': 'career', 'name': 'Cold Outreach Email', 'desc': 'Template for networking with recruiters.', 'icon': 'fa-paper-plane', 'endpoint': '/career-process/cold_email', 'inputs': [{'name': 'recruiter', 'type': 'text', 'label': 'Recruiter Name'}, {'name': 'company', 'type': 'text', 'label': 'Company'}, {'name': 'background', 'type': 'textarea', 'label': 'Brief Background'}]},
    'recommendation': {'id': 'recommendation', 'type': 'career', 'name': 'Letter of Recommendation', 'desc': 'Template for recommending a colleague.', 'icon': 'fa-star', 'endpoint': '/career-process/recommendation', 'inputs': [{'name': 'person', 'type': 'text', 'label': 'Person You Are Recommending'}, {'name': 'relationship', 'type': 'text', 'label': 'Your Relationship (e.g. Manager)'}, {'name': 'strengths', 'type': 'textarea', 'label': 'Key Strengths'}]},
    'offer_negotiation': {'id': 'offer_negotiation', 'type': 'career', 'name': 'Salary Negotiation', 'desc': 'Professional email to negotiate an offer.', 'icon': 'fa-comments-dollar', 'endpoint': '/career-process/offer_negotiation', 'inputs': [{'name': 'company', 'type': 'text', 'label': 'Company Name'}, {'name': 'current_offer', 'type': 'text', 'label': 'Current Offer'}, {'name': 'target_offer', 'type': 'text', 'label': 'Target Offer'}]},
    'promotion_request': {'id': 'promotion_request', 'type': 'career', 'name': 'Promotion Request', 'desc': 'Formal request for a promotion/raise.', 'icon': 'fa-arrow-up', 'endpoint': '/career-process/promotion_request', 'inputs': [{'name': 'manager', 'type': 'text', 'label': 'Manager Name'}, {'name': 'achievements', 'type': 'textarea', 'label': 'Recent Key Achievements'}]},
    'reference_list': {'id': 'reference_list', 'type': 'career', 'name': 'Reference List Builder', 'desc': 'Generate a professional reference sheet.', 'icon': 'fa-users', 'endpoint': '/career-process/reference_list', 'inputs': [{'name': 'references', 'type': 'textarea', 'label': 'List References (Name, Title, Email)'}]},
    'networking': {'id': 'networking', 'type': 'career', 'name': 'Networking Request', 'desc': 'Ask for a coffee chat or informational interview.', 'icon': 'fa-coffee', 'endpoint': '/career-process/networking', 'inputs': [{'name': 'contact', 'type': 'text', 'label': 'Contact Name'}, {'name': 'topic', 'type': 'text', 'label': 'Topic to Discuss'}]}
}

@resume_bp.route('/career-tool/<tool_id>')
def dynamic_career_tool(tool_id):
    tool = CAREER_TOOLS.get(tool_id)
    if not tool: return "Tool not found", 404
    return render_template('dynamic_tool.html', tool=tool)

@resume_bp.route('/career-process/<tool_id>', methods=['POST'])
def process_dynamic_career(tool_id):
    from weasyprint import HTML
    import io
    from flask import send_file
    
    form_data = request.form.to_dict()
    
    # Generic template rendering
    html_content = f"<html><body style='font-family: Arial, sans-serif; padding: 40px; line-height: 1.6;'>"
    html_content += f"<h1 style='color: #333; border-bottom: 2px solid #ccc; padding-bottom: 10px;'>{tool_id.replace('_', ' ').title()}</h1>"
    
    for key, value in form_data.items():
        html_content += f"<h3 style='margin-bottom: 5px; color: #555;'>{key.replace('_', ' ').title()}:</h3>"
        html_content += f"<p style='margin-top: 0; white-space: pre-wrap;'>{value}</p>"
        
    html_content += "</body></html>"
    
    pdf_bytes = HTML(string=html_content).write_pdf()
    buf = io.BytesIO(pdf_bytes)
    
    return send_file(buf, as_attachment=True, download_name=f"{tool_id}.pdf", mimetype='application/pdf')
