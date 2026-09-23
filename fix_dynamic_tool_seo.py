with open('templates/dynamic_tool.html', 'r') as f:
    content = f.read()

# Check if it already has SEO content
if 'SEO Content for AdSense' not in content:
    seo_block = """
<!-- SEO Content for AdSense Compliance -->
<div class="container bg-white p-4 p-md-5 rounded shadow-sm mt-5 mb-4 text-start" style="max-width: 800px; margin: 0 auto;">
    <h2 class="fw-bold mb-3">Best Free {{ tool_name }} Online</h2>
    <p>{{ tool_desc }} Our {{ tool_name }} is designed to be the fastest, most reliable, and 100% secure way to manage your files directly in your browser.</p>
    
    <h3 class="fw-bold mt-4">Why Choose Free Qube for {{ tool_name }}?</h3>
    <ul class="mb-4">
        <li><strong>Offline-Level Security:</strong> We use advanced client-side processing to execute the {{ tool_name }} logic directly in your browser's memory. Your files are never uploaded to any server, guaranteeing 100% data privacy.</li>
        <li><strong>100% Free & Unlimited:</strong> Process as many files as you want, as many times as you want. There are no daily limits, hidden fees, or watermarks added to your final document.</li>
        <li><strong>Blazing Fast:</strong> Forget about slow upload bars. Because the {{ tool_name }} happens on your local device CPU, it finishes almost instantly without relying on your internet connection speed.</li>
    </ul>

    <h3 class="fw-bold mt-4">How to Use the {{ tool_name }}</h3>
    <ol>
        <li>Click "Choose File" or drag and drop the file you want to process into the secure drop zone above.</li>
        <li>Adjust any settings or inputs required for the {{ tool_name }}.</li>
        <li>For images, the preview updates instantly. For PDFs, click the process button. Your browser will instantly generate and download the final file locally.</li>
    </ol>
</div>
{% endblock %}
"""
    new_content = content.replace('{% endblock %}', seo_block, 1) # replace first occurrence (which is the end of content block)
    # wait, there are multiple endblocks if scripts are there.
    # Let's replace the one right before {% block scripts %}
    # actually, I'll use regex or string find.
    
    parts = content.split('{% endblock %}')
    if len(parts) >= 2:
        new_content = parts[0] + seo_block + '{% endblock %}'.join(parts[1:])
        with open('templates/dynamic_tool.html', 'w') as f:
            f.write(new_content)
        print("Added SEO block to dynamic_tool.html")
    else:
        print("Could not find endblock")
