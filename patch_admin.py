with open('routes/admin.py', 'r') as f:
    content = f.read()

# Replace the AVAILABLE_FEATURES block
new_features = """
FEATURE_GROUPS = [
    {
        "key": "feature_nav_pdf",
        "label": "PDF Tools",
        "icon": "fa-file-pdf",
        "children": [
            {"key": "feature_pdf_merger", "label": "PDF Merger"},
            {"key": "feature_pdf_splitter", "label": "PDF Splitter"},
            {"key": "feature_pdf_word_to_pdf", "label": "Word to PDF"},
            {"key": "feature_pdf_excel_to_pdf", "label": "Excel to PDF"},
            {"key": "feature_pdf_image_to_pdf", "label": "Image to PDF"},
            {"key": "feature_pdf_lock", "label": "Lock PDF"},
            {"key": "feature_pdf_unlock", "label": "Unlock PDF"},
            {"key": "feature_pdf_dynamic", "label": "Dynamic Tools (Rotate, Remove, Watermark)"},
        ]
    },
    {
        "key": "feature_nav_image",
        "label": "Image Tools",
        "icon": "fa-image",
        "children": [
            {"key": "feature_image_resizer", "label": "Image Resizer"},
            {"key": "feature_image_converter", "label": "Image Converter"},
            {"key": "feature_image_qr", "label": "QR Generator"},
            {"key": "feature_image_dynamic", "label": "Dynamic Tools (Passport, BG Remove, Blur, Flip)"},
        ]
    },
    {
        "key": "feature_nav_games",
        "label": "Free Games",
        "icon": "fa-gamepad",
        "children": [
            {"key": "feature_game_sudoku-game", "label": "Sudoku"},
            {"key": "feature_game_tetris-game", "label": "Tetris"},
            {"key": "feature_game_brick-breaker", "label": "Brick Breaker"},
            {"key": "feature_game_snake-game", "label": "Snake"},
            {"key": "feature_game_neon-qube", "label": "Neon Qube"},
        ]
    },
    {
        "key": "feature_nav_finance",
        "label": "Finance Tools",
        "icon": "fa-calculator",
        "children": [
            {"key": "feature_fin_emi", "label": "EMI Calculator"},
            {"key": "feature_fin_sip", "label": "SIP Calculator"},
            {"key": "feature_fin_fd", "label": "FD Calculator"},
        ]
    },
    {
        "key": "feature_nav_health",
        "label": "Health Tools",
        "icon": "fa-heartbeat",
        "children": [
            {"key": "feature_health_bmi", "label": "BMI Calculator"},
            {"key": "feature_health_macro", "label": "Macro Calculator"},
        ]
    },
    {
        "key": "feature_nav_text",
        "label": "Text Tools",
        "icon": "fa-font",
        "children": [
            {"key": "feature_text_counter", "label": "Word Counter"},
            {"key": "feature_text_case", "label": "Case Converter"},
            {"key": "feature_text_tts", "label": "Text to Speech"},
        ]
    },
    {
        "key": "feature_nav_network",
        "label": "Network Tools",
        "icon": "fa-network-wired",
        "children": [
            {"key": "feature_net_ip", "label": "My IP Address"},
            {"key": "feature_net_ping", "label": "Ping Tester"},
        ]
    },
    {
        "key": "feature_nav_dev",
        "label": "Code & Dev Tools",
        "icon": "fa-code",
        "children": [
            {"key": "feature_dev_json", "label": "JSON Formatter"},
            {"key": "feature_dev_b64", "label": "Base64 Encode/Decode"},
        ]
    },
    {
        "key": "feature_nav_video",
        "label": "Video Tools",
        "icon": "fa-video",
        "children": [
            {"key": "feature_vid_mp3", "label": "Video to MP3"}
        ]
    },
    {
        "key": "feature_nav_kids",
        "label": "Kids Zone",
        "icon": "fa-child",
        "children": [
            {"key": "feature_kids_tracing", "label": "Letter Tracing"}
        ]
    },
    {
        "key": "feature_nav_compare",
        "label": "Compare Phones",
        "icon": "fa-mobile-alt",
        "children": []
    }
]
"""

import re
content = re.sub(r'AVAILABLE_FEATURES = \[.*?\]\n', new_features, content, flags=re.DOTALL)

# Now fix the dashboard() function to use FEATURE_GROUPS
dashboard_logic_old = """    features_list = []
    for f in AVAILABLE_FEATURES:
        f_copy = dict(f)
        f_copy['is_enabled'] = feature_dict.get(f['key'], True)
        features_list.append(f_copy)
        
    # Group features by category
    features_grouped = {}
    for f in features_list:
        features_grouped.setdefault(f['category'], []).append(f)"""

dashboard_logic_new = """    features_grouped = []
    for group in FEATURE_GROUPS:
        grp = dict(group)
        grp['is_enabled'] = feature_dict.get(grp['key'], True)
        grp_children = []
        for child in grp.get('children', []):
            c = dict(child)
            c['is_enabled'] = feature_dict.get(c['key'], True)
            grp_children.append(c)
        grp['children'] = grp_children
        features_grouped.append(grp)"""

content = content.replace(dashboard_logic_old, dashboard_logic_new)

with open('routes/admin.py', 'w') as f:
    f.write(content)

