with open('templates/admin_dashboard.html', 'r') as f:
    content = f.read()

import re
old_features_html = r'<div class="row">\s*{% for category, items in features_grouped.items\(\) %}.*?{% endfor %}\s*</div>'

new_features_html = """<div class="row">
                <div class="col-12">
                    <div class="accordion" id="featuresAccordion">
                        {% for group in features_grouped %}
                        <div class="accordion-item mb-3 border" style="border-radius: 8px; overflow: hidden;">
                            <div class="accordion-header d-flex justify-content-between align-items-center" style="background: white; padding: 15px 20px;">
                                <div class="d-flex align-items-center gap-3">
                                    <div class="form-check form-switch fs-4 m-0 p-0 d-flex align-items-center" style="min-height: auto;">
                                        <input class="form-check-input m-0" type="checkbox" style="cursor:pointer;"
                                               {{ 'checked' if group.is_enabled else '' }} 
                                               onchange="toggleFeature('{{ group.key }}')">
                                    </div>
                                    <h5 style="margin: 0; font-weight: 800; color: #1e293b;">
                                        <i class="fas {{ group.icon }} me-2 text-primary"></i>{{ group.label }}
                                    </h5>
                                </div>
                                {% if group.children %}
                                <button class="btn btn-sm btn-outline-secondary" type="button" data-bs-toggle="collapse" data-bs-target="#collapse_{{ group.key }}" aria-expanded="false" style="font-weight: 700; border-radius: 20px; padding: 4px 15px;">
                                    Expand Settings <i class="fas fa-chevron-down ms-1"></i>
                                </button>
                                {% endif %}
                            </div>
                            
                            {% if group.children %}
                            <div id="collapse_{{ group.key }}" class="accordion-collapse collapse" data-bs-parent="#featuresAccordion">
                                <div class="accordion-body bg-light border-top">
                                    <div class="row">
                                        {% for child in group.children %}
                                        <div class="col-md-6 mb-2">
                                            <div class="d-flex justify-content-between align-items-center p-3 bg-white rounded border">
                                                <div style="font-weight: 600; color: #475569;">{{ child.label }}</div>
                                                <div class="form-check form-switch fs-5 m-0">
                                                    <input class="form-check-input" type="checkbox" style="cursor:pointer;"
                                                           {{ 'checked' if child.is_enabled else '' }} 
                                                           onchange="toggleFeature('{{ child.key }}')">
                                                </div>
                                            </div>
                                        </div>
                                        {% endfor %}
                                    </div>
                                </div>
                            </div>
                            {% endif %}
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>"""

content = re.sub(old_features_html, new_features_html, content, flags=re.DOTALL)

# Add font-awesome if not present (although it is likely in base.html, it's not in the standalone admin layout)
if 'font-awesome' not in content:
    content = content.replace('</head>', '    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">\n</head>')

with open('templates/admin_dashboard.html', 'w') as f:
    f.write(content)
