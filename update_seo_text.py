import os
import re

seo_data = {
    'word_to_pdf.html': {
        'title': 'Word to PDF Converter Free Online | No Watermark & Secure - Free Qube',
        'desc': 'Best free Word to PDF converter online. Convert DOCX to PDF instantly in your browser with zero data uploads. 100% secure, no watermarks, no registration needed.',
        'keywords': 'free word to pdf converter, word to pdf, docx to pdf, convert word to pdf free online, no watermark word to pdf, secure pdf converter, client-side docx to pdf',
        'seo_html': '''<!-- SEO Content for AdSense Compliance -->
<div class="container bg-white p-4 p-md-5 rounded shadow-sm mt-5 mb-4">
    <h2 class="fw-bold mb-3">Best Free Word to PDF Converter Online</h2>
    <p>Looking for a reliable, fast, and secure way to convert Microsoft Word documents to PDF? The <strong>Free Qube Word to PDF Converter</strong> is the ultimate solution for students, professionals, and businesses. With just one click, transform your DOCX files into universally accessible PDF formats without compromising on formatting, fonts, or layout.</p>
    
    <h3 class="fw-bold mt-4">Why Use Our DOCX to PDF Converter?</h3>
    <ul class="mb-4">
        <li><strong>100% Client-Side Privacy:</strong> Unlike other converters that upload your sensitive documents to remote cloud servers, our tool processes everything directly inside your web browser using WebAssembly. Your personal essays, legal contracts, and financial reports never leave your device.</li>
        <li><strong>No Watermarks:</strong> We believe free should mean free. We never stamp annoying watermarks or branding on your exported PDF files.</li>
        <li><strong>Lightning Fast:</strong> Because there are no upload or download queues to wait for, your file is converted instantly.</li>
        <li><strong>No Registration Required:</strong> Forget about signing up for accounts or handing over your email address. Just drag, drop, and download.</li>
    </ul>

    <h3 class="fw-bold mt-4">How to Convert Word to PDF Free</h3>
    <p>Converting a document is incredibly simple:</p>
    <ol>
        <li>Click the upload box or drag and drop your Microsoft Word (.docx) file into the designated area.</li>
        <li>Wait a fraction of a second while our secure Javascript engine parses your document.</li>
        <li>Your browser will instantly prompt you to download the perfectly formatted PDF file.</li>
    </ol>
    
    <h3 class="fw-bold mt-4">Frequently Asked Questions (FAQ)</h3>
    <p><strong>Is this Word to PDF converter truly free?</strong><br>Yes, it is completely free with no hidden limits or premium paywalls.</p>
    <p><strong>Are my files safe?</strong><br>Absolutely. Since the conversion happens locally on your computer's RAM, no one else ever sees or stores your files.</p>
    <p><strong>Does it work on Mac and Mobile?</strong><br>Yes, our browser-based tool is compatible with Windows, macOS, Linux, iOS, and Android.</p>
</div>'''
    },
    'excel_to_pdf.html': {
        'title': 'Excel to PDF Converter Free | Convert XLSX to PDF Securely - Free Qube',
        'desc': 'Easily convert Excel spreadsheets (XLSX) to PDF format for free. 100% private client-side processing, no watermarks, fast, and completely secure.',
        'keywords': 'excel to pdf, free excel to pdf converter, xlsx to pdf, spreadsheet to pdf, convert excel to pdf online free, no watermark excel to pdf',
        'seo_html': '''<!-- SEO Content for AdSense Compliance -->
<div class="container bg-white p-4 p-md-5 rounded shadow-sm mt-5 mb-4">
    <h2 class="fw-bold mb-3">Fast & Free Excel to PDF Converter</h2>
    <p>Sharing Excel spreadsheets can often lead to formatting errors, missing fonts, or accidental data modifications. Converting your <strong>Excel to PDF</strong> is the gold standard for preserving your data's layout, ensuring it looks exactly the same on every device. Our free online Excel to PDF converter makes it effortless to lock in your spreadsheets, financial models, and data reports.</p>
    
    <h3 class="fw-bold mt-4">Key Features of Our XLSX to PDF Tool</h3>
    <ul class="mb-4">
        <li><strong>Zero Data Uploads:</strong> Financial data is highly sensitive. Our tool utilizes local browser processing, meaning your Excel sheets are parsed and converted locally. Your data is never transmitted to an external server, guaranteeing absolute confidentiality.</li>
        <li><strong>Maintains Formatting:</strong> Cell widths, background colors, and typography are precisely rendered into a clean, professional PDF table.</li>
        <li><strong>Completely Free, No Watermarks:</strong> Export clean, unbranded PDFs ready for professional distribution. No premium upgrades required.</li>
        <li><strong>Instant Processing:</strong> Skip the slow upload speeds of traditional cloud converters. Your PDF is generated in milliseconds.</li>
    </ul>

    <h3 class="fw-bold mt-4">How to Convert Excel Files to PDF</h3>
    <ol>
        <li>Upload your .xlsx file by clicking the upload area or dragging and dropping the file.</li>
        <li>The local engine immediately reads your spreadsheet data.</li>
        <li>Click download to save your secure, read-only PDF document to your device.</li>
    </ol>
</div>'''
    },
    'image_to_pdf.html': {
        'title': 'Image to PDF Converter Free | JPG & PNG to PDF - Free Qube',
        'desc': 'Convert JPG, PNG, and GIF images to PDF format instantly. Free online image to PDF converter with offline-grade privacy and zero watermarks.',
        'keywords': 'image to pdf, free image to pdf converter, jpg to pdf, png to pdf, convert pictures to pdf, photos to pdf free, merge images to pdf',
        'seo_html': '''<!-- SEO Content for AdSense Compliance -->
<div class="container bg-white p-4 p-md-5 rounded shadow-sm mt-5 mb-4">
    <h2 class="fw-bold mb-3">Convert Images to PDF Free Online</h2>
    <p>Whether you need to compile a portfolio, organize scanned receipts, or share a photo album, our <strong>Image to PDF converter</strong> is the easiest way to combine multiple pictures into a single, easily shareable PDF document. We support all major image formats including JPG, PNG, and GIF.</p>
    
    <h3 class="fw-bold mt-4">The Safest JPG to PDF Tool</h3>
    <p>Privacy is our top priority. When you use our tool to convert photos to PDF, the entire rendering process takes place on your own device. We never upload your personal photos, ID cards, or sensitive documents to the cloud. You get enterprise-grade security without paying a dime.</p>

    <h3 class="fw-bold mt-4">Benefits of Converting Pictures to PDF</h3>
    <ul class="mb-4">
        <li><strong>Easy Sharing:</strong> Instead of sending 20 separate image attachments via email, combine them into one neat PDF file.</li>
        <li><strong>Universal Compatibility:</strong> PDFs can be opened on any operating system, smartphone, or tablet without special image viewing software.</li>
        <li><strong>High Quality:</strong> Our conversion engine preserves the original resolution and clarity of your images, ensuring crisp, professional results.</li>
        <li><strong>No File Size Limits:</strong> Because there are no server uploads, you aren't restricted by arbitrary network limits.</li>
    </ul>
    
    <h3 class="fw-bold mt-4">How to Change an Image to PDF</h3>
    <p>Simply select your image files from your computer or smartphone, adjust the ordering if necessary, and click the convert button. Your unified PDF will be generated instantly for download.</p>
</div>'''
    },
    'pdf_merger.html': {
        'title': 'Merge PDF Files Free Online | Combine PDFs Securely - Free Qube',
        'desc': 'Merge multiple PDF files into one document for free. The fastest, most secure online PDF combiner. No uploads, no watermarks, unlimited merging.',
        'keywords': 'merge pdf, combine pdf files, free pdf merger, join pdf online, merge pdf free, no watermark pdf merger, secure pdf combiner',
        'seo_html': '''<!-- SEO Content for AdSense Compliance -->
<div class="container bg-white p-4 p-md-5 rounded shadow-sm mt-5 mb-4">
    <h2 class="fw-bold mb-3">Best Free PDF Merger Online</h2>
    <p>Managing multiple PDF documents can be a hassle. Our <strong>Free PDF Merger</strong> lets you easily combine multiple PDFs into one single document. Whether you are compiling legal case files, merging monthly reports, or putting together a research paper, our tool streamlines the process seamlessly.</p>
    
    <h3 class="fw-bold mt-4">Why Choose Our PDF Combiner?</h3>
    <ul class="mb-4">
        <li><strong>Offline-Level Security:</strong> We use advanced client-side JavaScript (pdf-lib) to merge your files directly in your browser's memory. Your PDFs are never uploaded to any server, guaranteeing 100% privacy.</li>
        <li><strong>Drag & Drop Reordering:</strong> Easily rearrange the order of your files before merging. Just drag the file cards into the perfect sequence.</li>
        <li><strong>100% Free & Unlimited:</strong> Combine as many files as you want, as many times as you want. There are no daily limits and no watermarks added to your final document.</li>
        <li><strong>Blazing Fast:</strong> Forget about slow upload bars. Because the merging happens on your local device CPU, it finishes almost instantly.</li>
    </ul>

    <h3 class="fw-bold mt-4">How to Combine PDF Files</h3>
    <ol>
        <li>Click "Add More PDFs" or drag and drop all the files you want to merge into the drop zone.</li>
        <li>Rearrange the files in the list until they are in the correct order.</li>
        <li>Click "Merge PDFs" and your browser will instantly generate and download the combined document.</li>
    </ol>
</div>'''
    },
    'pdf_split.html': {
        'title': 'Split PDF Free Online | Extract PDF Pages Securely - Free Qube',
        'desc': 'Easily split PDF files and extract specific pages for free. 100% private client-side processing. Cut, divide, and separate PDFs instantly with no watermarks.',
        'keywords': 'split pdf, extract pdf pages, free pdf splitter, cut pdf online, separate pdf pages, divide pdf, secure pdf splitter',
        'seo_html': '''<!-- SEO Content for AdSense Compliance -->
<div class="container bg-white p-4 p-md-5 rounded shadow-sm mt-5 mb-4">
    <h2 class="fw-bold mb-3">Split PDF Files and Extract Pages for Free</h2>
    <p>Have a massive PDF document but only need a few specific pages? Our <strong>Free PDF Splitter</strong> is the perfect tool for extracting exactly what you need. Easily divide, cut, and separate PDF pages into a new, lightweight document without downloading any expensive software.</p>
    
    <h3 class="fw-bold mt-4">The Safest Way to Cut PDFs</h3>
    <p>Most online PDF splitters require you to upload your entire document to their servers, exposing your private information. We do things differently. By utilizing powerful in-browser processing, your PDF is analyzed and split entirely on your local machine. <strong>Zero data uploads mean zero privacy risks.</strong></p>

    <h3 class="fw-bold mt-4">Features of Our PDF Extractor</h3>
    <ul class="mb-4">
        <li><strong>Custom Page Ranges:</strong> Extract a single page (e.g., "5"), a range of pages (e.g., "1-3"), or a combination (e.g., "1, 4-6, 9").</li>
        <li><strong>No Quality Loss:</strong> Your extracted pages retain their exact original quality, formatting, and text.</li>
        <li><strong>No Watermarks:</strong> Your new split PDF is completely clean and ready for professional use.</li>
        <li><strong>Instant Download:</strong> Processing happens in milliseconds directly in your browser.</li>
    </ul>
    
    <h3 class="fw-bold mt-4">How to Split a PDF</h3>
    <p>Simply upload your PDF, type in the page numbers or ranges you wish to keep in the input box, and hit extract. A new PDF containing only those pages will immediately download to your device.</p>
</div>'''
    }
}

