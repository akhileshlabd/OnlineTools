import re

with open('routes/admin.py', 'r') as f:
    content = f.read()

# Replace the dynamic placeholders with the actual granular keys
replacements = {
    '{"key": "feature_pdf_dynamic", "label": "Dynamic Tools (Rotate, Remove, Watermark)"}': 
    '{"key": "feature_pdf_rotate_pdf", "label": "Rotate PDF"},\n            {"key": "feature_pdf_remove_page", "label": "Remove Page"},\n            {"key": "feature_pdf_add_blank", "label": "Add Blank Page"},\n            {"key": "feature_pdf_watermark", "label": "Add Watermark"}',
    
    '{"key": "feature_image_dynamic", "label": "Dynamic Tools (Passport, BG Remove, Blur, Flip)"}':
    '{"key": "feature_image_passport_maker", "label": "Passport Maker"},\n            {"key": "feature_image_bg_remover", "label": "Background Remover"},\n            {"key": "feature_image_grayscale", "label": "Grayscale Image"},\n            {"key": "feature_image_blur", "label": "Blur Image"},\n            {"key": "feature_image_flip_h", "label": "Flip Horizontal"},\n            {"key": "feature_image_flip_v", "label": "Flip Vertical"},\n            {"key": "feature_image_rotate_tool", "label": "Rotate Image"},\n            {"key": "feature_image_brightness", "label": "Adjust Brightness"},\n            {"key": "feature_image_contrast", "label": "Adjust Contrast"}'
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open('routes/admin.py', 'w') as f:
    f.write(content)
