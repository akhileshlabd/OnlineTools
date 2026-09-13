import re

with open('templates/hub_pdf.html', 'r') as f:
    content = f.read()

new_cards = """
    <a href="{{ url_for('pdf.lock_pdf') }}" class="tool-card">
        <div class="icon-wrapper pdf-icon"><i class="fas fa-lock"></i></div>
        <h3>Lock PDF</h3>
        <p>Secure your PDF documents by adding strong password protection.</p>
    </a>
    <a href="{{ url_for('pdf.unlock_pdf') }}" class="tool-card">
        <div class="icon-wrapper pdf-icon"><i class="fas fa-unlock"></i></div>
        <h3>Unlock PDF</h3>
        <p>Remove passwords and encryption from protected PDF files.</p>
    </a>
"""

if "Lock PDF" not in content:
    # Insert right before the loop
    content = content.replace("{% for key, tool in pdf_tools.items() %}", new_cards + "\n    {% for key, tool in pdf_tools.items() %}")

with open('templates/hub_pdf.html', 'w') as f:
    f.write(content)
