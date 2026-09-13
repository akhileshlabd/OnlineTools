import sys

with open('templates/video_tool.html', 'r') as f:
    content = f.read()

# 1. Remove the old Result Card entirely
import re
content = re.sub(r'<!-- Result Section -->.*?</div>.*?</div>', '', content, flags=re.DOTALL)

# 2. Re-arrange processCard to include inputs at the top and the download button at the bottom
new_process_card = """
    <!-- Processing Section -->
    <div class="card shadow-sm border-0 mb-4" id="processCard" style="display: none;">
        <div class="card-body p-4 p-md-5 text-center">
            
            {% if tool.id == 'trim' %}
            <div class="row g-3 justify-content-center mb-4 text-start">
                <div class="col-md-5">
                    <label class="form-label fw-bold">Start Time</label>
                    <input type="text" class="form-control input-live" id="trimStart" placeholder="00:00:00" value="00:00:00">
                </div>
                <div class="col-md-5">
                    <label class="form-label fw-bold">End Time</label>
                    <input type="text" class="form-control input-live" id="trimEnd" placeholder="00:00:10" value="00:00:10">
                </div>
            </div>
            {% endif %}
            {% if tool.id == 'thumbnail' %}
            <div class="row g-3 justify-content-center mb-4 text-start">
                <div class="col-md-6">
                    <label class="form-label fw-bold">Snapshot Time (Seconds)</label>
                    <input type="number" class="form-control input-live" id="thumbTime" placeholder="e.g. 5" value="1" min="0" step="0.1">
                </div>
            </div>
            {% endif %}

            <h4 class="fw-bold mb-3" id="processStatus">Initializing...</h4>
            
            <div class="progress mb-3" style="height: 25px;">
                <div id="progressBar" class="progress-bar progress-bar-striped progress-bar-animated bg-primary" role="progressbar" style="width: 0%;" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">0%</div>
            </div>
            <p class="text-muted small" id="processLog">Loading FFmpeg core...</p>

            <div class="mt-4">
                <a href="#" class="btn btn-success btn-lg rounded-pill px-5 fw-bold shadow-sm" id="downloadBtn" style="display: none;" download>
                    <i class="fas fa-download me-2"></i>Download Result
                </a>
                <button class="btn btn-outline-secondary btn-lg rounded-pill px-4 ms-2" id="startOverBtn" style="display: none;" onclick="window.location.reload()">
                    <i class="fas fa-redo me-1"></i> Start Over
                </button>
            </div>
        </div>
    </div>
"""

# Replace old processCard
content = re.sub(r'<!-- Processing Section -->.*?<div class="alert alert-info', new_process_card + '\n\n    <div class="alert alert-info', content, flags=re.DOTALL)

# 3. Modify JS logic
js_replacement = """
    const processCard = document.getElementById('processCard');
    
    const progressBar = document.getElementById('progressBar');
    const processStatus = document.getElementById('processStatus');
    const processLog = document.getElementById('processLog');
    const downloadBtn = document.getElementById('downloadBtn');
    const startOverBtn = document.getElementById('startOverBtn');

    let selectedFile = null;
    let ffmpeg = null;
    let isProcessing = false;
    let queuedRun = false;
    const { createFFmpeg, fetchFile } = FFmpeg;

    dropZone.addEventListener('click', () => fileInput.click());
    dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('bg-white'); });
    dropZone.addEventListener('dragleave', (e) => { e.preventDefault(); dropZone.classList.remove('bg-white'); });
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('bg-white');
        if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
    });
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length) handleFile(fileInput.files[0]);
    });

    const liveInputs = document.querySelectorAll('.input-live');
    liveInputs.forEach(input => {
        input.addEventListener('change', () => {
            triggerRun();
        });
    });

    function handleFile(file) {
        if (!file.type.startsWith('video/')) {
            Swal.fire('Error', 'Please select a valid video file.', 'error');
            return;
        }
        selectedFile = file;
        fileNameEl.textContent = file.name;
        fileSizeEl.textContent = (file.size / (1024 * 1024)).toFixed(2) + ' MB';
        fileInfo.style.display = 'block';
        
        uploadCard.style.display = 'none';
        processCard.style.display = 'block';
        startOverBtn.style.display = 'inline-block';
        
        triggerRun();
    }

    async function triggerRun() {
        if (!selectedFile) return;
        if (isProcessing) {
            queuedRun = true;
            return;
        }
        
        isProcessing = true;
        downloadBtn.style.display = 'none';
        progressBar.classList.add('progress-bar-animated');
        progressBar.classList.remove('bg-success');
        progressBar.classList.add('bg-primary');
        liveInputs.forEach(i => i.disabled = true);

        try {
            await runFFmpeg();
        } catch (error) {
            console.error(error);
            const errMsg = error && error.message ? error.message : error.toString();
            Swal.fire('Error', 'An error occurred during processing: ' + errMsg, 'error');
        } finally {
            isProcessing = false;
            liveInputs.forEach(i => i.disabled = false);
            if (queuedRun) {
                queuedRun = false;
                triggerRun();
            }
        }
    }

    async function runFFmpeg() {
"""

content = re.sub(r'const processCard = document.getElementById\(\'processCard\'\);.*?async function runFFmpeg\(\) \{', js_replacement, content, flags=re.DOTALL)

# 4. Remove resultCard transition at the end of runFFmpeg
cleanup_replacement = """
        // Cleanup virtual FS
        try {
            ffmpeg.FS('unlink', safeInputName);
            ffmpeg.FS('unlink', outputName);
        } catch(e) {}
        
        progressBar.classList.remove('progress-bar-animated');
        progressBar.classList.remove('bg-primary');
        progressBar.classList.add('bg-success');
        processStatus.textContent = 'Processing Complete!';
"""
content = re.sub(r'// Cleanup virtual FS.*?resultCard.style.display = \'block\';', cleanup_replacement, content, flags=re.DOTALL)

with open('templates/video_tool.html', 'w') as f:
    f.write(content)
