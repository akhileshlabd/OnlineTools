import os
import re

seo_data = {
    'index.html': {
        'title': 'Free Qube | Free Online PDF, Image & Video Utility Tools',
        'desc': 'Free Qube offers powerful, secure, and completely free online utility tools. Convert, merge, split PDFs, edit images, and process video completely offline-in-browser.',
        'keywords': 'free online tools, pdf tools, image converter, video to mp3, background remover, free qube, secure online utilities',
        'seo_html': '''<!-- SEO Content for AdSense Compliance -->
<div class="container bg-white p-4 p-md-5 rounded shadow-sm mt-5 mb-4 text-start">
    <h1 class="fw-bold mb-3 h2 text-center">Your Secure Hub for Free Online Utilities</h1>
    <p>Welcome to <strong>Free Qube</strong>, the ultimate collection of free, high-performance online tools designed to make your digital life easier. Whether you need to convert a Word document to a PDF, remove the background from a photograph, or extract an MP3 audio track from a video, we have built a streamlined tool to help you get the job done instantly.</p>
    
    <h2 class="fw-bold mt-4 h3">Privacy First: 100% Client-Side Processing</h2>
    <p>In an era of data breaches and intrusive tracking, we believe your files belong to you. Traditional online converters force you to upload your sensitive PDFs, private home videos, and confidential spreadsheets to their remote cloud servers. Not Free Qube.</p>
    <p>We leverage cutting-edge web technologies like WebAssembly, FFmpeg.wasm, and local Machine Learning models to process your files <strong>directly inside your web browser</strong>. This means your data never leaves your computer, ensuring enterprise-grade privacy and zero upload wait times. It is the security of desktop software combined with the convenience of a web app.</p>
    
    <h2 class="fw-bold mt-4 h3">No Subscriptions. No Watermarks.</h2>
    <p>We believe essential digital utilities should be accessible to everyone. Our entire suite of tools is provided completely free of charge. You will never be hit with unexpected paywalls, artificial daily limits, or annoying watermarks stamped onto your downloaded files. Just select your tool, process your file, and go.</p>
</div>'''
    },
    'hub_pdf.html': {
        'title': 'Free PDF Tools | Merge, Split, Convert & Lock PDFs - Free Qube',
        'desc': 'The ultimate collection of free online PDF tools. Merge, split, compress, unlock, and convert PDFs (Word to PDF, Excel to PDF) securely with no watermarks.',
        'keywords': 'free pdf tools, online pdf editor, merge pdf, split pdf, word to pdf, excel to pdf, secure pdf tools, free qube pdf',
        'seo_html': '''<!-- SEO Content for AdSense Compliance -->
<div class="container bg-white p-4 p-md-5 rounded shadow-sm mt-5 mb-4 text-start">
    <h2 class="fw-bold mb-3">Comprehensive & Secure PDF Tools</h2>
    <p>Working with PDF documents has never been easier. Whether you are a student compiling assignments, a legal professional managing contracts, or simply organizing your digital paperwork, Free Qube offers a massive suite of PDF tools to meet your exact needs.</p>
    
    <h3 class="fw-bold mt-4 h4">Convert, Merge, and Modify</h3>
    <p>Our platform allows you to seamlessly <strong>merge multiple PDF files</strong> into a single, cohesive document. Need to extract specific pages? Our <strong>PDF splitter</strong> helps you divide large documents in seconds. You can also securely unlock password-protected files, lock sensitive documents with AES encryption, or convert a collection of images, Word docs, and Excel sheets directly into standard PDF files.</p>
    
    <h3 class="fw-bold mt-4 h4">Why Our PDF Tools are Better</h3>
    <ul class="mb-0">
        <li><strong>Total Privacy:</strong> Every PDF tool on Free Qube runs locally in your browser. Your sensitive documents are never uploaded to any server.</li>
        <li><strong>Zero Limits:</strong> Process as many files as you want without daily caps.</li>
        <li><strong>No Watermarks:</strong> Export clean, professional PDFs ready for the boardroom or the classroom.</li>
    </ul>
</div>'''
    },
    'hub_image.html': {
        'title': 'Free Image Tools | Convert, Resize & Remove Backgrounds - Free Qube',
        'desc': 'Free online image utility tools. Remove image backgrounds using AI, convert WebP to JPG, compress photos, and resize images instantly in your browser.',
        'keywords': 'free image tools, image converter, background remover, ai background eraser, resize image online, webp to jpg, free qube image',
        'seo_html': '''<!-- SEO Content for AdSense Compliance -->
<div class="container bg-white p-4 p-md-5 rounded shadow-sm mt-5 mb-4 text-start">
    <h2 class="fw-bold mb-3">Professional Image Tools, Completely Free</h2>
    <p>Digital imagery is everywhere, but getting your photos into the right format, size, or layout can be frustrating. The Free Qube Image Hub is a powerful collection of online image utilities designed to handle everything from simple format conversions to advanced AI background removal.</p>
    
    <h3 class="fw-bold mt-4 h4">A Complete Suite of Photo Utilities</h3>
    <p>Need to create a transparent PNG for a graphic design project? Our <strong>AI Background Remover</strong> isolates your subject instantly. Struggling to upload a massive photo to a website? Our image resizer and compressor will shrink your file size while maintaining visual quality. We also offer lightning-fast format conversion, allowing you to convert stubborn WebP files into universally accepted JPGs or PNGs.</p>
    
    <h3 class="fw-bold mt-4 h4">Local Processing for Maximum Speed</h3>
    <p>Waiting for high-resolution images to upload to a cloud server is a waste of time. Our image tools utilize HTML5 Canvas and local WebAssembly processing. Your photos are edited instantly using your device's own hardware, which means blistering speeds, no file-size upload limits, and 100% privacy for your personal pictures.</p>
</div>'''
    }
}

def update_file(filepath, data):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath}, does not exist.")
        return
        
    with open(filepath, 'r') as f:
        content = f.read()

    content = re.sub(r'{% block title %}.*?{% endblock %}\n*', '', content, flags=re.DOTALL)
    content = re.sub(r'{% block meta_desc %}.*?{% endblock %}\n*', '', content, flags=re.DOTALL)
    content = re.sub(r'{% block meta_keywords %}.*?{% endblock %}\n*', '', content, flags=re.DOTALL)
    content = re.sub(r'<!-- SEO Content for AdSense Compliance -->.*?(?={% endblock %})', '', content, flags=re.DOTALL)
    
    blocks = f"""{{% block title %}}{data['title']}{{% endblock %}}
{{% block meta_desc %}}{data['desc']}{{% endblock %}}
{{% block meta_keywords %}}{data['keywords']}{{% endblock %}}
"""
    
    content = re.sub(r'({% extends "base.html" %}\n)', r'\1\n' + blocks + '\n', content)
    content = re.sub(r'({% endblock %}\s*)$', r'\n' + data['seo_html'] + r'\n\1', content)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Updated {filepath} successfully.")

for template, data in seo_data.items():
    update_file(f"templates/{template}", data)

