import os
import re

seo_data = {
    'lock_pdf.html': {
        'title': 'Lock PDF Free Online | Protect PDF with Password Securely',
        'desc': 'Secure your PDF document with a strong password for free. 100% offline-level security. Encrypt your private PDF files locally so no one can access them.',
        'keywords': 'lock pdf, password protect pdf, secure pdf, encrypt pdf online, free pdf locker, add password to pdf, protect pdf document',
        'seo_html': '''<!-- SEO Content for AdSense Compliance -->
<div class="container bg-white p-4 p-md-5 rounded shadow-sm mt-5 mb-4">
    <h2 class="fw-bold mb-3">Password Protect & Lock PDFs Free Online</h2>
    <p>Sharing sensitive documents like financial statements, legal contracts, or medical records requires top-tier security. Our <strong>Free PDF Locker</strong> empowers you to easily encrypt your PDF files with a strong password. Once locked, only individuals with the exact password will be able to open, view, or edit your document.</p>
    
    <h3 class="fw-bold mt-4">Bank-Grade Encryption with Zero Uploads</h3>
    <p>Unlike traditional online PDF tools that force you to upload your sensitive files to their cloud servers, our PDF Locker operates entirely on your device. We utilize advanced client-side processing to apply AES encryption locally. Your document and your password never leave your computer, ensuring absolute confidentiality.</p>

    <h3 class="fw-bold mt-4">How to Lock a PDF File</h3>
    <ol class="mb-4">
        <li>Click the upload box to select your unencrypted PDF file.</li>
        <li>Type a strong password into the input field. (Remember this, as it cannot be recovered!)</li>
        <li>Click the "Lock PDF" button to instantly generate your encrypted, secure file.</li>
    </ol>
</div>'''
    },
    'unlock_pdf.html': {
        'title': 'Unlock PDF Free Online | Remove PDF Passwords Instantly',
        'desc': 'Remove password protection from your PDF files for free. Fast, secure, and completely private client-side PDF password remover.',
        'keywords': 'unlock pdf, remove pdf password, free pdf unlocker, decrypt pdf, pdf password remover, unlock protected pdf',
        'seo_html': '''<!-- SEO Content for AdSense Compliance -->
<div class="container bg-white p-4 p-md-5 rounded shadow-sm mt-5 mb-4">
    <h2 class="fw-bold mb-3">Unlock PDF Files Free Online</h2>
    <p>If you have received a secure PDF document but are tired of typing the password every time you want to read it, our <strong>Free PDF Unlocker</strong> is the perfect solution. As long as you know the document's password, you can permanently strip the encryption layer, saving it as a standard, accessible PDF file.</p>
    
    <h3 class="fw-bold mt-4">100% Private Client-Side Decryption</h3>
    <p>Removing passwords from PDFs online often involves massive security risks, as it requires uploading sensitive documents to foreign servers. We solve this by bringing the decryption engine to your browser. Your password and your decrypted PDF remain strictly on your local device, ensuring complete privacy.</p>

    <h3 class="fw-bold mt-4">How to Remove a PDF Password</h3>
    <ol class="mb-4">
        <li>Upload your locked PDF document to the tool above.</li>
        <li>Enter the current password required to open the file.</li>
        <li>Click "Unlock PDF" to permanently remove the encryption and download the unprotected file.</li>
    </ol>
</div>'''
    },
    'bg_remover.html': {
        'title': 'Remove Background from Image Free | AI Background Eraser',
        'desc': 'Automatically remove backgrounds from images for free using advanced AI. Create transparent PNGs instantly with no watermark and 100% local privacy.',
        'keywords': 'remove background, free background remover, ai background eraser, transparent background maker, remove bg, photo background editor',
        'seo_html': '''<!-- SEO Content for AdSense Compliance -->
<div class="container bg-white p-4 p-md-5 rounded shadow-sm mt-5 mb-4">
    <h2 class="fw-bold mb-3">Remove Backgrounds from Images Automatically for Free</h2>
    <p>Whether you are designing e-commerce product photos, creating YouTube thumbnails, or putting together professional presentations, having images with transparent backgrounds is crucial. Our <strong>Free AI Background Remover</strong> allows you to instantly isolate the main subject of your photo and erase the backdrop with a single click.</p>
    
    <h3 class="fw-bold mt-4">Unmatched Privacy: Local AI Processing</h3>
    <p>Most background removal tools charge exorbitant fees or force you to upload your personal photos to their AI cloud servers. Free Qube utilizes powerful client-side AI processing (using ONNX Runtime and WebAssembly) to run the machine learning models directly on your device CPU/GPU. Your photos are never uploaded, keeping your data entirely private.</p>

    <h3 class="fw-bold mt-4">Benefits of Our Background Eraser</h3>
    <ul class="mb-4">
        <li><strong>Completely Free:</strong> No subscriptions, no credits, and no premium paywalls.</li>
        <li><strong>No Watermarks:</strong> Export high-quality transparent PNGs without any branding.</li>
        <li><strong>Automated Precision:</strong> Our advanced AI automatically detects people, animals, and objects, cutting them out perfectly.</li>
    </ul>
    
    <h3 class="fw-bold mt-4">How to Make a Background Transparent</h3>
    <p>Just upload your JPG or PNG image. Our local AI will analyze the photo, separate the foreground from the background, and instantly provide you with a clean, transparent image ready to download.</p>
</div>'''
    },
    'image_converter.html': {
        'title': 'Image Converter Free Online | Convert WebP, JPG, PNG',
        'desc': 'Convert images between JPG, PNG, WebP, and GIF formats for free online. 100% client-side privacy, lightning fast, and no watermarks.',
        'keywords': 'image converter, convert webp to jpg, png to jpg, free photo converter, convert image format, online image converter',
        'seo_html': '''<!-- SEO Content for AdSense Compliance -->
<div class="container bg-white p-4 p-md-5 rounded shadow-sm mt-5 mb-4">
    <h2 class="fw-bold mb-3">Fast & Free Image Format Converter</h2>
    <p>In the modern web ecosystem, managing different image formats can be a headache. Whether you need to convert a modern WebP image into a universally compatible JPG, or transform a flat photo into a transparent PNG, our <strong>Free Image Converter</strong> handles it all instantly.</p>
    
    <h3 class="fw-bold mt-4">Supported Formats</h3>
    <ul class="mb-4">
        <li><strong>WebP to JPG / PNG:</strong> WebP images are great for websites but often fail to open in legacy software. Easily convert them back to standard formats.</li>
        <li><strong>PNG to JPG:</strong> Compress massive transparent images into lightweight JPGs perfect for sharing.</li>
        <li><strong>JPG to PNG:</strong> Convert photographs into formats that support transparency and lossless editing.</li>
    </ul>

    <h3 class="fw-bold mt-4">The Advantage of Client-Side Conversion</h3>
    <p>When you use Free Qube to convert your images, you never have to wait for your files to upload to a remote server. The conversion takes place locally via your browser's internal canvas API. This guarantees 100% privacy, immediate processing speeds, and no restrictive file size limits.</p>
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

