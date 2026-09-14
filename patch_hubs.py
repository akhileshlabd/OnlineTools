import re

def patch_hub(filename, mappings, loop_name=None, feature_prefix=None):
    try:
        with open(filename, 'r') as f:
            content = f.read()
            
        # Patch hardcoded tools
        for route, feature in mappings.items():
            pattern = r'(<a href="\{\{\s*url_for\(\'' + route + r'\'\)\s*\}\}".*?</a>)'
            
            def replacer(match):
                original = match.group(1)
                if '{% if features' in original: return original
                return f"{{% if features['{feature}'] %}}\n{original}\n{{% endif %}}"
                
            content = re.sub(pattern, replacer, content, flags=re.DOTALL)
            
        # Patch dynamic loops
        if loop_name and feature_prefix:
            pattern = r'({% for key, tool in ' + loop_name + r'\.items\(\) %}\s*)(<a href=".*?</a>)(\s*{% endfor %})'
            def loop_replacer(match):
                pre = match.group(1)
                inner = match.group(2)
                post = match.group(3)
                if '{% if features' in inner: return match.group(0)
                return f"{pre}{{% if features['{feature_prefix}_' ~ tool.id] %}}\n{inner}\n{{% endif %}}{post}"
            
            content = re.sub(pattern, loop_replacer, content, flags=re.DOTALL)
            
        with open(filename, 'w') as f:
            f.write(content)
    except FileNotFoundError:
        pass

# PDF
patch_hub('templates/hub_pdf.html', {
    'pdf.pdf_merger': 'feature_pdf_merger',
    'pdf.pdf_splitter': 'feature_pdf_splitter',
    'pdf.word_to_pdf': 'feature_pdf_word_to_pdf',
    'pdf.excel_to_pdf': 'feature_pdf_excel_to_pdf',
    'pdf.image_to_pdf': 'feature_pdf_image_to_pdf',
    'pdf.lock_pdf': 'feature_pdf_lock',
    'pdf.unlock_pdf': 'feature_pdf_unlock',
}, 'pdf_dynamic_tools', 'feature_pdf')

# Image
patch_hub('templates/hub_image.html', {
    'image.resizer': 'feature_image_resizer',
    'image.image_converter_page': 'feature_image_converter',
    'image.qr_generator': 'feature_image_qr',
}, 'image_dynamic_tools', 'feature_image')

# Finance
patch_hub('templates/hub_finance.html', {
    'finance.finance_calculator': 'feature_fin_emi', 
    # Just tying the single route to feature_fin_emi for now, it's just one html file that has Vue.js inside it. 
    # But wait, hub_finance doesn't have multiple tool-cards if the calculator is all-in-one. Let's ignore finance loop.
}, None, None)

