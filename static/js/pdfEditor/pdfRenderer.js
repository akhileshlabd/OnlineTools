class PDFRenderer {
    constructor(containerId, thumbnailContainerId) {
        this.container = document.getElementById(containerId);
        this.thumbContainer = document.getElementById(thumbnailContainerId);
        this.pdfDoc = null;
        this.pdfBytes = null;
        this.scale = 1.5;
        this.pages = []; // { pageNum, pdfPage, viewport, canvas, textLayer }
    }

    async loadDocument(file) {
        this.pdfBytes = await file.arrayBuffer();
        this.pdfDoc = await pdfjsLib.getDocument({ data: this.pdfBytes.slice(0) }).promise;
        this.container.innerHTML = '';
        this.thumbContainer.innerHTML = '';
        this.pages = [];

        for (let i = 1; i <= this.pdfDoc.numPages; i++) {
            await this.renderPage(i);
        }
        return this.pdfDoc.numPages;
    }

    async renderPage(pageNum) {
        const page = await this.pdfDoc.getPage(pageNum);
        const viewport = page.getViewport({ scale: this.scale });
        
        // Main wrapper
        const wrapper = document.createElement('div');
        wrapper.className = 'pdf-page-wrapper';
        wrapper.dataset.page = pageNum;
        wrapper.style.width = viewport.width + 'px';
        wrapper.style.height = viewport.height + 'px';

        // Canvas for PDF render
        const canvas = document.createElement('canvas');
        canvas.className = 'pdf-render-canvas';
        canvas.width = viewport.width;
        canvas.height = viewport.height;
        const ctx = canvas.getContext('2d');
        
        await page.render({ canvasContext: ctx, viewport }).promise;

        // Text layer for extracting text and enabling patching
        const textLayerDiv = document.createElement('div');
        textLayerDiv.className = 'pdf-text-layer';
        textLayerDiv.style.width = viewport.width + 'px';
        textLayerDiv.style.height = viewport.height + 'px';
        
        const textContent = await page.getTextContent();
        for (const item of textContent.items) {
            const span = document.createElement('span');
            span.textContent = item.str;
            
            // Item transform is [scaleX, skewY, skewX, scaleY, tx, ty]
            const tx = item.transform[4] * this.scale;
            const ty = viewport.height - (item.transform[5] * this.scale); // Y is inverted in PDF
            const fontSize = Math.sqrt(item.transform[0] * item.transform[0] + item.transform[1] * item.transform[1]) * this.scale;
            
            // Basic approximation of text rendering
            span.style.left = tx + 'px';
            span.style.top = (ty - fontSize) + 'px'; // Adjust top by font size
            span.style.fontSize = fontSize + 'px';
            span.style.fontFamily = item.fontName || 'sans-serif';
            
            textLayerDiv.appendChild(span);
        }

        // Overlay for Fabric.js (handled by EditorUI)
        const overlayCanvas = document.createElement('canvas');
        overlayCanvas.className = 'pdf-fabric-canvas';
        overlayCanvas.id = `fabric-page-${pageNum}`;
        overlayCanvas.width = viewport.width;
        overlayCanvas.height = viewport.height;

        wrapper.appendChild(canvas);
        wrapper.appendChild(textLayerDiv);
        wrapper.appendChild(overlayCanvas);
        this.container.appendChild(wrapper);

        // Thumbnail
        this.renderThumbnail(page, pageNum);

        this.pages.push({
            pageNum,
            viewport,
            originalWidth: viewport.width / this.scale,
            originalHeight: viewport.height / this.scale
        });
    }

    async renderThumbnail(page, pageNum) {
        const thumbScale = 0.2;
        const viewport = page.getViewport({ scale: thumbScale });
        const canvas = document.createElement('canvas');
        canvas.width = viewport.width;
        canvas.height = viewport.height;
        canvas.className = 'pdf-thumb-canvas';
        canvas.onclick = () => {
            document.querySelector(`.pdf-page-wrapper[data-page="${pageNum}"]`).scrollIntoView({ behavior: 'smooth' });
        };
        await page.render({ canvasContext: canvas.getContext('2d'), viewport }).promise;
        
        const wrap = document.createElement('div');
        wrap.className = 'thumb-wrap';
        wrap.appendChild(canvas);
        const lbl = document.createElement('div');
        lbl.textContent = pageNum;
        wrap.appendChild(lbl);
        this.thumbContainer.appendChild(wrap);
    }
}
window.PDFRenderer = PDFRenderer;

