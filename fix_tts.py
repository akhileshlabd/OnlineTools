import re

with open('templates/tts_converter.html', 'r') as f:
    content = f.read()

# 1. Fix the Preview Garbage Collection Bug
old_preview_listener = """        btnPreview.addEventListener('click', () => {
            const utterance = createUtterance();
            if (!utterance) return;
            
            window.speechSynthesis.cancel(); // Stop anything playing
            
            btnPreview.style.display = 'none';
            btnStop.style.display = 'inline-block';
            
            utterance.onend = () => {
                btnPreview.style.display = 'inline-block';
                btnStop.style.display = 'none';
            };
            
            window.speechSynthesis.speak(utterance);
        });"""

new_preview_listener = """        // Prevent Garbage Collection of Utterance (Chrome Bug Fix)
        window.currentUtterance = null;
        
        btnPreview.addEventListener('click', () => {
            window.currentUtterance = createUtterance();
            if (!window.currentUtterance) return;
            
            window.speechSynthesis.cancel(); // Stop anything playing
            
            btnPreview.style.display = 'none';
            btnStop.style.display = 'inline-block';
            
            window.currentUtterance.onend = () => {
                btnPreview.style.display = 'inline-block';
                btnStop.style.display = 'none';
            };
            
            // Fallback timeout in case onend never fires
            const estTime = (ttsInput.value.length / 10) * 1000;
            setTimeout(() => {
                btnPreview.style.display = 'inline-block';
                btnStop.style.display = 'none';
            }, estTime + 2000);
            
            window.speechSynthesis.speak(window.currentUtterance);
        });"""

content = content.replace(old_preview_listener, new_preview_listener)

# 2. Replace the Capture Download with a Standard Form Download
old_download_btn = """                <button id="btnDownload" class="btn btn-success btn-lg rounded-pill fw-bold px-4 shadow-sm flex-grow-1">
                    <i class="fas fa-download me-2"></i> Capture & Download Audio
                </button>"""

new_download_btn = """                <form id="downloadForm" action="/text/api/tts-download" method="POST" class="flex-grow-1 d-flex">
                    <input type="hidden" name="text" id="downloadTextInput">
                    <button type="submit" id="btnDownload" class="btn btn-success btn-lg rounded-pill fw-bold px-4 shadow-sm w-100">
                        <i class="fas fa-download me-2"></i> Download MP3
                    </button>
                </form>"""

content = content.replace(old_download_btn, new_download_btn)

# 3. Update Download Event Listener (Remove all WebRTC logic)
old_webrtc_logic = """        // 4. Capture & Download Engine (Using MediaRecorder)
        btnDownload.addEventListener('click', async () => {
            const utterance = createUtterance();
            if (!utterance) return;
            
            if (!('getDisplayMedia' in navigator.mediaDevices)) {
                Swal.fire('Unsupported Browser', 'Your browser does not support audio capture. Please use the Preview button or upgrade your browser.', 'error');
                return;
            }

            Swal.fire({
                title: 'Capture Audio',
                text: 'To download the audio securely without a server, we must record the tab. When prompted, select "This Tab" and make sure "Share audio" is toggled ON.',
                icon: 'info',
                showCancelButton: true,
                confirmButtonText: 'Start Capture'
            }).then(async (result) => {
                if (result.isConfirmed) {
                    try {
                        const stream = await navigator.mediaDevices.getDisplayMedia({
                            video: true,
                            audio: true
                        });
                        
                        const audioTracks = stream.getAudioTracks();
                        if (audioTracks.length === 0) {
                            Swal.fire('Error', 'No audio track found. Make sure you toggle "Share audio" in the popup.', 'error');
                            stream.getTracks().forEach(t => t.stop());
                            return;
                        }
                        
                        const audioStream = new MediaStream(audioTracks);
                        const mediaRecorder = new MediaRecorder(audioStream);
                        const chunks = [];
                        
                        mediaRecorder.ondataavailable = e => {
                            if(e.data.size > 0) chunks.push(e.data);
                        };
                        
                        mediaRecorder.onstop = () => {
                            // Compile to WebM/OGG depending on browser
                            const blob = new Blob(chunks, { type: 'audio/webm' });
                            const url = URL.createObjectURL(blob);
                            
                            // Show player
                            audioPreview.src = url;
                            audioPreviewContainer.style.display = 'block';
                            
                            // Trigger Download
                            const a = document.createElement('a');
                            a.href = url;
                            a.download = `tts_export_${Date.now()}.webm`;
                            a.click();
                            
                            // Cleanup
                            stream.getTracks().forEach(t => t.stop());
                            btnDownload.innerHTML = '<i class="fas fa-download me-2"></i> Capture & Download Audio';
                            btnDownload.disabled = false;
                        };
                        
                        mediaRecorder.start();
                        btnDownload.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> Recording...';
                        btnDownload.disabled = true;
                        
                        // Play the audio!
                        window.speechSynthesis.cancel();
                        utterance.onend = () => mediaRecorder.stop();
                        window.speechSynthesis.speak(utterance);
                        
                    } catch (err) {
                        console.error('Capture error:', err);
                        Swal.fire('Permission Denied', 'Audio capture was denied. Please allow tab capture to download.', 'error');
                    }
                }
            });
        });"""

new_download_logic = """        // 4. Download Engine (Direct MP3)
        const downloadForm = document.getElementById('downloadForm');
        const downloadTextInput = document.getElementById('downloadTextInput');

        downloadForm.addEventListener('submit', (e) => {
            const text = ttsInput.value.trim();
            if (!text) {
                e.preventDefault();
                Swal.fire('Empty', 'Please enter some text to download.', 'warning');
                return;
            }
            
            // Let the form submit natively to trigger the download attachment
            downloadTextInput.value = text;
            
            // Show a quick success toast
            Swal.fire({
                icon: 'success',
                title: 'Generating MP3...',
                text: 'Your download will start in a few seconds.',
                timer: 2500,
                showConfirmButton: false
            });
        });"""

content = content.replace(old_webrtc_logic, new_download_logic)

with open('templates/tts_converter.html', 'w') as f:
    f.write(content)
