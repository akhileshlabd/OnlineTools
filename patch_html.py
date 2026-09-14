import re

def patch_base():
    with open('templates/base.html', 'r') as f:
        content = f.read()

    mappings = [
        ('pdf_hub', 'feature_nav_pdf'),
        ('image_hub', 'feature_nav_image'),
        ('finance_hub', 'feature_nav_finance'),
        ('text_hub', 'feature_nav_text'),
        ('health_hub', 'feature_nav_health'),
        ('math_hub', 'feature_nav_math'),
        ('network_hub', 'feature_nav_network'),
        ('code_hub', 'feature_nav_dev'),
        ('video_hub', 'feature_nav_video'),
        ('games_hub', 'feature_nav_games'),
        ('kids_hub', 'feature_nav_kids'),
    ]
    
    for route, feature in mappings:
        pattern = r'(<li class="nav-item">[^<]*<a[^>]*href="\{\{\s*url_for\(' + f"'{route.split('_')[0]}.{route}'" + r'\)\s*\}\}"[^>]*>.*?</li>)'
        
        # We need to wrap it using re.sub
        def replacer(match):
            original = match.group(1)
            if '{% if features' in original: return original # already patched
            return f"{{% if features['{feature}'] %}}\n{original}\n{{% endif %}}"
            
        content = re.sub(pattern, replacer, content, flags=re.DOTALL)
        
    # Also patch compare_phones link if present in base
    content = re.sub(r'(<li class="nav-item">[^<]*<a[^>]*href="\{\{\s*url_for\(\'mobiles.compare_phones\'\)\s*\}\}"[^>]*>.*?</li>)',
                     r"{% if features['feature_nav_compare'] %}\n\1\n{% endif %}", content, flags=re.DOTALL)

    with open('templates/base.html', 'w') as f:
        f.write(content)


def patch_index():
    with open('templates/index.html', 'r') as f:
        content = f.read()

    mappings = [
        ('pdf.pdf_hub', 'feature_nav_pdf'),
        ('image.image_hub', 'feature_nav_image'),
        ('finance.finance_hub', 'feature_nav_finance'),
        ('text.text_hub', 'feature_nav_text'),
        ('health.health_hub', 'feature_nav_health'),
        ('math.math_hub', 'feature_nav_math'),
        ('network.network_hub', 'feature_nav_network'),
        ('code.code_hub', 'feature_nav_dev'),
        ('video.video_hub', 'feature_nav_video'),
        ('games.games_hub', 'feature_nav_games'),
        ('kids.kids_hub', 'feature_nav_kids'),
        ('mobiles.compare_phones', 'feature_nav_compare'),
    ]
    
    for route, feature in mappings:
        pattern = r'(<div class="col-md-6 col-lg-4 d-flex">\s*<a href="\{\{\s*url_for\(' + f"'{route}'" + r'\)\s*\}\}".*?</a>\s*</div>)'
        
        def replacer(match):
            original = match.group(1)
            if '{% if features' in original: return original
            return f"{{% if features['{feature}'] %}}\n{original}\n{{% endif %}}"
            
        content = re.sub(pattern, replacer, content, flags=re.DOTALL)

    with open('templates/index.html', 'w') as f:
        f.write(content)


def patch_games():
    with open('templates/hub_games.html', 'r') as f:
        content = f.read()
        
    pattern = r'({% for key, tool in games_tools.items() %}\s*)(<div class="col-md-6 col-lg-4 d-flex">.*?</div>)(\s*{% endfor %})'
    
    def replacer(match):
        pre = match.group(1)
        inner = match.group(2)
        post = match.group(3)
        if '{% if features' in inner: return match.group(0)
        
        new_inner = f"{{% if features['feature_game_' ~ tool.id] %}}\n{inner}\n{{% endif %}}"
        return pre + new_inner + post
        
    content = re.sub(pattern, replacer, content, flags=re.DOTALL)
    
    with open('templates/hub_games.html', 'w') as f:
        f.write(content)

patch_base()
patch_index()
patch_games()
print("HTML templates patched!")
