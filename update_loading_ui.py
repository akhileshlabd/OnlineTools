import re

# 1. Update HTML
with open('templates/akinator.html', 'r') as f:
    content = f.read()

old_loading = """        <!-- Loading State -->
        <div id="loadingState" class="card-body d-flex flex-column align-items-center justify-content-center text-center p-5">
            <div class="spinner-border text-primary mb-3" role="status" style="width: 3rem; height: 3rem;"></div>
            <h5 class="fw-bold">Loading AI Brain...</h5>
        </div>"""

new_loading = """        <!-- Loading State -->
        <div id="loadingState" class="card-body d-flex flex-column align-items-center justify-content-center text-center p-5">
            <h4 class="fw-bold text-primary mb-3">Akinator is loading to beat you, pls wait...</h4>
            <div class="spinner-border text-primary mb-4" role="status" style="width: 4rem; height: 4rem; border-width: 0.3rem;"></div>
            <div class="progress w-100 shadow-sm" style="height: 20px; border-radius: 10px; max-width: 400px;">
                <div id="loadingProgressBar" class="progress-bar progress-bar-striped progress-bar-animated bg-primary" role="progressbar" style="width: 0%"></div>
            </div>
            <p id="loadingStatusText" class="text-muted small mt-3 fw-bold fs-6">Processing Data: 0%</p>
        </div>"""

if "Akinator is loading to beat you" not in content:
    content = content.replace(old_loading, new_loading)

with open('templates/akinator.html', 'w') as f:
    f.write(content)


# 2. Update JS
with open('static/js/akinatorUI.js', 'r') as f:
    js_content = f.read()

old_init = """    async initGame(jsonUrl) {
        this.show(this.ui.loading);
        await this.engine.init(jsonUrl);
        this.nextTurn();
    }"""

new_init = """    async initGame(jsonUrl) {
        this.show(this.ui.loading);
        
        const progressBar = document.getElementById('loadingProgressBar');
        const statusText = document.getElementById('loadingStatusText');
        
        let progress = 0;
        // Simulate a smooth progression to accommodate future large datasets
        const progressInterval = setInterval(() => {
            progress += Math.floor(Math.random() * 15) + 5;
            if (progress > 90) progress = 90; // Hold at 90% until fetch finishes
            
            if (progressBar && statusText) {
                progressBar.style.width = progress + '%';
                statusText.textContent = `Processing Data: ${progress}%`;
            }
        }, 150);

        try {
            await this.engine.init(jsonUrl);
            
            // Finish the progress bar
            clearInterval(progressInterval);
            if (progressBar && statusText) {
                progressBar.style.width = '100%';
                statusText.textContent = 'Brain Loaded! 100%';
            }
            
            // Brief pause to let user see 100% completion
            setTimeout(() => {
                this.nextTurn();
            }, 600);
            
        } catch (err) {
            clearInterval(progressInterval);
            if (statusText) {
                statusText.textContent = 'Error loading data. Please refresh.';
                statusText.classList.replace('text-muted', 'text-danger');
            }
            console.error(err);
        }
    }"""

if "loadingProgressBar" not in js_content:
    js_content = js_content.replace(old_init, new_init)

with open('static/js/akinatorUI.js', 'w') as f:
    f.write(js_content)

