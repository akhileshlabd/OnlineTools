import os

hubs = ['hub_health.html', 'hub_math.html', 'hub_text.html', 'hub_network.html']

for hub in hubs:
    filepath = f"templates/{hub}"
    with open(filepath, 'r') as f:
        content = f.read()
    
    hub_name = hub.replace('hub_', '').replace('.html', '').title()
    
    seo_block = f"""
<!-- SEO Content for AdSense Compliance -->
<div class="container bg-white p-4 p-md-5 rounded shadow-sm mt-5 mb-4 text-start">
    <h2 class="fw-bold mb-3">Free {hub_name} Tools Online</h2>
    <p>Welcome to our comprehensive suite of <strong>free online {hub_name.lower()} tools</strong>. Whether you are a student, professional, or just looking to simplify your daily tasks, our highly optimized web utilities provide everything you need directly in your browser.</p>
    
    <h3 class="fw-bold mt-4">Why Use Free Qube {hub_name} Utilities?</h3>
    <p>We designed these tools with one primary goal: <strong>Privacy and Speed</strong>. Unlike other platforms that force you to create accounts, pay subscription fees, or upload sensitive data to their cloud servers, Free Qube executes all processing logic locally on your device.</p>
    
    <ul class="mb-4 mt-3">
        <li><strong>No Cloud Uploads:</strong> Absolute privacy for your data.</li>
        <li><strong>100% Free:</strong> No paywalls or hidden charges.</li>
        <li><strong>Instant Results:</strong> Powered by highly efficient JavaScript.</li>
    </ul>
    <p>Explore our selection of tools above to start optimizing your workflow today.</p>
</div>
{{% endblock %}}
"""
    parts = content.split('{% endblock %}')
    if len(parts) >= 2:
        new_content = parts[0] + seo_block + '{% endblock %}'.join(parts[1:])
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Fixed {hub}")