def update_file(filepath, data):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath}, does not exist.")
        return
        
    with open(filepath, 'r') as f:
        content = f.read()

    # Remove existing blocks if they exist so we can neatly prepend them
    content = re.sub(r'{% block title %}.*?{% endblock %}\n*', '', content, flags=re.DOTALL)
    content = re.sub(r'{% block meta_desc %}.*?{% endblock %}\n*', '', content, flags=re.DOTALL)
    content = re.sub(r'{% block meta_keywords %}.*?{% endblock %}\n*', '', content, flags=re.DOTALL)
    
    # Remove existing SEO div
    content = re.sub(r'<!-- SEO Content for AdSense Compliance -->.*?(?={% endblock %})', '', content, flags=re.DOTALL)
    
    # Construct new head blocks
    blocks = f"""{{% block title %}}{data['title']}{{% endblock %}}
{{% block meta_desc %}}{data['desc']}{{% endblock %}}
{{% block meta_keywords %}}{data['keywords']}{{% endblock %}}
"""
    
    # Insert head blocks right after extends
    content = re.sub(r'({% extends "base.html" %}\n)', r'\1\n' + blocks + '\n', content)
    
    # Insert new SEO div right before the final endblock
    content = re.sub(r'({% endblock %}\s*)$', r'\n' + data['seo_html'] + r'\n\1', content)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Updated {filepath} successfully.")

for template, data in seo_data.items():
    update_file(f"templates/{template}", data)

