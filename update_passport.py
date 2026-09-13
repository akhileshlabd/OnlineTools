import re

with open('templates/passport_maker.html', 'r') as f:
    content = f.read()

# 1. Update UI Output Format block
old_ui = """                    <div class="mb-4">
                        <label class="form-label fw-bold"><i class="fas fa-print text-primary me-2"></i>Output Format</label>
                        <select class="form-select shadow-sm" disabled>
                            <option>4x6" Photo Print (2x3 Grid)</option>
                        </select>
                        <small class="text-muted mt-2 d-block">Generates a standard 4x6 inch printable sheet at 300 DPI containing exactly six 2x2 inch passport photos with cut lines.</small>
                    </div>

                    <div class="d-grid gap-2 mt-5">
                        <a href="#" id="downloadBtn" class="btn btn-primary btn-lg rounded-pill fw-bold shadow-sm" download>
                            <i class="fas fa-download me-2"></i>Download 4x6" Sheet
                        </a>"""

new_ui = """                    <div class="mb-4">
                        <label class="form-label fw-bold"><i class="fas fa-print text-primary me-2"></i>Output Format</label>
                        <select class="form-select shadow-sm" id="outputFormat">
                            <option value="single">Single Digital Photo (600x600 px)</option>
                            <option value="grid">4x6" Printable Sheet (2x3 Grid)</option>
                        </select>
                        <small class="text-muted mt-2 d-block" id="formatHelperText">Generates a standard 2x2 inch digital photo for online applications.</small>
                    </div>

                    <div class="d-grid gap-2 mt-5">
                        <a href="#" id="downloadBtn" class="btn btn-primary btn-lg rounded-pill fw-bold shadow-sm" download>
                            <i class="fas fa-download me-2"></i><span id="downloadBtnText">Download Single Photo</span>
                        </a>"""
content = content.replace(old_ui, new_ui)

# 2. Update Preview Canvas Header
content = content.replace('<h6 class="fw-bold text-muted mb-3">Printable 4x6" Sheet Preview</h6>', '<h6 class="fw-bold text-muted mb-3" id="previewTitle">Photo Preview</h6>')

# 3. Update the Javascript logic inside updateCanvas()
old_js = """        // Printable 4x6" Sheet (1200x1800 px @ 300 DPI)
        previewCanvas.width = 1200;
        previewCanvas.height = 1800;
        const ctx = previewCanvas.getContext('2d');
        
        // Fill white base
        ctx.fillStyle = '#FFFFFF';
        ctx.fillRect(0, 0, 1200, 1800);

        // Draw 2x3 Grid with crop marks
        for(let row = 0; row < 3; row++) {
            for(let col = 0; col < 2; col++) {
                const x = col * 600;
                const y = row * 600;
                
                ctx.drawImage(photoCanvas, x, y, 600, 600);
                
                // Crop marks
                ctx.strokeStyle = '#CCCCCC';
                ctx.setLineDash([5, 5]);
                ctx.lineWidth = 2;
                ctx.strokeRect(x, y, 600, 600);
            }
        }
        
        // Update Download Link
        downloadBtn.href = previewCanvas.toDataURL('image/jpeg', 1.0);
        downloadBtn.download = `passport_sheet_4x6_${Date.now()}.jpg`;"""

new_js = """        const format = document.getElementById('outputFormat').value;
        const ctx = previewCanvas.getContext('2d');

        if (format === 'single') {
            previewCanvas.width = 600;
            previewCanvas.height = 600;
            ctx.drawImage(photoCanvas, 0, 0);
            
            downloadBtn.href = previewCanvas.toDataURL('image/jpeg', 1.0);
            downloadBtn.download = `passport_photo_single_${Date.now()}.jpg`;
            document.getElementById('downloadBtnText').textContent = 'Download Single Photo';
            document.getElementById('previewTitle').textContent = 'Single Digital Photo Preview';
            document.getElementById('formatHelperText').textContent = 'Generates a standard 2x2 inch (600x600 px) digital photo perfectly sized for online applications and forms.';
        } else {
            // Printable 4x6" Sheet (1200x1800 px @ 300 DPI)
            previewCanvas.width = 1200;
            previewCanvas.height = 1800;
            
            // Fill white base
            ctx.fillStyle = '#FFFFFF';
            ctx.fillRect(0, 0, 1200, 1800);

            // Draw 2x3 Grid with crop marks
            for(let row = 0; row < 3; row++) {
                for(let col = 0; col < 2; col++) {
                    const x = col * 600;
                    const y = row * 600;
                    
                    ctx.drawImage(photoCanvas, x, y, 600, 600);
                    
                    // Crop marks
                    ctx.strokeStyle = '#CCCCCC';
                    ctx.setLineDash([5, 5]);
                    ctx.lineWidth = 2;
                    ctx.strokeRect(x, y, 600, 600);
                }
            }
            
            downloadBtn.href = previewCanvas.toDataURL('image/jpeg', 1.0);
            downloadBtn.download = `passport_sheet_4x6_${Date.now()}.jpg`;
            document.getElementById('downloadBtnText').textContent = 'Download 4x6" Sheet';
            document.getElementById('previewTitle').textContent = 'Printable 4x6" Sheet Preview';
            document.getElementById('formatHelperText').textContent = 'Generates a standard 4x6 inch printable sheet at 300 DPI containing exactly six 2x2 inch passport photos with cut lines.';
        }"""
content = content.replace(old_js, new_js)

# 4. Add the event listener for the dropdown
old_listener = """    // Instantly reactive background color
    bgColorPicker.addEventListener('input', () => {
        updateCanvas();
    });"""

new_listener = """    // Instantly reactive UI
    bgColorPicker.addEventListener('input', () => updateCanvas());
    document.getElementById('outputFormat').addEventListener('change', () => updateCanvas());"""
content = content.replace(old_listener, new_listener)

with open('templates/passport_maker.html', 'w') as f:
    f.write(content)

