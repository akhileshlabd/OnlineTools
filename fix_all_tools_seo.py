import os

templates_dir = 'templates'
tool_files = [
    'pdf_split.html', 'lock_pdf.html', 'unlock_pdf.html', 
    'image_to_pdf.html', 'word_to_pdf.html', 'excel_to_pdf.html',
    'resizer.html', 'image_converter.html', 'qr_generator.html'
]

for filename in tool_files:
    filepath = os.path.join(templates_dir, filename)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r') as f:
        content = f.read()
        
    if 'SEO Content for AdSense' not in content:
        # Extract title from h2 if exists, or use filename
        tool_name = filename.replace('.html', '').replace('_', ' ').title()
        
        seo_block = f"""
<!-- SEO Content for AdSense Compliance -->
<div class="container bg-white p-4 p-md-5 rounded shadow-sm mt-5 mb-4 text-start" style="max-width: 800px; margin: 0 auto;">
    <h2 class="fw-bold mb-3">Best Free {tool_name} Online</h2>
    <p>Are you looking for the fastest and most secure way to process your files? Our <strong>Free {tool_name}</strong> tool is designed to provide professional-grade results directly in your web browser. There is no need to download heavy software or pay for premium subscriptions.</p>
    
    <h3 class="fw-bold mt-4">Why Choose Our {tool_name}?</h3>
    <ul class="mb-4">
        <li><strong>Maximum Privacy & Security:</strong> We utilize state-of-the-art client-side processing. This means your files are processed locally on your device's RAM and CPU. Your data is NEVER uploaded to an external server, ensuring absolute privacy.</li>
        <li><strong>100% Free Forever:</strong> Use this tool as many times as you need. We do not enforce daily limits, require email registrations, or stamp watermarks on your final files.</li>
        <li><strong>Lightning Fast Speed:</strong> By skipping the cloud upload and download process, your files are ready almost instantly, regardless of your internet speed.</li>
    </ul>

    <h3 class="fw-bold mt-4">How to Use This Tool</h3>
    <ol>
        <li>Click the file selection button or simply drag and drop your document into the secure area above.</li>
        <li>Configure any necessary settings or options provided by the tool interface.</li>
        <li>Click the process button. Your file will be generated instantly and downloaded securely to your device.</li>
    </ol>
</div>
{{% endblock %}}
"""
        # Replace the FIRST {% endblock %} which closes the content block
        parts = content.split('{% endblock %}')
        if len(parts) >= 2:
            new_content = parts[0] + seo_block + '{% endblock %}'.join(parts[1:])
            with open(filepath, 'w') as f:
                f.write(new_content)
            print(f"Added SEO block to {filename}")
        else:
            print(f"Could not find endblock in {filename}")
