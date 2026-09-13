with open('templates/sitemap.xml', 'r') as f:
    content = f.read()

# Add video hub
if "video.video_hub" not in content:
    content = content.replace('<!-- Category Hubs -->', "<!-- Category Hubs -->\n    <url><loc>{{ url_for('video.video_hub', _external=True) }}</loc><changefreq>weekly</changefreq><priority>0.9</priority></url>")

# Add video tools
if "video_tools" not in content:
    video_block = """
    <!-- Dynamic Video Tools -->
    {% for tool in video_tools %}
    <url><loc>{{ url_for(tool.url, _external=True) }}</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>
    {% endfor %}
"""
    content = content.replace('</urlset>', video_block + '\n</urlset>')

# Add new Word and Excel PDF endpoints
if "word_to_pdf" not in content:
    hardcoded_pdf = """
    <url><loc>{{ url_for('pdf.word_to_pdf_page', _external=True) }}</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>
    <url><loc>{{ url_for('pdf.excel_to_pdf_page', _external=True) }}</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>"""
    content = content.replace('<!-- Hardcoded Tools -->', '<!-- Hardcoded Tools -->' + hardcoded_pdf)

with open('templates/sitemap.xml', 'w') as f:
    f.write(content)
